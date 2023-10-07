"""
Downloads the csv file from the URL. Creates a new table in the Postgres server.
Reads the file as a dataframe and inserts each record to the Postgres table. 
"""
import logging
import pandas as pd
from connect_to_database import connect_to_postgres

conn = connect_to_postgres()

def write_to_postgres():
    """
    Create the dataframe and write to Postgres table if it doesn't already exist
    """
    df = pd.read_csv('./csv_files/churn_modelling.csv')
    
    df.to_sql(name='churn_modelling', con=conn, if_exists='replace', index=False)

    inserted_row_count = df.shape[0]
    logging.info(f' {inserted_row_count} rows from csv file inserted into churn_modelling table successfully')

if __name__ == '__main__':

    write_to_postgres()