from django.http import JsonResponse
from django.shortcuts import render
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
from .models import VideoContent
from rest_framework.permissions import IsAuthenticated
import os
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
import logging
logger = logging.getLogger(__name__)
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.views import APIView
from rest_framework.response import Response

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


@method_decorator(cache_page(CACHETTL), name='dispatch')
class Video_contentView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    parser_classes = (MultiPartParser, FormParser)  
    lookup_field = 'id' 
    queryset = VideoContent.objects.all()
    serializer_class = Video_contentSerializer


    """
    Increments the view count of the video content by 1 and saves the updated value to the database.
    :return: None. The method updates the view count and saves the instance.
    """
    def increment_view_count(self):
        self.view_count + 1
        self.save()


    """
    Handles GET requests to retrieve all video content, increment the view count,
    and serialize the data for the response.
    - Increments the view count before retrieving video content.
    - Logs debug information and prints the serialized data for testing purposes.
    :param request: The HTTP request object.
    :param *args: Additional positional arguments.
    :param **kwargs: Additional keyword arguments.
    :return: A Response object containing the serialized video content data.
    """
    def get(self, request, *args, **kwargs):
        self.increment_view_count()  
        logger.debug("List-Methode aufgerufen")
        print('video_contents',video_contents)
        video_contents = VideoContent.objects.all()
        serializer = Video_contentSerializer(video_contents, many=True)        
        print('testi9ng!!!!',serializer.data)  # Debug: Überprüfe die Ausgabe des Serializers
        return Response(serializer.data)


    """
    Handles GET requests to retrieve and return a filtered list of video content.
    - Retrieves the queryset, applies any filters, and serializes the results.
    - Prints a debug message indicating that the list method was called.
    :param request: The HTTP request object.
    :param *args: Additional positional arguments.
    :param **kwargs: Additional keyword arguments.
    :return: A Response object containing the serialized list of video content.
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        print ('list methode wurde verwendet')
        return Response(serializer.data)


    """
    The `retrieve` function increments the view count of an object, saves the instance, and returns the
    serialized data.
    
    :param request: The `request` parameter in the `retrieve` method represents the HTTP request that
    was made to retrieve the instance. It contains information such as the type of request (GET, POST,
    etc.), headers, user information, and any data that was sent along with the request. In this method,
    the
    :return: The `retrieve` method is returning the data serialized by the `serializer` in the form of a
    Response.
    """  
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        print ('retrieve methode wurde verwendet, instance.view_count =',instance)
        serializer = self.get_serializer(instance)
        print ('serializer methode wurde verwendet, instance =',serializer.data)
        return Response(serializer.data)


    """
        This Python function receives data, serializes it, creates a video content object, and returns a
        response based on the validity of the serializer.
        
        :param request: The `request` parameter in the `post` method is typically an object that
        contains information about the incoming HTTP request, such as the request data, headers, method
        type, and more. In this specific code snippet, `request.data` is being used to access the data
        sent in the request body
        :return: If the serializer is valid, the data will be returned with a status of HTTP 201
        Created. If the serializer is not valid, the errors will be returned with a status of HTTP 400
        Bad Request.
    """
    def post(self, request, *args, **kwargs):
        
        print("Empfangene Daten:", request.data)    
        serializer = Video_contentSerializer(data=request.data)
        print(serializer.data) 
        print("Video_content created: ", serializer)
        if serializer.is_valid():
            video_content = serializer.save()
            print("vor erste 1 if abfrage!!!!!!!!!!!",video_content)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    """
    The function `get_csrf_token` sets a CSRF token in a JSON response cookie with specific attributes.
    
    :param request: The `request` parameter in the `get_csrf_token` function is typically an HttpRequest
    object that represents the incoming HTTP request. It contains information about the request, such as
    headers, cookies, and other metadata. In this context, it is used to retrieve the CSRF token from
    the request's `
    :return: A JsonResponse object with a message 'CSRF token set' is being returned.
    """
def get_csrf_token(request):
    response = JsonResponse({'message': 'CSRF token set'})
    response.set_cookie('csrftoken', request.META.get('CSRF_COOKIE'), httponly=True, secure=True, samesite='Strict')
    return response


# This Python class represents a view for searching video content based on a query parameter.
class VideoSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('query', None)
        if query:
            videos = VideoContent.objects.filter(title__startswith=query)
            serializer = Video_contentSerializer(videos, many=True, context={'request': request})
            return Response({'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'error': 'No query provided'}, status=status.HTTP_400_BAD_REQUEST)