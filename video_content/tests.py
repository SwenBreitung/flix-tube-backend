
import os
import shutil
from unittest.mock import MagicMock, patch
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
import threading
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from video_content.models import VideoContent
from video_content.models import VideoContent
from video_content.serilazers import Video_contentSerializer
from .views import Video_contentView
# Create your tests here.



class VideoContentUploadTests(APITestCase):

    # def setUp(self):
    #     self.client = APIClient()
    #     self.upload_url = reverse('video_content')  # Stelle sicher, dass du die URL in deiner urls.py entsprechend benannt hast

    def test_upload_video_success(self):
        """
        Testet das erfolgreiche Hochladen eines Videos.
        """
        video_data = {
            'title': 'Test Video',
            'description': 'Test description',
            'video': SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")
        }
        
        response = self.client.post(self.upload_url, video_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(VideoContent.objects.filter(title='Test Video').exists())

    def test_upload_video_without_title(self):
        """
        Testet das Hochladen eines Videos ohne Titel, was fehlschlagen sollte.
        """
        video_data = {
            'description': 'Test description',
            'video': SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")
        }
        
        response = self.client.post(self.upload_url, video_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_video_without_file(self):
        """
        Testet das Hochladen eines Videos ohne Videodatei.
        """
        video_data = {
            'title': 'Test Video',
            'description': 'Test description',
        }
        
        response = self.client.post(self.upload_url, video_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def setUp(self):
        # Stelle sicher, dass das Verzeichnis für Thumbnails existiert
        self.thumbnail_dir = 'media/video_imgs'
        if not os.path.exists(self.thumbnail_dir):
            os.makedirs(self.thumbnail_dir)

        # Video- und Bild-Testdaten
        self.video = SimpleUploadedFile("test.mp4", b"file_content", content_type="video/mp4")
        self.image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

        self.client = APIClient()
        
    @patch('subprocess.run')
    def test_create_gif(self, mock_run):
        serializer = Video_contentSerializer()
        video_path = 'path/to/video.mp4'
        output_gif_path = 'path/to/output.gif'
        serializer.create_gif(video_path, output_gif_path)
        mock_run.assert_called_once()

    @patch('os.unlink')
    @patch('PIL.Image.Image.save')
    @patch('moviepy.editor.VideoFileClip')
    def test_create_thumbnail(self, mock_clip, mock_save, mock_unlink):
        mock_video_clip_instance = MagicMock()
        mock_video_clip_instance.get_frame.return_value = 'frame'
        mock_video_clip_instance.duration = 10
        mock_clip.return_value.__enter__.return_value = mock_video_clip_instance

        serializer = Video_contentSerializer()
        path = serializer.create_thumbnail(self.video)
        self.assertTrue(path.startswith(self.thumbnail_dir))
        mock_save.assert_called_once()
        mock_unlink.assert_called_once()
        
        
    @patch('video_content.Video_contentSerializer.create_thumbnail', return_value='path/to/thumbnail.jpg')
    @patch('video_content.Video_contentSerializer.create_gif')
    def test_create_video_content(self, mock_create_gif, mock_create_thumbnail):
        data = {
            'title': 'Test Video',
            'description': 'Test Description',
            'video': self.video,
            'video_imgs': self.image,
        }
        serializer = Video_contentSerializer(data=data)
        if serializer.is_valid():
            video_content = serializer.save()
            self.assertEqual(video_content.title, 'Test Video')
            mock_create_thumbnail.assert_called_once_with(self.video)
            # Überprüfe, ob das GIF-Erstellungsverfahren aufgerufen wurde
            mock_create_gif.assert_called_once()

        # Aufräumen
        if os.path.exists(self.thumbnail_dir):
            shutil.rmtree(self.thumbnail_dir)
