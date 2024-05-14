from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from likeapp.models import Like
from video_content.models import VideoContent


# @require_http_methods(["POST"])
def add_like(request, video_id):
    video = get_object_or_404(VideoContent, pk=video_id)
    # Überprüfe, ob der Benutzer dieses Video bereits geliked hat
    like, created = Like.objects.get_or_create(user=request.user, video=video)
    if created:
        return JsonResponse({'status': 'like added'})
    else:
        return JsonResponse({'status': 'already liked'})

@require_http_methods(["DELETE"])
def remove_like(request, video_id):
    video = get_object_or_404(VideoContent, pk=video_id)
    try:
        like = Like.objects.get(user=request.user, video=video)
        like.delete()
        return JsonResponse({'status': 'like removed'})
    except Like.DoesNotExist:
        return JsonResponse({'status': 'like not found'}, status=404)


# Create your views here.
