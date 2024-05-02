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
logger = logging.getLogger(__name__)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

@method_decorator(cache_page(CACHETTL), name='dispatch')
class Video_contentView(APIView):
    pagination_class = StandardResultsSetPagination
    parser_classes = (MultiPartParser, FormParser)  
    
    # Create your views here.   

    def get(self, request, *args, **kwargs):
        video_contents = VideoContent.objects.all()
        page = self.paginate_queryset(video_contents)
        if page is not set:
            serializer = Video_contentSerializer(video_contents, many=True)
            return Response(serializer.data)
        serializer = Video_contentSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


    def post(self, request, *args, **kwargs):
        print("Empfangene Daten:", request.data)
        logger.debug("Empfangene Request-Daten: %s", request.data)
        
        # Erstellen des Serializers mit Daten aus request.data, die sowohl Dateien als auch normale Daten enthalten können
        serializer = Video_contentSerializer(data=request.data)
        print("Video_content created: ", serializer)

        if serializer.is_valid():
            print("is_valid: ", serializer)
            # Speichern des Serializers und Erstellen eines neuen VideoContent-Objekts
            video_content = serializer.save()
            # Überprüfen, ob ein Thumbnail vorhanden ist, wenn nicht, erstelle eines
            print("vor erste 1 if abfrage!!!!!!!!!!!",video_content)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error("Validierungsfehler: %s", serializer.errors)
            print('error', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



