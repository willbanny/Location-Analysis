import os
import numpy as np

##################  VARIABLES  ##################
CLIENT_ID = os.environ.get("MB_ID")
CLIENT_SECRET = os.environ.get("MB_SECRET")

GCP_PROJECT = os.environ.get("GCP_PROJECT")
BQ_DATASET = os.environ.get("BQ_DATASET")
BQ_REGION = os.environ.get("BQ_REGION")
BQ_DISTRICT_TABLE = os.environ.get("BQ_DISTRICT_TABLE")

MASTER_COLUMN_NAMES_RAW = ["District",
    "HECTARES",
    "BR_Left",
    "BR_Top",
    "BR_Right",
    "BR_Bottom",
    "Centroid_Lon",
    "Centroid_Lat"]

MASTER_DTYPES_RAW = {
    "District": "object",
    "HECTARES": "float32",
    "BR_Left": "float32",
    "BR_Top": "float32",
    "BR_Right": "float32",
    "BR_Bottom": "float32",
    "Centroid_Lon": "float32",
    "Centroid_Lat": "float32"
}
