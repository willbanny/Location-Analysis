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
BQ_GOLDEN_TABLE = os.environ.get("BQ_GOLDEN_TABLE")
BQ_CAREHOME_X_TABLE = os.environ.get("BQ_CAREHOME_X_TABLE")

MASTER_COLUMN_NAMES_RAW = ["District",
    "HECTARES",
    "District_ID",
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
DEP_COLUMN_NAMES_RAW = ['lsoa11cd',
                        "Local_Authority_District_code__2019_",
    "Local_Authority_District_name__2019_",
    "Index_of_Multiple_Deprivation__IMD__Score",
    "Index_of_Multiple_Deprivation__IMD__Rank__where_1_is_most_deprived_",
    'Index_of_Multiple_Deprivation__IMD__Score',
'    Index_of_Multiple_Deprivation__IMD__Rank__where_1_is_most_deprived_',
    'Index_of_Multiple_Deprivation__IMD__Decile__where_1_is_most_deprived_10__of_LSOAs_',
    'Income_Score__rate_',
    'Income_Rank__where_1_is_most_deprived_',
    'Income_Decile__where_1_is_most_deprived_10__of_LSOAs_',
    'Employment_Score__rate_',
    'Employment_Rank__where_1_is_most_deprived_',
    'Employment_Decile__where_1_is_most_deprived_10__of_LSOAs_',
    'Education__Skills_and_Training_Score',
    'Education__Skills_and_Training_Rank__where_1_is_most_deprived_',
    'Education__Skills_and_Training_Decile__where_1_is_most_deprived_10__of_LSOAs_',
    'Health_Deprivation_and_Disability_Score',
    'Health_Deprivation_and_Disability_Rank__where_1_is_most_deprived_',
    'Health_Deprivation_and_Disability_Decile__where_1_is_most_deprived_10__of_LSOAs_',
    'Crime_Score',
    'Crime_Rank__where_1_is_most_deprived_',
    'Crime_Decile__where_1_is_most_deprived_10__of_LSOAs_',
    'Barriers_to_Housing_and_Services_Score',
    'Barriers_to_Housing_and_Services_Rank__where_1_is_most_deprived_',
    'Barriers_to_Housing_and_Services_Decile__where_1_is_most_deprived_10__of_LSOAs_',
    'Living_Environment_Score',
    'Living_Environment_Rank__where_1_is_most_deprived_',
    'Living_Environment_Decile__where_1_is_most_deprived_10__of_LSOAs_',
    'Income_Deprivation_Affecting_Children_Index__IDACI__Score__rate_',
    'Income_Deprivation_Affecting_Children_Index__IDACI__Rank__where_1_is_most_deprived_',
    'Income_Deprivation_Affecting_Children_Index__IDACI__Decile__where_1_is_most_deprived_10__of_LSOAs_',
    'Income_Deprivation_Affecting_Older_People__IDAOPI__Score__rate_',
    'Income_Deprivation_Affecting_Older_People__IDAOPI__Rank__where_1_is_most_deprived_',
    'Income_Deprivation_Affecting_Older_People__IDAOPI__Decile__where_1_is_most_deprived_10__of_LSOAs_',
    'Children_and_Young_People_Sub_domain_Score',
    'Children_and_Young_People_Sub_domain_Rank__where_1_is_most_deprived_',
    'Children_and_Young_People_Sub_domain_Decile__where_1_is_most_deprived_10__of_LSOAs_',
    'Adult_Skills_Sub_domain_Score',
    'Adult_Skills_Sub_domain_Rank__where_1_is_most_deprived_',
    'Adult_Skills_Sub_domain_Decile__where_1_is_most_deprived_10__of_LSOAs_',
    'Geographical_Barriers_Sub_domain_Score',
    'Geographical_Barriers_Sub_domain_Rank__where_1_is_most_deprived_',
    'Geographical_Barriers_Sub_domain_Decile__where_1_is_most_deprived_10__of_LSOAs_',
    'Wider_Barriers_Sub_domain_Score',
    'Wider_Barriers_Sub_domain_Rank__where_1_is_most_deprived_',
    'Wider_Barriers_Sub_domain_Decile__where_1_is_most_deprived_10__of_LSOAs_',
    'Indoors_Sub_domain_Score',
    'Indoors_Sub_domain_Rank__where_1_is_most_deprived_',
    'Indoors_Sub_domain_Decile__where_1_is_most_deprived_10__of_LSOAs_',
    'Outdoors_Sub_domain_Score',
    'Outdoors_Sub_domain_Rank__where_1_is_most_deprived_',
    'Outdoors_Sub_domain_Decile__where_1_is_most_deprived_10__of_LSOAs_',
    'Total_population__mid_2015__excluding_prisoners_',
    'Dependent_Children_aged_0_15__mid_2015__excluding_prisoners_',
    'Population_aged_16_59__mid_2015__excluding_prisoners_',
    'Older_population_aged_60_and_over__mid_2015__excluding_prisoners_',
    'Working_age_population_18_59_64__for_use_with_Employment_Deprivation_Domain__excluding_prisoners__',
    "longitude",
    "latitude"]
DEP_DTYPES_RAW = {
    "Local_Authority_District_code__2019_": "object",
    "Local_Authority_District_name__2019_": "object",
    "Index_of_Multiple_Deprivation__IMD__Score": "float32",
    "longitude": "float32",
    "latitude": "float32"
}
