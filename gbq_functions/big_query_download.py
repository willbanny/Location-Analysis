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
    a specified district, filtering out any duplicate values from prior uploads'''

    query = f"""
            SELECT DISTINCT {",".join(GOOGLE_COLUMN_NAMES_RAW)}
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
            WHERE District = "{district}"'''

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
            WHERE District = "{district}"'''

    district_id_df = bigquery.Client(project=GCP_PROJECT).query(query1).result().to_dataframe()
    district_id = district_id_df.iloc[0]['District_ID']

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


def upload_google_api_outputs(district:str,
                              data: pd.DataFrame,
                              truncate=False):
    '''
    Save output of google_api call to BigQuery, appending new data to existing dataset
    inputs required: district name and a pd.dataframe from google api call.
    '''

    assert isinstance(data, pd.DataFrame)
    full_table_name = f"{GCP_PROJECT}.{BQ_DATASET}.google_api_data"
    print(f"\nSave {district} data to BigQuery @ {full_table_name}...:")

    # Load data onto full_table_name

    client = bigquery.Client()

    write_mode = "WRITE_TRUNCATE" if truncate else "WRITE_APPEND"
    job_config = bigquery.LoadJobConfig(write_disposition=write_mode)

    job = client.load_table_from_dataframe(data, full_table_name, job_config=job_config)
    result = job.result()  # wait for the job to complete
    print(f"✅ {district} Data saved to bigquery, with shape {data.shape}")


def upload_golden_df(district:str,
                              data: pd.DataFrame,
                              truncate=False):
    '''
    Upload the dataframe of the merged crime, google, and deprivation stats to GBQ.
    '''

    assert isinstance(data, pd.DataFrame)
    full_table_name = f"{GCP_PROJECT}.{BQ_DATASET}.full_merged_data"
    print(f"\nSave combined {district} data to BigQuery @ {full_table_name}...:")

    # Load data onto full_table_name

    client = bigquery.Client()

    write_mode = "WRITE_TRUNCATE" if truncate else "WRITE_APPEND"
    job_config = bigquery.LoadJobConfig(write_disposition=write_mode)

    job = client.load_table_from_dataframe(data, full_table_name, job_config=job_config)
    result = job.result()  # wait for the job to complete
    print(f"✅ Merged {district} Data saved to bigquery, with shape {data.shape}")
