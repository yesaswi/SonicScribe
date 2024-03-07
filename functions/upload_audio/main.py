import os
from google.cloud import storage

def upload_audio(request):
    if request.method != 'POST':
        return 'Method not allowed', 405

    audio_file = request.files.get('audio')
    if not audio_file:
        return 'No audio file found', 400

    bucket_name = os.environ.get('AUDIO_BUCKET_NAME')
    if not bucket_name:
        return 'Audio bucket name not set', 500

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(audio_file.filename)

    blob.upload_from_file(audio_file)

    return 'Audio file uploaded successfully', 200
