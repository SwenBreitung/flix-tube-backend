from django.contrib import admin
from .models import VideoContent
from likes.models import Like


@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at', 'view_count')
    readonly_fields = ('created_at', 'up_likes_count', 'down_likes_count')

    def up_likes_count(self, obj):
        # obj ist eine Instanz von VideoContent
        return Like.objects.filter(video=obj, up_like=True).count()
    
    def down_likes_count(self, obj):
        # obj ist eine Instanz von VideoContent
        return Like.objects.filter(video=obj, down_like=True).count()
    
    up_likes_count.short_description = 'Up Likes'
    down_likes_count.short_description = 'Down Likes'
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'video', 'video_imgs', 'preview_gif', 'view_count', 'up_likes_count', 'down_likes_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )