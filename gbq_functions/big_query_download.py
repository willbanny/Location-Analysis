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
    full_table_name = f"{GCP_PROJECT}.{BQ_DATASET}.{BQ_GOOGLE_TABLE}"
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
    full_table_name = f"{GCP_PROJECT}.{BQ_DATASET}.{BQ_GOLDEN_TABLE}"
    print(f"\nSave combined {district} data to BigQuery @ {full_table_name}...:")

    # Load data onto full_table_name

    client = bigquery.Client()

    write_mode = "WRITE_TRUNCATE" if truncate else "WRITE_APPEND"
    job_config = bigquery.LoadJobConfig(write_disposition=write_mode)

    job = client.load_table_from_dataframe(data, full_table_name, job_config=job_config)
    result = job.result()  # wait for the job to complete
    print(f"✅ Merged {district} Data saved to bigquery, with shape {data.shape}")


def get_golden_df(district:list):
    '''
    function that pulls the merged dataframe for data per district
    '''
    counter = 0
    london_districts = []

    if len(district) == 1:
        full_string = f'''SELECT District_ID FROM {GCP_PROJECT}.{BQ_DATASET}.{BQ_DISTRICT_TABLE} WHERE District = "{district[0]}"'''
    else:
        base_string = f'''SELECT District_ID FROM {GCP_PROJECT}.{BQ_DATASET}.{BQ_DISTRICT_TABLE}'''
        for dist in district:
            if counter == 0:
                query_string = f'''{base_string} WHERE District = "{dist}" OR'''

                counter += 1
                london_districts.append(query_string)
            else:
                query_string = f'''District = "{dist}" OR'''

                counter += 1
                london_districts.append(query_string)
        full_string = ' '.join(london_districts)[:-3]

    query1 = full_string

    district_id_df = bigquery.Client(project=GCP_PROJECT).query(query1).result().to_dataframe()
    district_id = district_id_df.iloc[0]['District_ID']


    or_strings = []
    counter = 0
    for i, row in district_id_df.iterrows():
        if counter == 0:
            f_string_output = f'WHERE {BQ_GOLDEN_TABLE}.Local_Authority_District_code__2019_ = "{row["District_ID"]}" OR'
            counter += 1
            or_strings.append(f_string_output)
        else:
            f_string_output = f'{BQ_GOLDEN_TABLE}.Local_Authority_District_code__2019_ = "{row["District_ID"]}" OR'
            counter += 1
            or_strings.append(f_string_output)

    full_or_string = ' '.join(or_strings)[:-3]


    query2 = f"""
            SELECT DISTINCT *
            FROM {GCP_PROJECT}.{BQ_DATASET}.{BQ_GOLDEN_TABLE}
            {full_or_string}
        """

    client = bigquery.Client(project=GCP_PROJECT)
    query_job = client.query(query2)
    result = query_job.result()
    golden_df = result.to_dataframe()
    return golden_df

def upload_carehome_df(data: pd.DataFrame,
                              truncate=False):
    '''
    Upload the dataframe of the merged crime, google, and deprivation stats to GBQ.
    '''

    assert isinstance(data, pd.DataFrame)
    full_table_name = f"{GCP_PROJECT}.{BQ_DATASET}.{BQ_CAREHOME_X_TABLE}"
    print(f"\nSave all carehome X data to BigQuery @ {full_table_name}...:")

    # Load data onto full_table_name

    client = bigquery.Client()

    write_mode = "WRITE_TRUNCATE" if truncate else "WRITE_APPEND"
    job_config = bigquery.LoadJobConfig(write_disposition=write_mode)

    job = client.load_table_from_dataframe(data, full_table_name, job_config=job_config)
    result = job.result()  # wait for the job to complete
    print(f"✅ Uploaded carehome X dataset to GBQ with shape {data.shape}")


def get_carehome_X_df(district:list):
    '''
    function that pulls the merged dataframe for data per district
    '''
    counter = 0
    london_districts = []

    if len(district) == 1:
        full_string = f'''SELECT District_ID FROM {GCP_PROJECT}.{BQ_DATASET}.{BQ_DISTRICT_TABLE} WHERE District = "{district[0]}"'''
    else:
        base_string = f'''SELECT District_ID FROM {GCP_PROJECT}.{BQ_DATASET}.{BQ_DISTRICT_TABLE}'''
        for dist in district:
            if counter == 0:
                query_string = f'''{base_string} WHERE District = "{dist}" OR'''

                counter += 1
                london_districts.append(query_string)
            else:
                query_string = f'''District = "{dist}" OR'''

                counter += 1
                london_districts.append(query_string)
        full_string = ' '.join(london_districts)[:-3]

    query1 = full_string

    district_id_df = bigquery.Client(project=GCP_PROJECT).query(query1).result().to_dataframe()
    district_id = district_id_df.iloc[0]['District_ID']


    or_strings = []
    counter = 0
    for i, row in district_id_df.iterrows():
        if counter == 0:
            f_string_output = f'WHERE {BQ_CAREHOME_X_TABLE}.district_code = "{row["District_ID"]}" OR'
            counter += 1
            or_strings.append(f_string_output)
        else:
            f_string_output = f'{BQ_CAREHOME_X_TABLE}.district_code = "{row["District_ID"]}" OR'
            counter += 1
            or_strings.append(f_string_output)

    full_or_string = ' '.join(or_strings)[:-3]


    query2 = f"""
            SELECT DISTINCT *
            FROM {GCP_PROJECT}.{BQ_DATASET}.{BQ_CAREHOME_X_TABLE}
            {full_or_string}
        """

    client = bigquery.Client(project=GCP_PROJECT)
    query_job = client.query(query2)
    result = query_job.result()
    carehome_df = result.to_dataframe()
    return carehome_df

def get_all_golden_df():
    query2 = f"""
        SELECT DISTINCT *
        FROM {GCP_PROJECT}.{BQ_DATASET}.{BQ_GOLDEN_TABLE}
    """

    client = bigquery.Client(project=GCP_PROJECT)
    query_job = client.query(query2)
    result = query_job.result()
    all_golden_df = result.to_dataframe()
    return all_golden_df
