import pandas as pd
import geopy.distance as GD
from gbq_functions.big_query_download import *
from scipy import spatial

radius_list = [0, 500, 1000, 1500]

grid_coords = get_district_gridpoints_df('City of Leicester (B)')
google_data = get_google_df('City of Leicester (B)')
crime_data = get_crime_df('City of Leicester (B)')
dep_df = get_deprivation_df('City of Leicester (B)')
crime_data = crime_data.rename(columns={"Latitude": "lat", "Longitude": "lng"})

grid_coords = grid_coords.rename(columns={"Latitude": "lat", "Longitude": "lng"})

google_engineered = grid_coords.copy()
crime_engineered = grid_coords.copy()
dep_engineered = grid_coords.copy()

def ret_true_false(c1, c2, r):
    dis = GD.geodesic((c1['lng'], c1['lat']), (c2['lng'], c2['lat'])).m
    if dis < r[1] and dis > r[0]:
        return True
    return False

def find_given_radius(r, google_engineered, google_data, features, feature_name):
    for f in features:
        google_engineered[f'{f}_{r[1]}'] = \
        google_engineered.apply(lambda c1: google_data[google_data[f'{feature_name}']==f].apply\
                             (lambda c2: ret_true_false(c1, c2, r), axis=1)\
                             .sum(), axis=1)
    return google_engineered

for i in range(0, len(radius_list)-1):
    google_engineered = find_given_radius(radius_list[i:i+2], google_engineered, google_data, list(google_data['feature_name'].unique()), 'feature_name')

for i in range(0, len(radius_list)-1):
    crime_engineered = find_given_radius(radius_list[i:i+2], crime_engineered, crime_data, list(crime_data['Crime_type'].unique()), 'Crime_type')


google_engineered.to_csv('google_trail_bigQuery.csv')
crime_engineered.to_csv('crime_trial_bigQuery.csv')

# dep -- engineering

row_list =[]
for index, rows in dep_df.iterrows():
    my_list =(rows.longitude, rows.latitude)
    row_list.append(my_list)
tree = spatial.KDTree(row_list)

def ret_long_lat_key(c1):
    return row_list[tree.query([(c1['lat'],c1['lng'])])[1][0]]

coor_index = grid_coords.apply(lambda c1: ret_long_lat_key(c1), axis=1)

dep_engineered['lng_m'] = coor_index.map(lambda x: x[0])
dep_engineered['lat_m'] = coor_index.map(lambda x: x[1])
# dep_engineered

dep_engineered = pd.merge(dep_engineered, dep_df,  how='left', left_on=['lng_m','lat_m'], right_on = ['longitude','latitude'])
dep_engineered = dep_engineered.drop(columns=['lng_m', 'lat_m'])

dep_engineered.to_csv('dep_trial_bigQuery.csv')
