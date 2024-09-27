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
from django.core.cache import cache


"""
Handles adding or updating a like (up or down) for a specific video by an authenticated user.
The function supports toggling likes, where an existing like can be removed or changed,
and cache is invalidated after any like modification.

Permissions:
    - Requires the user to be authenticated (IsAuthenticated).

:param request: The HTTP request containing the like type ('up' or 'down').
:param video_id: The ID of the video for which the like is being added or updated.
:return: A JsonResponse with the status of the operation (like added, updated, or removed).
"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_like(request, video_id):
    video = get_object_or_404(VideoContent, pk=video_id)
    user = request.user
    data = request.data
    like_type = data.get('likeType')
    if like_type not in ['up', 'down']:
        print("Invalid likeType received. Only 'up' or 'down' likes are allowed.")
        return JsonResponse({'status': 'Only up or down likes are allowed'}, status=400)

    try:
        like = Like.objects.get(video=video, user=user)
        print(f"Existing like found: up_like={like.up_like}, down_like={like.down_like}")
        
        if like_type == 'up':
            print('testing uplike')
            if like.up_like:
                like.delete()
                cache.delete(f'video_{video.id}_likes')  # Cache invalidieren nach dem Löschen
                print("Up like removed.")
                return JsonResponse({'status': 'up like removed'}, status=200)
            else:
                like.up_like = True
                like.down_like = False
                like.save()
                cache.delete(f'video_{video.id}_likes')  # Cache invalidieren nach dem Speichern
                print("Like updated to up.")
                return JsonResponse({'status': 'like updated to up'}, status=200)
        elif like_type == 'down':
            print('testing downlike')
            if like.down_like:
                like.delete()
                cache.delete(f'video_{video.id}_likes')  # Cache invalidieren nach dem Löschen
                print("Down like removed.")
                return JsonResponse({'status': 'down like removed'}, status=200)
            else:
                like.up_like = False
                like.down_like = True
                like.save()
                cache.delete(f'video_{video.id}_likes')  # Cache invalidieren nach dem Speichern
                print("Like updated to down.")
                return JsonResponse({'status': 'like updated to down'}, status=200)
    except Like.DoesNotExist:
        if like_type == 'up':
            Like.objects.create(video=video, user=user, up_like=True, down_like=False)
            cache.delete(f'video_{video.id}_likes')  # Cache invalidieren nach dem Erstellen
            print("New up like added.")
            return JsonResponse({'status': 'up like added'}, status=201)
        elif like_type == 'down':
            Like.objects.create(video=video, user=user, up_like=False, down_like=True)
            cache.delete(f'video_{video.id}_likes')  # Cache invalidieren nach dem Erstellen
            print("New down like added.")
            return JsonResponse({'status': 'down like added'}, status=201)


"""
Retrieves the count of up and down likes for a specific video.
The function requires the user to be authenticated and returns the number of likes and dislikes.

Permission:
    - Requires the user to be authenticated (IsAuthenticated).

:param request: The HTTP request from the client.
:param video_id: The ID of the video for which likes are being retrieved.
:return: A JsonResponse containing the number of up likes and down likes, with an HTTP 200 status.
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_likes(request, video_id):
    video = get_object_or_404(VideoContent, pk=video_id)
    up_likes = Like.objects.filter(video=video, up_like=True).count()
    down_likes = Like.objects.filter(video=video, down_like=True).count()
    cache.delete(f'video_{video.id}_likes')
    return JsonResponse({'up_likes': up_likes, 'down_likes': down_likes}, status=200)


"""
Removes a like (up or down) for a specific video by the authenticated user.
If the like exists, it is deleted and the cache is invalidated. If no like exists, a 404 error is returned.

Permission:
    - Requires the user to be authenticated (IsAuthenticated).

:param request: The HTTP request from the client.
:param video_id: The ID of the video for which the like is being removed.
:return: A JsonResponse indicating whether the like was successfully removed or if it was not found.
"""
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_like(request, video_id):
    video = get_object_or_404(VideoContent, pk=video_id)
    user = request.user
    try:
        like = Like.objects.get(video=video, user=user)
        like.delete()
        cache.delete(f'video_{video.id}_likes')
        return JsonResponse({'status': 'like removed'}, status=200)
    except Like.DoesNotExist:
        return JsonResponse({'status': 'like not found'}, status=404)

