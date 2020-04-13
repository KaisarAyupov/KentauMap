import os
import pandas as pd
import folium
from folium.plugins import HeatMap
from folium.plugins import HeatMapWithTime
from datetime import datetime, timedelta


df = pd.read_csv('data/GammaPnt.csv', engine='python')

df.SampleTime = pd.to_datetime(df.SampleTime, format='%Y-%m-%d %H:%M:%S')
df['month'] = df.SampleTime.apply(lambda x: x.month)
df['week'] = df.SampleTime.apply(lambda x: x.week)
df['day'] = df.SampleTime.apply(lambda x: x.day)
df['hour'] = df.SampleTime.apply(lambda x: x.hour)


def generateBaseMap(default_location=[43.509, 68.508], default_zoom_start=15):
    gamma_map = folium.Map(location=default_location, control_scale=True, zoom_start=default_zoom_start)
    return gamma_map


df_copy = df.copy()

gamma_map = generateBaseMap()
HeatMap(data=df_copy[['xdd', 'ydd', 'Gama']].groupby(['xdd', 'ydd']).sum().reset_index().values.tolist(), radius=8).add_to(gamma_map)

gamma_map.add_child(folium.ClickForMarker(popup='Potential Location'))
df_hour_list = []
for hour in df_copy.SampleData.sort_values().unique():
    df_hour_list.append(df_copy.loc[df_copy.SampleData == hour, ['xdd', 'ydd', 'Gama']].groupby(['xdd', 'ydd']).sum().reset_index().values.tolist())

##print(df_hour_list)

time_index = list(df_copy.SampleData.sort_values().unique())
gamma_map = generateBaseMap(default_zoom_start=14)
HeatMapWithTime(df_hour_list, index=time_index, radius=10, gradient={0.2: 'cyan', 0.4: 'yellow', 0.6: 'orange', 1: 'red'}, min_opacity=0.5, max_opacity=0.8, use_local_extrema=True).add_to(gamma_map)

gamma_map.save(os.path.join('results', 'GammaSamplingMapWithTime.html'))
