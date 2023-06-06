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
    '''function that finds the district ID from master table
    based on specified district, and then returns a dataframe of all the crime stats for
    that district_ID'''
    query1 = f'''
            SELECT District_ID
            FROM {GCP_PROJECT}.{BQ_DATASET}.{BQ_DISTRICT_TABLE}
            WHERE District = {district}'''

    district_id_df = bigquery.Client(project=GCP_PROJECT).query(query1).result().to_dataframe()
    district_id = district_id_df.iloc[0]['District_ID']

    query2 = f"""
            SELECT {",".join(CRIME_COLUMN_NAMES_RAW)}
            FROM {GCP_PROJECT}.{BQ_DATASET}.{BQ_CRIME_TABLE}
            WHERE {BQ_CRIME_TABLE}.District_ID = "{district_id}"
        """

    client = bigquery.Client(project=GCP_PROJECT)
    query_job = client.query(query2)
    result = query_job.result()
    crime_df = result.to_dataframe()
    return crime_df


def get_deprivation_df(district):
    '''function that finds the district ID from master table
    based on specified district, and then returns a dataframe of all the crime stats for
    that district_ID'''
    query1 = f'''
            SELECT District_ID
            FROM {GCP_PROJECT}.{BQ_DATASET}.{BQ_DISTRICT_TABLE}
            WHERE District = {district}'''

    district_id_df = bigquery.Client(project=GCP_PROJECT).query(query1).result().to_dataframe()
    district_id = district_id_df.iloc[0]['Local_Authority_District_code__2019_']

    query2 = f"""
            SELECT {",".join(DEP_COLUMN_NAMES_RAW)}
            FROM {GCP_PROJECT}.{BQ_DATASET}.{BQ_DEP_TABLE}
            WHERE {BQ_DEP_TABLE}.Local_Authority_District_code__2019_ = "{district_id}"
        """

    client = bigquery.Client(project=GCP_PROJECT)
    query_job = client.query(query2)
    result = query_job.result()
    dep_df = result.to_dataframe()
    return dep_df
