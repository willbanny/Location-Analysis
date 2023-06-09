import requests
from params import *
import pandas as pd
import geopy.distance
import time
from gbq_functions.big_query_download import *


district_list = ['Croydon London Boro',
 'Bromley London Boro',
 'Hounslow London Boro',
 'Ealing London Boro',
 'Havering London Boro',
 'Harrow London Boro',
 'Brent London Boro',
 'Barnet London Boro',
 'Lambeth London Boro',
 'Southwark London Boro',
 'Lewisham London Boro',
 'Greenwich London Boro',
 'Bexley London Boro',
 'Waltham Forest London Boro',
 'Redbridge London Boro',
 'Richmond upon Thames London Boro',
 'Merton London Boro',
 'Wandsworth London Boro',
 'Kensington and Chelsea London Boro',
 'City of Westminster London Boro',
 'Camden London Boro',
 'Tower Hamlets London Boro',
 'Islington London Boro',
 'Hackney London Boro',
 'Haringey London Boro',
 'Newham London Boro',
 'Barking and Dagenham London Boro',
 'City and County of the City of London',
 'Kingston upon Thames London Boro',
 'Enfield London Boro',
 'Sutton London Boro',
 'Hammersmith and Fulham London Boro',
 'Hillingdon London Boro']


# Set your API key and endpoint URL
API_KEY = GOOGLE_PLACE_API_KEY
ENDPOINT_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

# Set district origin and radius for search
df_districts = pd.read_csv(f'{PWD_CURR}/raw_data/district_coords_clean.csv')

county = 0
for district_string in district_list:
    # district_string = 'Bromley London Boro'
    county += 1
    print(f'\n+============================================================+\n{district_string} Start\nCount = {county}\n+============================================================+\n')

    chosen_district = df_districts[df_districts['District'] == district_string]
    origin_location = (chosen_district.iloc[0]['Centroid_Lat'], chosen_district.iloc[0]['Centroid_Lon'])
    location_string = f'{chosen_district.iloc[0]["Centroid_Lat"]}, {chosen_district.iloc[0]["Centroid_Lon"]}'
    bottom_left = (chosen_district.iloc[0]['BR_Bottom'], chosen_district.iloc[0]['BR_Left'])
    radius_size_meters = f'{geopy.distance.geodesic(origin_location, bottom_left).m}'

    print(f'Radius (m) = {radius_size_meters}')
    print(f'Origin = {location_string}')
    print(f'Bottom Left = {bottom_left}')

    # Set params
    queries = ['all hospital', 'all train station', 'all bus station', 'all park', 'all places of worship', 'all parking', 'all leisure centre', 'all museum', 'all national trust']
    # queries = ['all hospital']
    q_features = []
    for q in queries:
        x = q.replace('all ', '', 1)
        x = x.replace(' ', '_')
        q_features.append(x)


    results = []

    for i in range(0, len(queries)):
        # Set additional parameters for the search
        params = {
            'location': location_string,
            'radius': radius_size_meters,  # Adjust the radius as needed
            'keyword': queries[i],
            'key': API_KEY
        }

        # Send the initial API request
        response = requests.get(url=ENDPOINT_URL, params=params)
        data = response.json()

        # Parse the response and extract coordinates
        while True:
            if data['status'] == 'OK':
                for result in data['results']:
                    name = result['name']
                    location = result['geometry']['location']
                    latitude = location['lat']
                    longitude = location['lng']
                    results.append({'Name': name, 'lat': latitude, 'lng': longitude, 'feature_name': q_features[i]})

                if 'next_page_token' in data:
                    time.sleep(2)
                    params['pagetoken'] = data['next_page_token']
                    response = requests.get(url=ENDPOINT_URL, params=params)
                    data = response.json()
                else:
                    # No more next page token, exit the loop
                    break
            else:
                print(f"Request failed with status: {data['status']}")
                break
        print(f'---> Complete: {q_features[i]}')

    df = pd.DataFrame(results)
    df['district'] = district_string

    # print(df)
    # df.to_csv(f'{PWD_CURR}/raw_data/features/google_data.csv', index=False)
    upload_google_api_outputs(district_string, df)
    print(f'\n+============================================================+\n{district_string} Uploaded\n+============================================================+\n')
