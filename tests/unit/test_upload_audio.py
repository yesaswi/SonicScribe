import unittest
from unittest import mock
from functions.upload_audio.main import upload_audio

class TestUploadAudio(unittest.TestCase):
    @mock.patch('functions.upload_audio.main.storage.Client')
    def test_upload_audio_success(self, mock_storage_client):
        # Mock the request object
        mock_request = mock.MagicMock()
        mock_request.method = 'POST'
        mock_request.files = {'audio': mock.MagicMock(filename='test_audio.wav', content_type='audio/wav')}
        
        # Mock the storage client and bucket
        mock_bucket = mock.MagicMock()
        mock_storage_client.return_value.bucket.return_value = mock_bucket
        
        # Set the environment variable for the audio bucket name
        with mock.patch.dict('os.environ', {'AUDIO_BUCKET_NAME': 'test-bucket'}):
            response = upload_audio(mock_request)
        
        self.assertEqual(response, ('Audio file uploaded successfully', 200))
        mock_storage_client.assert_called_once_with()
        mock_storage_client.return_value.bucket.assert_called_once_with('test-bucket')
        mock_bucket.blob.assert_called_once()
        mock_bucket.blob.return_value.upload_from_file.assert_called_once()
    
    def test_upload_audio_invalid_method(self):
        mock_request = mock.MagicMock()
        mock_request.method = 'GET'
        
        response = upload_audio(mock_request)
        
        self.assertEqual(response, ('Method not allowed', 405))
    
    def test_upload_audio_missing_file(self):
        mock_request = mock.MagicMock()
        mock_request.method = 'POST'
        mock_request.files = {}
        
        response = upload_audio(mock_request)
        
        self.assertEqual(response, ('No audio file found', 400))
    
    @mock.patch('functions.upload_audio.main.storage.Client')
    def test_upload_audio_missing_bucket_name(self, mock_storage_client):
        mock_request = mock.MagicMock()
        mock_request.method = 'POST'
        mock_request.files = {'audio': mock.MagicMock()}
        
        with mock.patch.dict('os.environ', clear=True):
            response = upload_audio(mock_request)
        
        self.assertEqual(response, ('Audio bucket name not set', 500))
        mock_storage_client.assert_not_called()

if __name__ == '__main__':
    unittest.main()