import pandas as pd
import numpy as np
import geopy.distance as GD
from gbq_functions.big_query_download import *
from sklearn.neighbors import BallTree

radius_list = [0, 500, 1000, 1500]
district_string = 'City of Leicester (B)'

grid_coords = get_district_gridpoints_df(district_string)
google_data = get_google_df(district_string)
crime_data = get_crime_df(district_string)
crime_data = crime_data.rename(columns={"Latitude": "lat", "Longitude": "lng"})
dep_df = get_deprivation_df(district_string)

grid_coords = grid_coords.rename(columns={"Latitude": "lat", "Longitude": "lng"})

google_engineered = grid_coords.copy()
crime_engineered = grid_coords.copy()

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

# google -- engineering

for i in range(0, len(radius_list)-1):
    google_engineered = find_given_radius(radius_list[i:i+2], google_engineered, google_data, list(google_data['feature_name'].unique()), 'feature_name')

# crime -- engineering

for i in range(0, len(radius_list)-1):
    crime_engineered = find_given_radius(radius_list[i:i+2], crime_engineered, crime_data, list(crime_data['Crime_type'].unique()), 'Crime_type')

# dep -- engineering

bt = BallTree(np.deg2rad(dep_df[['latitude', 'longitude']].values), metric='haversine')

distances, indices = bt.query(np.deg2rad(grid_coords[['lat', 'lng']]))

dep_engineered = dep_df.iloc[indices[:, 0]]
dep_engineered[['lng', 'lat']] = grid_coords[['lng', 'lat']].values

# Upload

google_engineered.to_csv('google_trail_bigQuery.csv')
crime_engineered.to_csv('crime_trial_bigQuery.csv')
dep_engineered.to_csv('dep_trial_bigQuery.csv')

# Build Golden DF
golden_df = google_engineered\
.merge(crime_engineered, how='left', on=['lng', 'lat'])\
.merge(dep_engineered, how='left', on=['lng', 'lat'])

# Upload Golden DF
# golden_df[list(golden_df.select_dtypes('int64').columns)] = \
#     golden_df[list(golden_df.select_dtypes('int64').columns)].astype('float64')
col_nam = []
for i in list(golden_df.columns):
    x = i.replace(' ', '_')
    col_nam.append(x.replace('-', '_'))
golden_df.columns = col_nam

golden_df.to_csv('golden_df_trial_bigQuery.csv')
upload_golden_df(district_string, golden_df)
