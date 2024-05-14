import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from likeapp.models import Like
from video_content.models import VideoContent
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import VideoContent, Like


@require_http_methods(["POST"])
def add_like(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(VideoContent, pk=video_id)
        data = json.loads(request.body)
        like_type = data.get('likeType', 'up')  # Standardwert 'up', falls nichts gesendet wird
        like, created = Like.objects.get_or_create(video=video, like_type=like_type)
        if created:
            return JsonResponse({'status': 'like added'}, status=201)
        else:
            return JsonResponse({'status': 'already liked'}, status=200)

@require_http_methods(["DELETE"])
def remove_like(request, video_id):
    video = get_object_or_404(VideoContent, pk=video_id)
    print('hier endet es!!')
    try:
        like = Like.objects.get( video=video)
        like.delete()
        return JsonResponse({'status': 'like removed'})
    except Like.DoesNotExist:
        print('hier endet es!!!')
        return JsonResponse({'status': 'like not found'}, status=404)

# class LikeView(APIView):
#     def post(self, request, video_id):
#         """
#         Add a like to a video.
#         """
#         video = get_object_or_404(VideoContent, pk=video_id)
#         like, created = Like.objects.get_or_create(user=request.user, video=video)
        
#         if created:
#             return Response({'status': 'like added'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'status': 'already liked'}, status=status.HTTP_409_CONFLICT)

#     def delete(self, request, video_id):
#         """
#         Remove a like from a video.
#         """
#         video = get_object_or_404(VideoContent, pk=video_id)
#         try:
#             like = Like.objects.get(user=request.user, video=video)
#             like.delete()
#             return Response({'status': 'like removed'}, status=status.HTTP_204_NO_CONTENT)
#         except Like.DoesNotExist:
#             return Response({'status': 'like not found'}, status=status.HTTP_404_NOT_FOUND)

# # Create your views here.
