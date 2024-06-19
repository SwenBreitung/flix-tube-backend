import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from likes.models import Like
from video_content.models import VideoContent
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import VideoContent, Like
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_like(request, video_id):
    video = get_object_or_404(VideoContent, pk=video_id)
    user = request.user
    data = request.data
    like_type = data.get('likeType')

    print(f"Received likeType: {like_type}")  # Log-Ausgabe hinzugefügt

    if like_type != 'up':
        print("Invalid likeType received. Only 'up' likes are allowed.")
        return JsonResponse({'status': 'Only up likes are allowed'}, status=400)

    try:
        like = Like.objects.get(video=video, user=user)
        print(f"Existing like found: {like.like_type}")  # Log-Ausgabe hinzugefügt
        if like.like_type == 'up':
            like.delete()
            print("Up like removed.")
            return JsonResponse({'status': 'like removed'}, status=200)
        else:
            like.like_type = 'up'
            like.save()
            print("Like updated to up.")
            return JsonResponse({'status': 'like updated'}, status=200)
    except Like.DoesNotExist:
        Like.objects.create(video=video, user=user, like_type='up')
        print("New up like added.")
        return JsonResponse({'status': 'like added'}, status=201)
    
# Zusätzliche Funktion zur Überprüfung der Like-Zählungen
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_likes(request, video_id):
    video = get_object_or_404(VideoContent, pk=video_id)
    up_likes = Like.objects.filter(video=video, like_type='up').count()
    down_likes = Like.objects.filter(video=video, like_type='down').count()
    return JsonResponse({'up_likes': up_likes, 'down_likes': down_likes}, status=200)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_like(request, video_id):
    video = get_object_or_404(VideoContent, pk=video_id)
    user = request.user
    try:
        like = Like.objects.get(video=video, user=user)
        like.delete()
        return JsonResponse({'status': 'like removed'})
    except Like.DoesNotExist:
        return JsonResponse({'status': 'like not found'}, status=404)

