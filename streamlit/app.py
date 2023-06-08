import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium


'''
# Location Analysis
'''

st.markdown('''
Test Header
''')

carehomes_df = pd.read_csv("../raw_data/carehome_locations.csv")

st.dataframe(carehomes_df, use_container_width=True)


golden_df = pd.read_csv('../raw_data/croydon_golden_with_labels.csv')
mapObj = folium.Map(location=[51.3895011342637,-0.107834356217441], zoom_start=11.5)
lats = golden_df['lat']
longs = golden_df['lng']
clusters = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1,
       1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 2, 0, 2,
       0, 0, 1, 1, 1, 1, 1, 1, 0, 2, 2, 0, 2, 0, 1, 1, 1, 1, 1, 1, 0, 0,
       2, 0, 1, 1, 1, 1, 2, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1,
       1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1]
zipped = zip(lats, longs, clusters)
data = np.array(list(zipped))
HeatMap(data, scale_radius=True, radius=30).add_to(mapObj)
st_folium(mapObj, width = 725)
