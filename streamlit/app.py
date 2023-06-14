import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium, folium_static
# from gbq_functions.big_query_download import *
from gbq_functions.params import *
import seaborn as sns
import matplotlib.pyplot as plt
from google.cloud import bigquery

'''
# Location Analysis
'''

st.markdown('''
# OUTPUTS!
''')

outputs_df = pd.read_csv("../outputs/model_output_labels.csv")
st.dataframe(outputs_df, use_container_width=True)

carehomes_df = pd.read_csv("../raw_data/carehome_locations.csv")
london_carehomes = carehomes_df[carehomes_df['region']=="London"]
# st.dataframe(london_carehomes, use_container_width=True)


@st.cache_data
def get_master_district_df():
    '''function that returns the full master district df.
    Dataframe contains district name (primary key), lat_lons for the center,
    lat_lons for the edges of rectangle around area, and the area of the
    rectangle in Hectares'''

    query = f"""
            SELECT {",".join(MASTER_COLUMN_NAMES_RAW)}
            FROM {GCP_PROJECT}.{BQ_DATASET}.{BQ_DISTRICT_TABLE}
            ORDER BY HECTARES DESC
        """

    client = bigquery.Client(project=GCP_PROJECT)
    query_job = client.query(query)
    result = query_job.result()
    master_districts_df = result.to_dataframe()
    return master_districts_df


district_list = get_master_district_df()['District']
district_list


golden_df = pd.read_csv('../raw_data/golden_df_wb_tests.csv')
# golden_df


labeled_df = pd.read_csv('../outputs/test_labelled_districts.csv')
mapObj = folium.Map(location=[51.509865,-0.118092], zoom_start=10)

# adding carehome points to map

def plotDot(point):
    '''input: series that contains a numeric named latitude and a numeric named longitude
    this function creates a CircleMarker and adds it to your this_map'''
    folium.CircleMarker(location=[point.latitude, point.longitude],
                        radius=(point.num_beds)/100,
                        weight=2,
                        tooltip=point.Location_Names).add_to(mapObj)

london_carehomes.apply(plotDot, axis = 1)

# option = st.selectbox("select district(s)",

with st.form("district input"):
    district_input = st.text_input("input district name:")


    submitted = st.form_submit_button("Submit")
    if submitted:
       golden_df[golden_df['district_name']==district_input]
       labeled_df_filtered = labeled_df[labeled_df['district_name']==district_input]
       lats = labeled_df_filtered['lat']
       longs = labeled_df_filtered['lng']
       clusters = labeled_df_filtered['Labels']
       zipped = zip(lats, longs, clusters)
       data = np.array(list(zipped))


HeatMap(data, scale_radius=True, radius=30).add_to(mapObj)
folium_static(mapObj, width = 725)
labeled_df_filtered

# filtered_df = golden_df[golden_df['district_name']==district_input]


# lats = labeled_df['lat']
# longs = labeled_df['lng']
# clusters = labeled_df['Robust__Non_PCA_Crimeless_Labels']
# zipped = zip(lats, longs, clusters)
# data = np.array(list(zipped))
# HeatMap(data, scale_radius=True, radius=30).add_to(mapObj)



# fig = plt.figure(figsize=(10, 4))

# sns.scatterplot(x=outputs_df['lng'], y=outputs_df['lat'], hue=outputs_df.Robust__Non_PCA_Crimeless_Labels, palette='Set1', marker = ".")
# sns.scatterplot(x = london_carehomes["longitude"], y = london_carehomes["latitude"], c='black' ,alpha=0.3)
# plt.show()

# sns.scatterplot(x=outputs_df['lng'], y=outputs_df['lat'], hue=outputs_df.MinMax_Non_PCA_Crimeless_Labels, palette='Set1', marker = ".")
# sns.scatterplot(x = london_carehomes["longitude"], y = london_carehomes["latitude"], c='black' ,alpha=0.3)
# plt.show()
# # st.pyplot(fig)


# Square Map function

# import matplotlib as mpl


# # set up the grid
# step = 0.02
# lat_step = max(n2 - n1 for n1, n2 in zip(sorted(set(lats)), sorted(set(lats))[1:]))
# long_step = max(n2 - n1 for n1, n2 in zip(sorted(set(longs)), sorted(set(longs))[1:]))
# xi, yi = np.meshgrid(
#     lats,
#     longs,
# )


# g = np.stack([
#     lats,
#     longs,
#     clusters
# ], axis=1)

# # geo_json returns a single square
# def geo_json(lat, long, cluster, lat_step, long_step):
#     cmap = mpl.cm.viridis
#     return {
#       "type": "FeatureCollection",
#       "features": [
#         {
#           "type": "Feature",
#           "properties": {
#             'color': 'white',
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


# # ...with squares...
# for i in range(len(clusters)):
#     folium.GeoJson(geo_json(lats[i], longs[i], clusters[i], lat_step, long_step),
#                    lambda x: x['properties']).add_to(mapObj)

# st_folium(mapObj, width = 725)
