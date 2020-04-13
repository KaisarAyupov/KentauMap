import os
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from folium.plugins import FastMarkerCluster
import branca

df = pd.read_csv('data/GammaPntAll.csv', engine='python')
df.columns = df.columns.str.strip()

#creating a map that's centered to our sample
gamma_pnt_map = folium.Map(location=[df['xdd'].mean(), 
                                df['ydd'].mean()], 
                                zoom_start=11)

mc = MarkerCluster()

#creating a Marker for each point in df_sample.  Each point will get a popup with their zip
for row in df.itertuples():
    mc.add_child(folium.Marker(location=[row.xdd, row.ydd], icon=None,
                    popup=row.Gamma))
    
gamma_pnt_map.add_child(mc)

legend_html =   '''
                <div style="position: fixed; 
                            bottom: 50px; left: 50px; padding: 5px; border:2px solid grey; z-index:9999; font-size:14px; background-color: #ffffff;
                            ">&nbsp; УСЛОВНЫЕ ОБОЗНАЧЕНИЯ: <br>
                              &nbsp; Точки замеров гамма-съемки; <i class="fa fa-map-marker fa-2x" style="color:#2e85cb"></i><br>
                </div>
                ''' 

gamma_pnt_map.get_root().html.add_child(folium.Element(legend_html))

gamma_pnt_map.save(os.path.join('results', 'Gamma MarkerClusters Map.html'))
