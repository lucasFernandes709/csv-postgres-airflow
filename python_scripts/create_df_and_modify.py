"""
Creates a base dataframe out of churn_modelling table and creates 3 separate dataframes out of it.
"""
import numpy as np
import pandas as pd

def create_base_df(conn):
    """
    Base dataframe of churn_modelling table
    """
    df = pd.read_sql_table('churn_modelling', con=conn)

    df.drop('RowNumber', axis=1, inplace=True)
    index_to_be_null = np.random.randint(10000, size=30)
    df.loc[index_to_be_null, ['Balance', 'CreditScore', 'Geography']] = np.nan
    
    most_occured_country = df['Geography'].value_counts().index[0]
    df['Geography'].fillna(value=most_occured_country, inplace=True)
    
    avg_balance = df['Balance'].mean()
    df['Balance'].fillna(value=avg_balance, inplace=True)

    median_creditscore = df['CreditScore'].median()
    df['CreditScore'].fillna(value=median_creditscore, inplace=True)

    return df


def create_creditscore_df(df):
    
    cols_to_select = ['Geography', 'Gender', 'Exited', 'CreditScore']
    df_creditscore = (
        df
        .reindex(columns=cols_to_select)
        .groupby(['Geography', 'Gender'])
        .agg({'CreditScore': 'mean', 'Exited': 'sum'})
        .rename(columns={'Exited': 'total_exited', 'CreditScore': 'avg_credit_score'})
        .reset_index()
        .sort_values('avg_credit_score')
    )

    return df_creditscore


def create_exited_age_correlation(df):

    df_exited_age_correlation = (
        df
        .groupby(['Geography', 'Gender', 'Exited'])
        .agg({
            'Age': 'mean',
            'EstimatedSalary': 'mean',
            'Exited': 'count'
        })
        .rename(columns={
            'Age': 'avg_age',
            'EstimatedSalary': 'avg_salary',
            'Exited': 'number_of_exited_or_not'
        })
        .reset_index()
        .sort_values('number_of_exited_or_not')
    )

    return df_exited_age_correlation


def create_exited_salary_correlation(df):

    cols_to_select = 'Geography','Gender','Exited','EstimatedSalary'
    df_salary = (
        df
        .reindex(columns=cols_to_select)
        .groupby(['Geography', 'Gender'])
        .agg({'EstimatedSalary': 'mean'})
        .sort_values('EstimatedSalary')
        .reset_index()
    )

    min_salary = round(df_salary['EstimatedSalary'].min(), 0)

    df['is_greater'] = df['EstimatedSalary'].apply(lambda x: 1 if x > min_salary else 0)

    df_exited_salary_correlation = pd.DataFrame({
        'Exited': df['Exited'],
        'is_greater': df['EstimatedSalary'] > df['EstimatedSalary'].min(),
        'correlation': np.where(df['Exited'] == (df['EstimatedSalary'] > df['EstimatedSalary'].min()), 1, 0)
    })

    return df_exited_salary_correlation