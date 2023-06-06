from google.cloud import bigquery
import pandas as pd
# from colorama import Fore, Style
from pathlib import Path
from macrobond.params import *

storage_filename = "console.cloud.google.com/bigquery?ws=!1m5!1m4!4m3!1slocation-analysis-389008!2sgrid_centroids1!3sgrid_centroids"


query = f"""
        SELECT {",".join(MASTER_COLUMN_NAMES_RAW)}
        FROM {GCP_PROJECT}.{BQ_DATASET}.{BQ_DISTRICT_TABLE}
        ORDER BY HECTARES DESC
    """

client = bigquery.Client(project=GCP_PROJECT)
query_job = client.query(query)
result = query_job.result()
df = result.to_dataframe()
print(df.head())


# SELECT
# master.District
# ,master.HECTARES
# ,master.Centroid_Lon
# ,master.Centroid_Lat
# ,master.BR_Left
# ,master.BR_Top
# ,BR_Right
# ,BR_Bottom
# ,Centroid_Lon
# ,Centroid_Lat
# FROM `location-analysis-389008.grid_centroids1.master_district_table` AS master
# ORDER BY master.HECTARES DESC
