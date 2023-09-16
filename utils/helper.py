import boto3

region = 'eu-west-1'
bucket_name= 'payminute344'
access_key = 'AKIAYBXRAS5VKZE5TTKY'
secret_key = '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'


def create_bucket():    
    client = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,

    )

    client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': region
        }
    )