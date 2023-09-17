
import boto3
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from configparser import ConfigParser
from utils.helper import create_bucket, connect_to_dwh
from constants import db_tables
from sql_statements.create import raw_data_tables


config = ConfigParser()
config.read('.env')


bucket_name= config['AWS']['bucket_name']

region = config['AWS']['region']
access_key = config['AWS']['access_key']
secret_key = config['AWS']['secret_key']

host = config['DB_CRED']['host']
user = config['DB_CRED']['username']
password = config['DB_CRED']['password']
database = config['DB_CRED']['database']

dwh_host = config['DWH']['host']
dwh_user = config['DWH']['username']
dwh_password = config['DWH']['password']
dwh_database = config['DWH']['database']
role = config['DWH']['role']

#step 1 create a bucket using boto3
#create_bucket()


#step 2 Extract from database to data lake

# conn = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:5432/{database}')

s3_path = 's3://{}/{}.csv'


# for table in db_tables:
#     query = f'SELECT * FROM {table}'
#     df = pd.read_sql_query(query, conn)

#     df.to_csv(
#         s3_path.format(bucket_name, table)
#         , index=False
#         , storage_options={
#             'key': access_key
#             , 'secret': secret_key
#         }
#     )


#step 3 Create the Raw Schemas in DWH

conn_details = {
    'host' : dwh_host
    , 'user' : dwh_user
    , 'password' : dwh_password
    , 'database': dwh_database
}
conn = connect_to_dwh(conn_details)
print('conn successful')

cursor = conn.cursor()

#----Create the dev Schema

#create_dev_schema_query = 'CREATE SCHEMA raw_data;'
#cursor.execute(create_dev_schema_query)


# ----- Creating the raw tables
for query in raw_data_tables:
    print(f'=================== {query[:50]}')
    cursor.execute(query)

conn.commit()


schema = 'raw_data'
# -- copy from s3 to Redshift

for table in db_tables:
    query = f'''
        copy {schema}.{table}
        from '{s3_path.format(bucket_name, table)}'
        iam_role '{role}'
        delimiter ','
        ignoreheader 1;
    '''
    cursor.execute(query)
    conn.commit()