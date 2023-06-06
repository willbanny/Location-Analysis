from google.cloud import bigquery
import pandas as pd
from gbq_functions.params import *

def get_master_district_df():
    '''function that returns the full master district df.
    Dataframe contains district name (primary key), lat_lons for the center,
    lat_lons for the edges of rectangle around area, and the area of the
    rectangle in Hectares'''

    query = f"""
            SELECT {",".join(MASTER_COLUMN_NAMES_RAW)}
            FROM {GCP_PROJECT}.{BQ_DATASET}.{BQ_DISTRICT_TABLE}
            ORDER BY HECTARES DESC
        """

    client = bigquery.Client(project=GCP_PROJECT)
    query_job = client.query(query)
    result = query_job.result()
    master_districts_df = result.to_dataframe()
    return master_districts_df

def get_district_gridpoints_df(district):
    '''function that returns a dataframe of all the grid point coordinates
    for a specified district'''

    query = f"""
            SELECT {",".join(GRID_COLUMN_NAMES_RAW)}
            FROM {GCP_PROJECT}.{BQ_DATASET}.{BQ_GRID_TABLE}
            WHERE {BQ_GRID_TABLE}.District = "{district}"
        """

    client = bigquery.Client(project=GCP_PROJECT)
    query_job = client.query(query)
    result = query_job.result()
    district_grid_df = result.to_dataframe()
    return district_grid_df


def get_google_df(district):
    '''function that returns a dataframe of all the google features for
    a specified district'''

    query = f"""
            SELECT {",".join(GOOGLE_COLUMN_NAMES_RAW)}
            FROM {GCP_PROJECT}.{BQ_DATASET}.{BQ_GOOGLE_TABLE}
            WHERE {BQ_GOOGLE_TABLE}.district = "{district}"
        """

    client = bigquery.Client(project=GCP_PROJECT)
    query_job = client.query(query)
    result = query_job.result()
    google_df = result.to_dataframe()
    return google_df


def get_crime_df(district):
    '''function that returns a dataframe of all the crime stats for
    a specified district'''
