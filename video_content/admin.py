from django.contrib import admin
from video_content.models import VideoContent
# Register your models here.
from import_export import resources
from .models import VideoContent
from import_export.admin import ImportExportModelAdmin
from likeapp.models import Like


@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'video', 'video_imgs', 'preview_gif','id','view_count','up_likes_count')
    search_fields = ['title', 'description']
    readonly_fields = ('up_likes_count', 'down_likes_count','created_at')

    def up_likes_count(self, obj):
        # obj ist eine Instanz von VideoContent
        return Like.objects.filter(video=obj, like_type='up').count()
    up_likes_count.short_description = 'Up Likes'
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'video', 'video_imgs', 'preview_gif', 'created_at', 'view_count', 'up_likes_count', 'down_likes_count')
        }),
    )