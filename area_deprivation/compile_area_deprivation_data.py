import pandas as pd


deprivation_df = pd.read_csv('../raw_data/File_7_-_All_IoD2019_Scores__Ranks__Deciles_and_Population_Denominators_3.csv')
co_ordinates = pd.read_csv('../raw_data/lsoa_latlong.csv')


assert deprivation_df.isna().sum().sum() == 0
assert co_ordinates.isna().sum().sum() == 0


deprivation_df = deprivation_df.rename(columns={'LSOA code (2011)': 'lsoa11cd'})
deprivation_co_ordinates = pd.merge(deprivation_df, co_ordinates, how='inner', on='lsoa11cd')


deprivation_co_ordinates.to_csv('../raw_data/deprivation_lsoas_with_co_ordinates.csv')
