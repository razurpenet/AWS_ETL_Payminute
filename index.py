
import boto3
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from configparser import ConfigParser


from utils.helper import create_bucket
from utils.helper import db_tables


config = ConfigParser()
config.read('.env')


bucket_name= config['AWS']['bucket_name']

region = config['AWS']['region']
access_key = config['AWS']['access_key']
secret_key = config['AWS']['secret_key']

host = config['AWS']['host']
user = config['AWS']['username']
password = config['AWS']['password']
database = config['AWS']['database']

#step 1 create a bucket using boto3
create_bucket()


#step 2 Extract from database to data lake

conn = create_engine('postgresql+psycopg2://{user}:{pasword}@{host}:5432/{database}')

s3_path = 's3://{}/{}.csv'


for table in db_tables:
    query = f'SELECT * FROM {table}'
    df = pd.read_sql_query(query, conn)

    df.to_csv(
        s3_path.format(bucket_name, table)
        , index=False
        , storage_options={
            'key': access_key
            , 'secret': secret_key
        }
    )



