from django.shortcuts import render
from rest_framework.response import Response
from video_content.models import VideoContent
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.conf import settings
from video_content.serilazers import Video_contentSerializer
CACHETTL = getattr(settings, 'CACHETTL', None)
from rest_framework.parsers import MultiPartParser, FormParser
import logging
from moviepy.editor import VideoFileClip
from PIL import Image
import os
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

# logger = logging.getLogger(__name__)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

@method_decorator(cache_page(CACHETTL), name='dispatch')
class Video_contentView(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    parser_classes = (MultiPartParser, FormParser)  
    lookup_field = 'id' 
    queryset = VideoContent.objects.all()
    serializer_class = Video_contentSerializer
    # Create your views here.   

    def increment_view_count(self):
        self.view_count += 1
        self.save()
        
        
    def get(self, request, *args, **kwargs):
        self.increment_view_count()  
        print('video_contents',video_contents)
        video_contents = VideoContent.objects.all()
        serializer = Video_contentSerializer(video_contents, many=True)        
        print('testi9ng!!!!',serializer.data)  # Debug: Überprüfe die Ausgabe des Serializers
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        print("Empfangene Daten:", request.data)    
        # Erstellen des Serializers mit Daten aus request.data, die sowohl Dateien als auch normale Daten enthalten können
        serializer = Video_contentSerializer(data=request.data)
        print(serializer.data) 
        print("Video_content created: ", serializer)

        if serializer.is_valid():
            print("is_valid: ", serializer)
            video_content = serializer.save()
            print("vor erste 1 if abfrage!!!!!!!!!!!",video_content)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




