from django.conf import settings
from django.db import models
from video_content.models import VideoContent
from django.contrib.auth.models import User

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    video = models.ForeignKey(VideoContent, on_delete=models.CASCADE)
    # like_type = models.CharField(max_length=10, choices=(('up', 'Up'), ('down', 'Down')))
    up_like = models.BooleanField(default=False)
    down_like = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user','video')
    
    
    def save(self, *args, **kwargs):
        if self.up_like and self.down_like:
            raise ValueError("Ein Like kann entweder up_like oder down_like sein, aber nicht beides.")
        super().save(*args, **kwargs)

# Create your models here.
