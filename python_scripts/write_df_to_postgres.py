import logging
import pandas as pd
from connect_to_database import connect_to_postgres
from create_df_and_modify import create_base_df, create_creditscore_df, create_exited_age_correlation, create_exited_salary_correlation

conn = connect_to_postgres()

def write_table_to_postgres(df: pd.DataFrame, table: str, conn: str):
    
    df.to_sql(name=table, con=conn, if_exists='replace', index=False)
    inserted_row_count = df.shape[0]
    logging.info(f' {inserted_row_count} rows from csv file inserted into {table} table successfully')


if __name__ == '__main__':

    main_df = create_base_df(conn)
    df_creditscore = create_creditscore_df(main_df)
    df_exited_age_correlation = create_exited_age_correlation(main_df)
    df_exited_salary_correlation = create_exited_salary_correlation(main_df)

    df_dict = {
        'creditscore': df_creditscore,
        'exited_age_correlation': df_exited_age_correlation,
        'exited_salary_correlation': df_exited_salary_correlation
    }

    for df in df_dict:
        write_table_to_postgres(df_dict[df], df, conn) 
