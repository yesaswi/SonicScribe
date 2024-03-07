import os
from google.cloud import storage
from openai import OpenAI, OpenAIError
import json
from typing import Dict

def extract_minutes(event, context):
    bucket_name = event['bucket']
    transcript_file = event['name']

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(transcript_file)

    transcript = blob.download_as_string().decode('utf-8')

    openai_api_key = os.environ.get('OPENAI_API_KEY')
    minutes_model = os.environ.get('MINUTES_MODEL', 'gpt-4-0125-preview')

    minutes_extractor = OpenAIMeetingMinutesExtractor(openai_api_key, minutes_model)

    try:
        minutes = minutes_extractor.extract_minutes(transcript)
    except OpenAIError as e:
        raise MeetingMinutesExtractorError(f"Error extracting meeting minutes: {e}") from e

    minutes_bucket_name = os.environ.get('MINUTES_BUCKET_NAME')
    if not minutes_bucket_name:
        raise ValueError('Minutes bucket name not set')

    minutes_bucket = storage_client.bucket(minutes_bucket_name)
    minutes_blob = minutes_bucket.blob(f'{os.path.splitext(transcript_file)[0]}.json')
    minutes_blob.upload_from_string(json.dumps(minutes))

    # Publish a message to the Pub/Sub topic
    # (Code for publishing to Pub/Sub topic goes here)

class MeetingMinutesExtractorError(Exception):
    pass

class OpenAIMeetingMinutesExtractor:
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def extract_minutes(self, transcription: str) -> Dict[str, str]:
        # (Code for extracting meeting minutes using OpenAI API)
        # ...