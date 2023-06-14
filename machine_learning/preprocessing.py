import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import os

from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import SelectPercentile, mutual_info_regression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler, OneHotEncoder, RobustScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from crime_features import crime_features
from gbq_functions.big_query_download import *


# Feature Selection

#Load Golden DF
#Change FilePath

local_golden_df = pd.read_csv("/home/mih_sud/code/willbanny/Location-Analysis/raw_data/London_Data_Expanded_1.csv")

# Preprocess and select features
local_golden_df = local_golden_df.fillna(0)

dirty_city_features = local_golden_df.columns

city_features = []

for feature in dirty_city_features:
    if "250" in feature:
        city_features.append(feature)
    elif "500" in feature:
        city_features.append(feature)
    elif "750" in feature:
        city_features.append(feature)
    elif "100" in feature:
        city_features.append(feature)
    elif "1000" in feature:
        city_features.append(feature)
    elif "1250" in feature:
        city_features.append(feature)
    elif "1500" in feature:
        city_features.append(feature)
    elif "Score" in feature:
        if "1" not in feature:
            city_features.append(feature)


#Create a DataFrame which will be scaled

to_scale_df = pd.DataFrame()
for feature in city_features:
    to_scale_df[feature] = local_golden_df[feature]


#Scaling

#MinMax Scale the DataFrame

mm_scaler = MinMaxScaler()
mm_scaler.fit(to_scale_df)
mm_scaled_df = pd.DataFrame(mm_scaler.transform(to_scale_df), columns=city_features)

#Robust Scale the DataFrame

r_scaler = RobustScaler()
r_scaler.fit(to_scale_df)
r_scaled_df = pd.DataFrame(r_scaler.transform(to_scale_df), columns=city_features)


#Crimeless selection
crimeless_features = list(set(city_features) - set(crime_features))


mm_crimeless_non_PCA_df = pd.DataFrame()
r_crimeless_non_PCA_df = pd.DataFrame()

for feature in crimeless_features:

    r_crimeless_non_PCA_df[feature] = r_scaled_df[feature]
    mm_crimeless_non_PCA_df[feature] = mm_scaled_df[feature]


#PCA

#MinMax Crime PCA

mm_pca = PCA()
mm_pca.fit(mm_scaled_df)

mm_proj = mm_pca.transform(mm_scaled_df)
mm_proj = pd.DataFrame(mm_proj, columns=[f'PC{i}' for i in range(1, len(city_features) + 1)])

#MinMax Crimeless PCA

mm_crimeless_pca = PCA()
mm_crimeless_pca.fit(mm_crimeless_non_PCA_df)

mm_crimeless_proj = mm_crimeless_pca.transform(mm_crimeless_non_PCA_df)
mm_crimeless_proj = pd.DataFrame(mm_crimeless_proj, columns=[f'PC{i}' for i in range(1, len(crimeless_features) + 1)])

#Robust Crime PCA

r_pca = PCA()
r_pca.fit(r_scaled_df)

r_proj = r_pca.transform(r_scaled_df)
r_proj = pd.DataFrame(r_proj, columns=[f'PC{i}' for i in range(1, len(city_features )+ 1)])

#MinMax Crimeless PCA

r_crimeless_pca = PCA()
r_crimeless_pca.fit(r_crimeless_non_PCA_df)

r_crimeless_proj = r_crimeless_pca.transform(r_crimeless_non_PCA_df)
r_crimeless_proj = pd.DataFrame(r_crimeless_proj, columns=[f'PC{i}' for i in range(1, len(crimeless_features) + 1)])


#Care home selection

england_care_home_df = pd.read_csv('raw_data/carehome_locations.csv')

#Only store those that fit the golden df dimensions

care_home_local_df = england_care_home_df[england_care_home_df["latitude"] <= local_golden_df["lat"].max()]
care_home_local_df = care_home_local_df[care_home_local_df["latitude"] >= local_golden_df["lat"].min() ]
care_home_local_df = care_home_local_df[care_home_local_df["longitude"] >= local_golden_df["lng"].min() ]
care_home_local_df = care_home_local_df[care_home_local_df["longitude"] <= local_golden_df["lng"].max() ]

#K-Means

#MinMax Crime K-means PCA

mm_crime_pca_km = KMeans(n_clusters= 3)
mm_crime_pca_km.fit(mm_proj)

#MinMax Crimeless K-means PCA

mm_crimeless_pca_km = KMeans(n_clusters= 3)
mm_crimeless_pca_km.fit(mm_crimeless_proj)

#Robust Crime K-means PCA

r_crime_pca_km = KMeans(n_clusters= 3)
r_crime_pca_km.fit(r_proj)

#Robust Crimeless K-means PCA

r_crimeless_pca_km = KMeans(n_clusters= 3)
r_crimeless_pca_km.fit(mm_crimeless_proj)




#MinMax Crime K-means Non_PCA

mm_crime_non_pca_km = KMeans(n_clusters= 3)
mm_crime_non_pca_km.fit(mm_scaled_df)

#MinMax Crimeless K-means Non_PCA

mm_crimeless_non_pca_km = KMeans(n_clusters= 3)
mm_crimeless_non_pca_km.fit(mm_crimeless_non_PCA_df)

#Robust Crime K-means Non_PCA

r_crime_non_pca_km = KMeans(n_clusters= 3)
r_crime_non_pca_km.fit(r_scaled_df)

#Robust Crimeless K-means Non_PCA

r_crimeless_non_pca_km = KMeans(n_clusters= 3)
r_crimeless_non_pca_km.fit(r_crimeless_non_PCA_df)


#Export df


export_df = local_golden_df[["lng","lat"]].copy()

export_df["MinMax_PCA_Crime_Labels"] = mm_crime_pca_km.labels_
export_df["Robust_PCA_Crime_Labels"] = r_crime_pca_km.labels_
export_df["MinMax_PCA_Crimeless_Labels"] = mm_crimeless_pca_km.labels_
export_df["Robust_PCA_Crimeless_Labels"] = r_crimeless_pca_km.labels_

export_df["MinMax_Non_PCA_Crime_Labels"] = mm_crime_non_pca_km.labels_
export_df["Robust__Non_PCA_Crime_Labels"] = r_crime_non_pca_km.labels_
export_df["MinMax_Non_PCA_Crimeless_Labels"] = mm_crimeless_non_pca_km.labels_
export_df["Robust__Non_PCA_Crimeless_Labels"] = r_crimeless_non_pca_km.labels_


#Change File_Path
export_df.to_csv('outputs/model_output_labels.csv')
