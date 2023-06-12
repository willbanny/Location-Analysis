import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import SelectPercentile, mutual_info_regression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler, OneHotEncoder, RobustScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier

from sklearn.decomposition import PCA


#list the features in the order of importance

def feature_listing_function(df, target_df):

    onehot_encoder = OneHotEncoder(sparse=False)
    encoded_target_array = onehot_encoder.fit_transform(target_df)
    encoded_target_df = pd.DataFrame(encoded_target_array, columns = onehot_encoder.get_feature_names_out())
    target_list = encoded_target_df.columns

    features = df.columns

    feature_importance_list = []

    for target in target_list:

        clf = RandomForestClassifier(random_state=1)
        clf.fit(df.values, encoded_target_df[target].values)

        # Index sort the most important features
        sorted_feature_weight_idxes = np.argsort(clf.feature_importances_)[::-1] # Reverse sort

        most_important_features = np.take_along_axis(
        np.array(df.iloc[:, 0: len(features) + 1].columns.tolist()),
        sorted_feature_weight_idxes, axis=0)
        most_important_weights = np.take_along_axis(
        np.array(clf.feature_importances_),
        sorted_feature_weight_idxes, axis=0)


        feature_importance_list.append(list(zip(most_important_features, most_important_weights)))


    flat_data = [item for sublist in feature_importance_list for item in sublist]
    index_data = {}
    for index, value in flat_data:
        if index not in index_data:
            index_data[index] = [value]
        else:
            index_data[index].append(value)
    df = pd.DataFrame(index_data)
    df = df.transpose()
    return df


