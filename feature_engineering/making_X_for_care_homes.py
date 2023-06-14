import pandas as pd
import numpy as np
from gbq_functions.big_query_download import *
from sklearn.neighbors import BallTree
from gbq_functions.big_query_download import *
from math import radians, sin, cos, sqrt, atan2

care_df = pd.read_csv('/Users/nateoppenheimer/code/willbanny/Location-Analysis/feature_engineering/care_homes_by_district.csv')

def calculate_distance(coord1, coord2):
    # Convert coordinates to radians
    lon1, lat1 = radians(coord1['lng']), radians(coord1['latitude'])
    lon2, lat2 = radians(coord2['lng']), radians(coord2['latitude'])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distance = 6371 * c  # Radius of the Earth in kilometers

    return distance * 1000  # Convert distance to meters

def count_coordinates_within_distance(coord_df, target_df, distance):
    coord_df_rad = np.radians(coord_df[['lng', 'lat']])
    target_df_rad = np.radians(target_df[['lng', 'lat']])

    lat_diff = target_df_rad['lat'].values[:, np.newaxis] - coord_df_rad['lat'].values
    lon_diff = target_df_rad['lng'].values[:, np.newaxis] - coord_df_rad['lng'].values

    a = np.sin(lat_diff / 2)**2 + np.cos(target_df_rad['lat'].values[:, np.newaxis]) * \
        np.cos(coord_df_rad['lat'].values) * np.sin(lon_diff / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distances = 6371 * c * 1000  # Convert distance to meters

    counts = np.sum((distances >= distance[0]) & (distances <= distance[1]), axis=1)
    return counts

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
#  'City and County of the City of London',
 'Kingston upon Thames London Boro',
 'Enfield London Boro',
 'Sutton London Boro',
 'Hammersmith and Fulham London Boro',
 'Hillingdon London Boro']

# district_list = ['City and County of the City of London']
# print(care_df[care_df['district_name'] == 'City and County of the City of London'])

count_num_dis_to_bq = 0
final_df = pd.DataFrame()
for district_string in district_list:

    radius_list = [0, 100, 250, 500, 750, 1000, 1250, 1500]

    grid_coords = care_df[care_df['district_name']==district_string].reset_index(drop=True).copy()
    google_data = get_google_df(district_string)
    crime_data = get_crime_df(district_string)
    crime_data = crime_data.rename(columns={"Latitude": "lat", "Longitude": "lng"})
    dep_df = get_deprivation_df(district_string)
    print(f'+----------------------------------------+\nfinished getting all data from big querey\n+----------------------------------------+\n')

    # grid_coords = grid_coords.rename(columns={"Latitude": "lat", "Longitude": "lng"})

    # google -- engineering
    google_engineered = pd.DataFrame()
    features = list(google_data['feature_name'].unique())
    for i in range(0, len(radius_list)-1):
        for f in features:
            google_engineered[f'{f}_{radius_list[i+1]}']\
                =count_coordinates_within_distance\
                    (google_data[google_data['feature_name']==f][['lat', 'lng']], grid_coords[['lat', 'lng']], radius_list[i:(i+2)])
            print(f'{f}_{radius_list[i+1]} completed')
    google_engineered = google_engineered.join(grid_coords[['lng', 'lat']])


    # crime -- engineering
    crime_engineered = pd.DataFrame()
    features = list(crime_data['Crime_type'].unique())
    for i in range(0, len(radius_list)-1):
        for f in features:
            crime_engineered[f'{f}_{radius_list[i+1]}']\
                =count_coordinates_within_distance\
                    (crime_data[crime_data['Crime_type']==f][['lat', 'lng']], grid_coords[['lat', 'lng']], radius_list[i:(i+2)])
            print(f'{f}_{radius_list[i+1]} completed')
    crime_engineered = crime_engineered.join(grid_coords[['lng', 'lat']])

    print('\n+============================================================+\nAll distances to crime and google maps features complete\n+============================================================+\n')

    # deprevation -- engineering
    bt = BallTree(np.deg2rad(dep_df[['latitude', 'longitude']].values), metric='haversine')

    distances, indices = bt.query(np.deg2rad(grid_coords[['lat', 'lng']]))
    print(f'distance: {distances}\nindices: {indices}')

    dep_engineered = dep_df.iloc[indices[:, 0]]
    dep_engineered[['lng', 'lat']] = grid_coords[['lng', 'lat']].values
    print('\n+============================================================+\nFinished with the finding closest dep thing\n+============================================================+\n')

    # Store
    # google_engineered.to_csv('google_trail_bigQuery.csv')
    # crime_engineered.to_csv('crime_trial_bigQuery.csv')
    # dep_engineered.to_csv('dep_trial_bigQuery.csv')

    # Build Golden DF
    golden_df = google_engineered\
    .merge(crime_engineered, how='left', on=['lng', 'lat'])\
    .merge(dep_engineered, how='left', on=['lng', 'lat'])

    # Upload Golden DF
    new_l = []
    for c_name in list(golden_df.columns):
        c_name = c_name.replace('-', '_')
        c_name = c_name.replace(' ', '_')
        new_l.append(c_name)
    golden_df.columns = new_l
    golden_df['district_name'] = district_string

    golden_df.to_csv('meh.csv')
    # upload_golden_df(district_string, golden_df)
    print(f'\n+============================================================+\nGolden DF Uploaded for {district_string}\n+============================================================+\n')
    final_df = pd.concat([final_df, golden_df.copy()])
final_df.to_csv('care_homes_X.csv')
