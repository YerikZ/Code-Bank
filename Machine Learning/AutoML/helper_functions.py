
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

# Function to add prefix to a set of columns
def add_col_prefix(df, cols_to_update, prefix):
    for col in cols_to_update:
        df.rename(columns={col: prefix+col}, inplace=True)
    return df.copy()

# Function to create dummy features and contact with the original df
def create_dummy_features(df, cols_to_dummies):
    for col in cols_to_dummies:
        df = pd.concat([df.drop(columns=col), 
                        pd.get_dummies(df[col], prefix=col)], axis=1)
    return df.copy()

# function to create descriptive stats by group from a dataframe
def create_desc_stats(df, grp_col, col_func):
    # grp_col: column to be grouped
    # col_func: list of (columns to calculate, function to apply) e.g. [('colA', 'min'), ('colB', 'mean')
    df.fillna(0, inplace=True)
    temp_df = {}
    for i in range(len(col_func)):
        col = col_func[i][0]
        func = col_func[i][1]
        #print(col, func)
        temp_df[i] = df.groupby(grp_col)[[col]].__getattribute__(func)().reset_index()
        temp_df[i].rename(columns={col: col + '_' + func}, inplace=True)
    final_df = temp_df[0] # define a final_df to merge all the temp_df
    for j in range(len(temp_df)):
        if j > 0:
            final_df = pd.merge(final_df, temp_df[j], on=grp_col, how='inner')
    return final_df