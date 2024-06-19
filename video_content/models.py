from django.db import models
from django.utils import timezone

class VideoContent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)  # Standardwert ist korrekt
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)  # auto_now_add setzt den Wert automatisch
    video_imgs = models.FileField(upload_to='video_imgs/', blank=True, null=True)
    preview_gif = models.FileField(upload_to='video_gifs/', blank=True, null=True)
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
