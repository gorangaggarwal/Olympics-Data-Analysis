import pandas as pd

def preprocess(olympics_df,region_df):
    olympics_df = olympics_df[olympics_df['Season'] == 'Summer']
    olympics_df = olympics_df.merge(region_df, on='NOC', how='left')
    olympics_df = olympics_df.drop_duplicates(inplace=False)
    olympics_df = pd.concat([olympics_df, pd.get_dummies(olympics_df['Medal']).astype('int')], axis=1)
    return olympics_df