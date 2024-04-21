from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile_images/%Y/%m/%d/', verbose_name=("profile_img"), blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
# Create your models here.
