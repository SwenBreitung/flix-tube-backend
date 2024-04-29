
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
from .views import Video_contentView
# Create your tests here.



class VideoContentUploadTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.upload_url = reverse('video_content')  # Stelle sicher, dass du die URL in deiner urls.py entsprechend benannt hast

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
