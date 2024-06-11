import json
import boto3
import os
import uuid

comprehend = boto3.client('comprehend')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Construct the S3 object URL
    s3_object_url = f"s3://{bucket}/{key}"

    # Generate a random string of digits
    random_digits = str(uuid.uuid4().int)[:8]

    # Start a sentiment analysis job
    sentiment_job_name = f"sentiment-analysis-job-{key.replace('/', '-')}-{random_digits}"
    comprehend.start_sentiment_detection_job(
        JobName=sentiment_job_name,
        LanguageCode='en',  # Update with your desired language code
        DataAccessRoleArn='arn:aws:iam::718974227478:role/ComprehendRole',  # Replace with your Comprehend role ARN
        InputDataConfig={
            'S3Uri': s3_object_url,
            'InputFormat': 'ONE_DOC_PER_FILE'
        },
        OutputDataConfig={
            'S3Uri': f"s3://{bucket}/comprehend-output/"
        }
    )

   
    
