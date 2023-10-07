import logging
import traceback
import configparser
from sqlalchemy import create_engine

def connect_to_postgres():
    config = configparser.ConfigParser()
    config.read('config.ini')
    postgres_config = config['Postgres DB']

    postgres_host = postgres_config['postgres_host']
    postgres_database = postgres_config['postgres_database']
    postgres_user = postgres_config['postgres_user']
    postgres_password = postgres_config['postgres_password']

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s:%(funcName)s:%(levelname)s:%(message)s')

    try:
        # SQLAchemy connection
        engine_str = f'postgresql+psycopg2://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_database}'
        conn = create_engine(engine_str)
        logging.info('Postgres server connection is successful')
        return conn

    except Exception as e:
        traceback.print_exc()
        logging.error("Couldn't connect to Postgres")