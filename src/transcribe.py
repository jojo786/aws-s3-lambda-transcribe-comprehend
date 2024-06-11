import json
import boto3
import os
import uuid

transcribe = boto3.client('transcribe')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Construct the S3 object URL
    s3_object_url = f"https://s3.amazonaws.com/{bucket}/{key}"

    # Generate a random string of digits
    random_digits = str(uuid.uuid4().int)[:8]

    # Transcribe the audio file
    transcribe_job_name = f"transcribe-job-{key.replace('/', '-')}-{random_digits}"
    transcribe.start_transcription_job(
        TranscriptionJobName=transcribe_job_name,
        Media={'MediaFileUri': s3_object_url},
        MediaFormat='mp3',  # Update with your audio file format
        LanguageCode='en-US',  # Update with your desired language code
        OutputBucketName=bucket,
        OutputKey="transcribe-output/"  # Update with your desired output key prefix
    )

    print(f'Transcription job {transcribe_job_name} started for {key}')
    
