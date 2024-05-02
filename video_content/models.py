
from django.db import models
from django.utils import timezone


class VideoContent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)   
    # updated_at = models.DateTimeField(auto_now=True)
    video = models.FileField(upload_to='videos/',blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    video_image = models.FileField(upload_to='video_imgs/',blank=True, null=True)
    preview_gif = models.FileField(upload_to='video_gifs/',blank=True, null=True)
    
    def __str__(self):
        return self.title

# Create your models here.
