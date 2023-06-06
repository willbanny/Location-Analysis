import googlemaps
import time
import pandas as pd
import geopy.distance
from params import *


API_KEY = GOOGLE_PLACE_API_KEY
# print(f'GOOGLE_PLACE_API_KEY = {GOOGLE_PLACE_API_KEY}')

# --- SET VARIABLES ---
district_string = 'City of Leicester (B)'
search_type_list = ['hospital', 'train_station', 'bus_station', 'park', 'place_of_worship']
# search_type_list = ['hospital']

# load district db as df
df_districts = pd.read_csv(f'{PWD_CURR}/raw_data/district_coords_clean.csv')

chosen_district = df_districts[df_districts['District'] == district_string]
origin_location = (chosen_district.iloc[0]['Centroid_Lat'], chosen_district.iloc[0]['Centroid_Lon'])
bottom_left = (chosen_district.iloc[0]['BR_Bottom'], chosen_district.iloc[0]['BR_Left'])
radius_size_meters = geopy.distance.geodesic(origin_location, bottom_left).m

# Find and record all locations of types defined in 'search_type_list' withing the given radius 'distance'
map_client = googlemaps.Client(key = API_KEY)
lst_df = []
for t in search_type_list:
    lst_temp = []
    response = map_client.places_nearby(
        location=origin_location,
        radius=radius_size_meters,
        type=t,
    )
    lst_temp.extend(response.get('results'))
    next_page_token = response.get('next_page_token')
    while next_page_token:
        time.sleep(3)

        response = map_client.places_nearby(
            location=origin_location,
            radius=radius_size_meters,
            type=t,
            page_token=next_page_token
        )

        lst_temp.extend(response.get('results'))
        next_page_token = response.get('next_page_token')
    lst_df.append(pd.DataFrame(lst_temp))

# Store locations for various types in different csvs
frames = []
for i in range(0, len(lst_df)):
    formatted_df = pd.DataFrame(lst_df[i]['geometry'].map(lambda x: x['location'])).copy()
    formatted_df['lat'] = formatted_df['geometry'].map(lambda x: x['lat'])
    formatted_df['lng'] = formatted_df['geometry'].map(lambda x: x['lng'])
    formatted_df = formatted_df.drop(columns=['geometry'])
    formatted_df['feature_name'] = search_type_list[i]
    frames.append(formatted_df.copy())
result = pd.concat(frames)
result['district'] = district_string

result.to_csv(f'{PWD_CURR}/raw_data/features/google_data.csv', index=False)
