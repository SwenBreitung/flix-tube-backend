from django.shortcuts import render
from rest_framework.response import Response
from video_content.models import VideoContent
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.views import APIView

from django.utils.decorators import method_decorator
from django.conf import settings



CACHETTL = getattr(settings, 'CACHETTL', None)
@method_decorator(cache_page(CACHETTL), name='dispatch')
class Video_contentView(APIView):
    print("Video_content created: ")
    def post(self, request):
        print("Video_content created: ", self)
        serializer = VideoContent(data=request.data)
        print("Video_content created: ", serializer)
        if serializer.is_valid():
            print("is_valid: ", serializer)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Create your views here.
