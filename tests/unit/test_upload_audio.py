import pytest
from functions.upload_audio.main import upload_audio

# Mocking the request object provided to the upload_audio function
@pytest.fixture
def mock_request(mocker):
    return mocker.MagicMock()

# Patching the 'storage.Client' constructor to return a mock object
# This simplifies the previous version by focusing only on the mock client necessary for interaction
@pytest.fixture
def mock_storage_client(mocker):
    return mocker.patch('functions.upload_audio.main.storage.Client')

# Optionally setting and cleaning up an environment variable for tests that rely on it
@pytest.fixture
def mock_environment(monkeypatch):
    monkeypatch.setenv('AUDIO_BUCKET_NAME', 'test-bucket')
    yield
    monkeypatch.delenv('AUDIO_BUCKET_NAME', raising=False)

# Test the successful upload of an audio file
def test_upload_audio_success(mock_request, mock_storage_client, mock_environment, mocker):
    mock_request.method = 'POST'
    mock_request.files = {'audio': mocker.MagicMock(filename='test_audio.wav', content_type='audio/wav')}
    mock_bucket = mocker.MagicMock()
    mock_storage_client.return_value.bucket.return_value = mock_bucket
    
    response = upload_audio(mock_request)
    
    assert response == ('Audio file uploaded successfully', 200)
    mock_storage_client.return_value.bucket.assert_called_once_with('test-bucket')
    mock_bucket.blob.assert_called_once()
    mock_bucket.blob.return_value.upload_from_file.assert_called_once()

# Test handling of an invalid method (GET instead of POST)
def test_upload_audio_invalid_method(mock_request):
    mock_request.method = 'GET'
    response = upload_audio(mock_request)
    
    assert response == ('Method not allowed', 405)

# Test the case where no audio file is provided in the request
def test_upload_audio_missing_file(mock_request):
    mock_request.method = 'POST'
    mock_request.files = {}
    
    response = upload_audio(mock_request)
    
    assert response == ('No audio file found', 400)

# Test the behavior when the required environment variable for the bucket name is missing
def test_upload_audio_missing_bucket_name(mock_request, mock_storage_client, monkeypatch, mocker):
    mock_request.method = 'POST'
    mock_request.files = {'audio': mocker.MagicMock()}
    monkeypatch.delenv('AUDIO_BUCKET_NAME', raising=False)
    
    response = upload_audio(mock_request)
    
    assert response == ('Audio bucket name not set', 500)
    # This assertion checks that the code did not proceed to attempt accessing any bucket due to the missing environment variable
    mock_storage_client.return_value.bucket.assert_not_called()
