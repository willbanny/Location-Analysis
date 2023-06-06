# imports
import pandas as pd
import numpy as np
import macrobond_data_api as mda
from macrobond_data_api.web import WebClient
from macrobond.params import *


client_id = CLIENT_ID
client_secret = CLIENT_SECRET

with WebClient(client_id, client_secret) as api:
    series = api.get_unified_series("gblama10086","gblama10085", 'gblama10087', 'gblama10088', 'gblama10089').to_pd_data_frame()

series_df = (series)
print(series_df)
