## Information

![image](./img/overview.png)


```bash
pip install -r python_scripts/requirements.txt
```

## Steps

`write_csv_to_postgres.py`-> reads a csv file from local repository and writes it writes it to a table in a local PostgreSQL instance.

`create_df_and_modify.py` -> reads the same Postgres table and creates a pandas dataframe out of it, modifies it. Then, creates 3 separate dataframes.

`write_df_to_postgres.py` -> writes these 3 dataframes to 3 separate tables located on the same Postgres database.



## Apache Airflow:

Run the following command to clone the necessary repo on your local

```bash
git clone https://github.com/dogukannulu/docker-airflow.git
```
After cloning the repo, run the following command only once:

```bash
docker build --rm --build-arg AIRFLOW_DEPS="datadog,dask" --build-arg PYTHON_DEPS="flask_oauthlib>=0.9" -t puckel/docker-airflow .
```

Then run the following command:

```bash
docker-compose -f docker-compose-LocalExecutor.yml up -d
```

Now you have a running Airflow container and you can reach out to that on `https://localhost:8080`. If there is `No module: ...` error, you can access to bash with the following command:

```bash
docker exec -it <container_id> /bin/bash 
```

Then:
```bash
pip install <necessary libraries>
```

After all these, we can move all .py files under dags folder in docker-airflow repo.

## PostgreSQL

I am using a local Postgres Server and installed `PgAdmin` to control the tables instead of using `psql`.