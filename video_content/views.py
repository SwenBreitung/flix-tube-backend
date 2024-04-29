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
logger = logging.getLogger(__name__)
@method_decorator(cache_page(CACHETTL), name='dispatch')
class Video_contentView(APIView):
    parser_classes = (MultiPartParser, FormParser)        
    def post(self, request, *args, **kwargs):
        print("Empfangene Daten:", request.data)
        logger.debug("Empfangene Request-Daten: %s", request.data)
        # Erstellen des Serializers mit Daten aus request.data, die sowohl Dateien als auch normale Daten enthalten können
        serializer = Video_contentSerializer(data=request.data)
        # Debugging-Ausgabe des Serializers
        print("Video_content created: ", serializer)
        if serializer.is_valid():
            # Debugging-Ausgabe, wenn die Daten valide sind
            print("is_valid: ", serializer)

            # Speichern des Serializers und Erstellen eines neuen VideoContent-Objekts
            serializer.save()

            # Antwort bei erfolgreicher Erstellung
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error("Validierungsfehler: %s", serializer.errors)
            # Antwort, wenn Daten ungültig sind, mit Fehlerdetails
            print('error',serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

        # print("Empfangene Daten:", request.data)  
        # print("Video_content created: ", self,request)
        # serializer = Video_contentSerializer(data=request.data)
        # print("Video_content created: ", serializer)
        # if serializer.is_valid():
        #     print("is_valid: ", serializer)
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Create your views here.
