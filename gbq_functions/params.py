import os
import numpy as np

##################  VARIABLES  ##################
GCP_PROJECT = os.environ.get("GCP_PROJECT")
BQ_DATASET = os.environ.get("BQ_DATASET")
BQ_REGION = os.environ.get("BQ_REGION")
BQ_DISTRICT_TABLE = os.environ.get("BQ_DISTRICT_TABLE")
BQ_GRID_TABLE = os.environ.get("BQ_DISTRICT_GRID_TABLE")
BQ_GOOGLE_TABLE = os.environ.get("BQ_GOOGLE_TABLE")
BQ_CRIME_TABLE = os.environ.get("BQ_CRIME_TABLE")
BQ_DEP_TABLE = os.environ.get("BQ_DEP_TABLE")

MASTER_COLUMN_NAMES_RAW = ["District",
    "HECTARES",
    "District_ID"
    "BR_Left",
    "BR_Top",
    "BR_Right",
    "BR_Bottom",
    "Centroid_Lon",
    "Centroid_Lat"]
MASTER_DTYPES_RAW = {
    "District": "object",
    "HECTARES": "float32",
    "District_ID": "object",
    "BR_Left": "float32",
    "BR_Top": "float32",
    "BR_Right": "float32",
    "BR_Bottom": "float32",
    "Centroid_Lon": "float32",
    "Centroid_Lat": "float32"
}

GRID_COLUMN_NAMES_RAW = ["District",
    "Description",
    "GridName",
    "Longitude",
    "Latitude"]
GRID_DTYPES_RAW = {
    "District": "object",
    "Description": "object",
    "GridName": "object",
    "Longitude": "float32",
    "Latitude": "float32"
}

GOOGLE_COLUMN_NAMES_RAW = ["lat",
    "lng",
    "feature_name",
    "district"]
GOOGLE_DTYPES_RAW = {
    "lat": "float32",
    "lng": "float32",
    "feature_name": "object",
    "district": "object"
}

CRIME_COLUMN_NAMES_RAW = ["LSOA_ID",
    "LSOA_name",
    "Crime_type",
    "Longitude",
    "Latitude",
    'Date',
    'Crime_ID',
    'District_Name',
    'District_ID']

CRIME_DTYPES_RAW = {
    "LSOA_ID": "object",
    "LSOA_name": "object",
    "Crime_type": "object",
    "Longitude": "float32",
    "Latitude": "float32",
    "Date": "object",
    "Crime_ID": "object",
    "District_Name": "object",
    "District_ID": "object"
}


DEP_COLUMN_NAMES_RAW = ["Local_Authority_District_code__2019_",
    "Local_Authority_District_name__2019_",
    "Index_of_Multiple_Deprivation__IMD__Score",
    "longitude",
    "latitude"]

DEP_DTYPES_RAW = {
    "Local_Authority_District_code__2019_": "object",
    "Local_Authority_District_name__2019_": "object",
    "Index_of_Multiple_Deprivation__IMD__Score": "float32",
    "longitude": "float32",
    "latitude": "float32"
}
