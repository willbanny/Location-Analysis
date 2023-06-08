import pandas as pd
from gbq_functions.big_query_download import *

grid_coords = get_district_gridpoints_df('Wandsworth London Boro')
grid_coords.to_csv('grid_points_trial_bigQuery.csv')
