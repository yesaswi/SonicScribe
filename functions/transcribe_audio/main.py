import os
from google.cloud import storage
from openai import OpenAI, OpenAIError

def transcribe_audio(event, context):
    bucket_name = event['bucket']
    audio_file = event['name']

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(audio_file)

    audio_file_path = "/tmp/" + audio_file
    blob.download_to_filename(audio_file_path)

    openai_api_key = os.environ.get('OPENAI_API_KEY')
    audio_model = os.environ.get('AUDIO_MODEL', 'whisper-1')

    transcriber = OpenAIAudioTranscriber(openai_api_key, audio_model)

    try:
        transcription = transcriber.transcribe_audio(audio_file_path)
    except OpenAIError as e:
        raise AudioTranscriberError(f"Error transcribing audio: {e}") from e

    transcription_bucket_name = os.environ.get('TRANSCRIPTION_BUCKET_NAME')
    if not transcription_bucket_name:
        raise ValueError('Transcription bucket name not set')

    transcription_bucket = storage_client.bucket(transcription_bucket_name)
    transcription_blob = transcription_bucket.blob(f'{os.path.splitext(audio_file)[0]}.txt')
    transcription_blob.upload_from_string(transcription)

    # Publish a message to the Pub/Sub topic
    # (Code for publishing to Pub/Sub topic goes here)

class AudioTranscriberError(Exception):
    pass

class OpenAIAudioTranscriber:
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def transcribe_audio(self, audio_file_path: str, chunk_size_ms: int = 600_000) -> str:
        # (Code for audio transcription using OpenAI API)
        # ...