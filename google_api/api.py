# pip install googlemaps
# pip install prettyprint

import googlemaps
import pprint
import time
import pandas as pd

API_KEY = 'AIzaSyBI4OBAQiNen89euuT-cirsIJwwBebGoS8'

def miles_to_meters(miles):
    try:
        return miles/0.00062137
    except:
        print('something went wrong')

city_string = 'Leicester'
search_type_list = ['hospital', 'train_station', 'bus_station', 'park', 'place_of_worship']
# search_type_list = ['bus_station']
radius_miles_from_center = 3

df = pd.read_csv('/Users/nateoppenheimer/code/willbanny/Location-Analysis/raw_data/gb_towns_lat_lon_pop.csv')

# df

chosen_city = df[df['city'] == city_string]

location = (chosen_city.iloc[0]['lat'], chosen_city.iloc[0]['lng'])

distance = miles_to_meters(radius_miles_from_center)

# Client
map_client = googlemaps.Client(key = API_KEY)

lst_df = []
for t in search_type_list:
    lst_temp = []
    response = map_client.places_nearby(
        location=location,
        radius=distance,
        type=t,
    )
    lst_temp.extend(response.get('results'))
    next_page_token = response.get('next_page_token')
    while next_page_token:
        time.sleep(3)

        response = map_client.places_nearby(
            location=location,
            radius=distance,
            type=t,
            page_token=next_page_token
        )

        lst_temp.extend(response.get('results'))
        next_page_token = response.get('next_page_token')
    lst_df.append(pd.DataFrame(lst_temp))

for i in range(0, len(lst_df)):
    lst_df[i][['geometry']].to_csv(f'/Users/nateoppenheimer/code/willbanny/Location-Analysis/raw_data/features/{search_type_list[i]}.csv')

# lst_df[0]
