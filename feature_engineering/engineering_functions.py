import pandas as pd
import geopy.distance as GD

radius_list = [500, 1000, 1500]

grid_coords = pd.read_csv('/Users/nateoppenheimer/code/willbanny/Location-Analysis/raw_data/features/bquxjob_2efec792_188918eb4d5.csv')
google_data = pd.read_csv('/Users/nateoppenheimer/code/willbanny/Location-Analysis/raw_data/features/google_data.csv')

google_engineered = grid_coords.copy()
google_engineered = google_engineered.rename(columns={"Latitude": "lat", "Longitude": "lng"})

def find_given_radius(r, grid_coords, google_data, features):
    for f in features:
        grid_coords[f'{f}_{r}'] = \
        grid_coords.apply(lambda c1: google_data[google_data['feature_name']==f].apply\
                             (lambda c2: GD.geodesic((c1['lng'], c1['lat']), (c2['lng'], c2['lat'])).m < r, axis=1)\
                             .sum(), axis=1)
    return grid_coords

for r in radius_list:
    google_engineered = find_given_radius(r, google_engineered, google_data, list(google_data['feature_name'].unique()))

google_engineered.to_csv('trial.csv')
