from django.contrib import admin
from video_content.models import VideoContent
# Register your models here.


class VideoContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'description'] 

admin.site.register(VideoContent, VideoContentAdmin)