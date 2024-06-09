from django.db import models

# Create your models here.

class VideoContent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    # Weitere Felder...

    def __str__(self):
        return self.title
