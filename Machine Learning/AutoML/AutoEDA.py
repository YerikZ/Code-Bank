import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression, \
chi2, f_regression, f_classif
import warnings
warnings.filterwarnings('ignore')


def create_desc_stats(df):
    try:
        stats_df = {}
        # data types
        stats_df['dtype'] = df.dtypes.reset_index()
        stats_df['dtype'] .columns = ['features', 'dtype']
        # count
        stats_df['count'] = df.count().reset_index()
        stats_df['count'] .columns = ['features', 'count']
        # num of missing values
        stats_df['NA'] = np.round(df.isna().sum() / df.shape[0], 4)
        stats_df['NA'] = stats_df['NA'].reset_index() 
        stats_df['NA'].columns = ['features', 'NA%']
        # num of unique values
        stats_df['nunique'] = df.nunique().reset_index()
        stats_df['nunique'] .columns = ['features', 'nunique']
        # min
        stats_df['min'] = df.min().reset_index()
        stats_df['min'] .columns = ['features', 'min']
        # mean
        stats_df['mean'] = df.mean().reset_index()
        stats_df['mean'] .columns = ['features', 'mean']
        # std
        stats_df['std'] = df.std().reset_index()
        stats_df['std'] .columns = ['features', 'std']
        # median
        stats_df['median'] = df.median().reset_index()
        stats_df['median'] .columns = ['features', 'median']
        # max
        stats_df['max'] = df.max().reset_index()
        stats_df['max'] .columns = ['features', 'max']
        
        final_df = stats_df['dtype']
        for key in stats_df.keys():
            if key != 'dtype':
                final_df = pd.merge(final_df, stats_df[key], on='features', how='left')
    except Exception as e:
        print('Error:', str(e))
    return final_df

def create_feature_target_charts(df, target, n_bin=20, figsize=(12,4)):
    for col in df.columns:
        try:
            if col == target:
                temp_df = df[[col]]
            else:
                temp_df = df[[col, target]]
            
            # col is a UID
            if temp_df[col].nunique() == temp_df.shape[0]:
                print(col, 'is an ID column.')
                continue
            # number of unique values > n_bin, create n_bin bins
            elif temp_df[col].nunique() > n_bin:
                temp_df['bin']=pd.cut(df[col], n_bin)
            else:
                temp_df['bin']=df[col]
            chart_df = temp_df.groupby('bin')[[target]].mean().reset_index()
            chart_df['count'] = temp_df.groupby('bin')[[target]].count().reset_index()[target]
            plt.figure(figsize=figsize)
            ax = sns.barplot(x=chart_df['bin'], y=chart_df['count'])
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            ax2 = plt.twinx()
            sns.lineplot(data=chart_df[target], ax=ax2)
            ax.set_xlabel(col)
            ax2.set_ylabel(target)
            
            # label the % of each bar
            labels = list(chart_df['count']/chart_df['count'].sum())
            for (i, label) in zip(ax.patches, labels):
                ax.text(i.get_x() + i.get_width()/2-.03, i.get_height(), \
                    str(int(round(label*100,0)))+'%', fontsize=9)
            plt.show()
        except Exception as e:
            print('Error', col, str(e))
            continue

def create_feature_association_table(df, target, model_type, categorical_cutoff=20):
    # model_type: reg or clf
    
    col_num = [] # numeric features
    col_cat = [] # categorical features
    col_text = [] # text features
    features = [target] + list(df.columns[df.columns!=target])
    
    for col in df.columns:
        # col is a UID or target
        if (df[col].nunique() == df.shape[0]) or col == target:
            continue
        elif df[col].dtype == np.float:
            col_num.append(col)
        elif df[col].dtype == np.int:
            # number of unique values <= categorical_cutoff, assume categorical
            if df[col].nunique() <= categorical_cutoff:
                col_cat.append(col)
            else:
                col_num.append(col)
        else:
            col_text.append(col)
    
    df_corr = df.corr()[target].reset_index() #pearson correlation
    df_corr.columns = ['features', 'correlation']
    
    try:
        if model_type == 'clf':
            # mutual information
            mi = mutual_info_classif(X=df[col_cat + col_num], 
                                     y=df[target], 
                                     discrete_features=[True for i in range(len(col_cat))] + \
                                    [False for i in range(len(col_num))]
                                    )
            # avova
            f_val, f_pval = f_classif(X=df[col_cat + col_num], y=df[target])
        else:
            # mutual information
            mi = mutual_info_regression(X=df[col_cat + col_num], 
                                     y=df[target], 
                                     discrete_features=[True for i in range(len(col_cat))] + \
                                    [False for i in range(len(col_num))]
                                    )
            # avova
            f_val, f_pval = f_regression(X=df[col_cat + col_num], y=df[target])

        # chi2
        # get non-negative categorical variable
        col_chi2 = [col for col in col_cat if sum(df[col]<0) == 0]
        chi2_val, chi2_pval = chi2(X=df[col_chi2], y=df[target])

        df_mi = pd.DataFrame({'features': col_cat + col_num, 'mutual_info': mi})
        df_fval = pd.DataFrame({'features': col_cat + col_num,
                                'f_value': f_val,
                                'f_pval': f_pval
                               })
        df_chi2 = pd.DataFrame({'features': col_chi2,
                                'chi2_val': chi2_val,
                                'chi2_pval': chi2_pval
                               })


        final_df = pd.merge(pd.merge(pd.merge(df_corr, df_mi, on='features', how='outer'),
                           df_fval, on='features', how='outer'),
                            df_chi2, on='features', how='outer')
        final_df = pd.concat([final_df.tail(1), final_df.head(-1)], axis=0).reset_index(drop=True)
        return np.round(final_df, 4)
    except Exception as e:
        print('ERROR:', str(e))