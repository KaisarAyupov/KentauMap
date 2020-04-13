import os
import datetime
import ee.mapclient
import ee
import folium 
import geehydro
import numpy as np # yes, numpy!
import pandas as pd # yes, pandas!
from ipygee import*
from pandas.plotting import register_matplotlib_converters

ee.Initialize()

adm2_polygon = ee.FeatureCollection('users/caesar699/AdmRegion/adm2pol')
# select the adm2pol Indigenous Park shapefile
adm2pol = adm2_polygon.filter(ee.Filter.eq('CD', 5120))

NDVI_map = folium.Map(location=[43.5236, 68.4152], zoom_start=12)
NDVI_map.addLayer(adm2pol)

# Filter the L7 collection to a single month.
collection = (ee.ImageCollection('COPERNICUS/S2')
              .filterBounds(adm2pol)
              .filterMetadata('CLOUD_COVERAGE_ASSESSMENT','less_than',10)
              .filterDate(datetime.datetime(2019, 5, 1),
                          datetime.datetime(2019, 9, 1)))

def NDVI(image):
  """A function to compute NDVI."""
  return image.expression('float(b("B8") - b("B4")) / (b("B8") + b("B4"))')
def SAVI(image):
  """A function to compute Soil Adjusted Vegetation Index."""
  return ee.Image(0).expression(
      '(1 + L) * float(nir - red)/ (nir + red + L)',
      {
          'nir': image.select('B4'),
          'red': image.select('B3'),
          'L': 0.2
      })

vis = {
    'min': 0,
    'max': 1,
    'palette': [
        'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163',
        '99B718', '74A901', '66A000', '529400', '3E8601',
        '207401', '056201', '004C00', '023B01', '012E01',
        '011D01', '011301'
    ]}
# mean NDVI in the Xingu Park
NDVI_map.addLayer(collection.map(NDVI).mean().clip(adm2pol), vis)

from branca.element import Template, MacroElement

template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
     
<div class='legend-title'>Legend:</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:green;opacity:0.7;'></span>High</li>
    <li><span style='background:orange;opacity:0.7;'></span>Middle</li>
    <li><span style='background:red;opacity:0.7;'></span>Low</li>

  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

macro = MacroElement()
macro._template = Template(template)
NDVI_map.get_root().add_child(macro)

title_html = """
<div style="position: fixed; 
     top: 20px; left: 80px; border:2px solid grey; z-index:9999; background-color: white;"> 
  <div class="col-sm-auto">
  <h5 style="margin: 10px;" class="card-title">СОСТОЯНИЕ РАСТИТЕЛЬНОГО ПОКРОВА</h5>
  <p class="text-center">(2019года, по данным Sentinel-2)</p>
  </div>
</div>"""
NDVI_map.get_root().html.add_child(folium.Element(title_html))
NDVI_map.save(os.path.join('results','SentinelNDVI.html'))
