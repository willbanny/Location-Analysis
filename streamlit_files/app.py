import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium, folium_static
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import streamlit.components.v1 as components


# Location Analysis

st.markdown('''
# OUTPUTS!
''')

# HtmlFile = open("../maps/leicester_squares_map.html", 'r', encoding='utf-8')
# source_code = HtmlFile.read()
# components.html(source_code, width=1200, height=600)


# outputs_df = pd.read_csv("../raw_data/model_output_labels.csv")
# st.dataframe(outputs_df, use_container_width=True)

# carehomes_df = pd.read_csv("../raw_data/carehome_locations.csv")
# london_carehomes = carehomes_df[carehomes_df['region']=="London"]
# # st.dataframe(london_carehomes, use_container_width=True)

@st.cache_data  # 👈 Add the caching decorator
def load_data(csv):
    df = pd.read_csv(csv)
    return df

df = load_data('../raw_data/display_gd.csv')
golden_df = df[df['district_name'] == 'Cambridge District (B)']
golden_df = golden_df.drop_duplicates(['lat', 'lng'])
golden_df['id'] = golden_df.index


mapObj = folium.Map(location=[51.509865,-0.118092], zoom_start=10, prefer_canvas=True)

# adding carehome points to map

# def plotDot(point):
#     '''input: series that contains a numeric named latitude and a numeric named longitude
#     this function creates a CircleMarker and adds it to your this_map'''
#     folium.CircleMarker(location=[point.latitude, point.longitude],
#                         radius=(point.num_beds)/100,
#                         weight=2,
#                         tooltip=point.Location_Names).add_to(mapObj)

# london_carehomes.apply(plotDot, axis = 1)

lats = np.array( golden_df['lat'] )
longs = np.array( golden_df['lng'] )
# clusters = np.array( golden_df['Robust__Non_PCA_Crimeless_Labels'] )

# HeatMap(data, scale_radius=True, radius=30).add_to(mapObj)

# folium_static(mapObj, width = 725)

# fig = plt.figure(figsize=(10, 4))

# sns.scatterplot(x=outputs_df['lng'], y=outputs_df['lat'], hue=outputs_df.Robust__Non_PCA_Crimeless_Labels, palette='Set1', marker = ".")
# sns.scatterplot(x = london_carehomes["longitude"], y = london_carehomes["latitude"], c='black' ,alpha=0.3)
# plt.show()

# sns.scatterplot(x=outputs_df['lng'], y=outputs_df['lat'], hue=outputs_df.MinMax_Non_PCA_Crimeless_Labels, palette='Set1', marker = ".")
# sns.scatterplot(x = london_carehomes["longitude"], y = london_carehomes["latitude"], c='black' ,alpha=0.3)
# plt.show()
# # st.pyplot(fig)


# Square Map function

#breakpoint()


# set up the grid
lat_step = max(n2 - n1 for n1, n2 in zip(sorted(set(lats)), sorted(set(lats))[1:]))
long_step = max(n2 - n1 for n1, n2 in zip(sorted(set(longs)), sorted(set(longs))[1:]))


# geo_json returns a single square

# @st.cache_data  # 👈 Add the caching decorator
# def geo_json(lat, long, cluster, lat_step, long_step):
#     cmap = mpl.cm.viridis
#     return {
#       "type": "FeatureCollection",
#       "features": [
#         {
#           "type": "Feature",
#           "properties": {
#             'color': 'white',
#             'opacity': '0',
#             'weight': 1,
#             'fillColor': mpl.colors.to_hex(cmap(cluster*( 255//max(clusters) ) ) ),
#             'fillOpacity': 0.5,
#           },
#           "geometry": {
#             "type": "Polygon",
#             "coordinates": [[
#                 [long - long_step/2, lat - lat_step/2],
#                 [long - long_step/2, lat + lat_step/2],
#                 [long + long_step/2, lat + lat_step/2],
#                 [long + long_step/2, lat - lat_step/2],
#                 [long - long_step/2, lat - lat_step/2],
#               ]]}}]}



my_geo_json = {
      "type": "FeatureCollection",
      "features": []}


for i in range(len(lats)):
    my_geo_json['features'].append(
        {
          "type": "Feature",
          "properties": {},
          "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [longs[i] - long_step/2, lats[i] - lat_step/2],
                [longs[i] - long_step/2, lats[i] + lat_step/2],
                [longs[i] + long_step/2, lats[i] + lat_step/2],
                [longs[i] + long_step/2, lats[i] - lat_step/2],
                [longs[i] - long_step/2, lats[i] - lat_step/2],
              ]]},
          "id": int(golden_df['id'].values[i])
        }
    )


folium.Choropleth(
    geo_data=my_geo_json,
    data=golden_df,
    columns = ['id','metric'],
    fill_color='YlGn',
    fill_opacity=0.5,
    line_opacity=0,
    key_on='feature.id',
    bins=5
).add_to(mapObj)



# ...with squares...

# def apply_squares():
#     for i in np.arange(len(clusters)):
#         folium.GeoJson(geo_json(lats[i], longs[i], clusters[i], lat_step, long_step),
#                     lambda x: x['properties']).add_to(mapObj)

# apply_squares()

folium_static(mapObj, width = 725)
