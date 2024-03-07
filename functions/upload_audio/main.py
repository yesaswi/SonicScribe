import os
from google.cloud import storage
import functions_framework
from datetime import datetime

@functions_framework.http
def upload_audio(request):
    if request.method != 'POST':
        return 'Method not allowed', 405

    audio_file = request.files.get('audio')
    if not audio_file:
        return 'No audio file found', 400
    
    bucket_name = os.environ.get('AUDIO_BUCKET_NAME')
    if not bucket_name:
        return 'Audio bucket name not set', 500
    
    # Calculate file size
    file_size = (lambda f: f.seek(0, os.SEEK_END) or f.tell())(audio_file)
    audio_file.seek(0)  # Reset file pointer to the beginning

    print(f'Audio file content type: {audio_file.content_type}')
    print(f'Audio file name: {audio_file.filename}')
    print(f'Audio file size: {file_size} bytes')

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Generate a unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    audio_file_name_prefix = f"{timestamp}"
    audio_file_name = f"{audio_file_name_prefix}_{audio_file.filename}"
    # Create a blob with the unique filename
    blob = bucket.blob(f"Raw/{audio_file_name}")

    # Upload audio file to GCS
    blob.upload_from_file(file_obj=audio_file, content_type=audio_file.content_type)

    return 'Audio file uploaded successfully', 200
