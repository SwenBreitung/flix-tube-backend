from django.conf import settings
from django.db import models
from video_content.models import VideoContent
from django.contrib.auth.models import User

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    video = models.ForeignKey(VideoContent, on_delete=models.CASCADE)
    like_type = models.CharField(max_length=10, choices=(('up', 'Up'), ('down', 'Down')))

    class Meta:
        unique_together = ('user','video')
# Create your models here.
