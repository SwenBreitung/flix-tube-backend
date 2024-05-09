from django.contrib import admin
from video_content.models import VideoContent
# Register your models here.
from import_export import resources
from .models import VideoContent
from import_export.admin import ImportExportModelAdmin
# class BookResource(resources.ModelResource):

#     class Meta:
#         model = VideoContent

# class VideoContentAdmin(admin.ModelAdmin):
#     list_display = ['title', 'description'] 


# @admin.register(VideoContent)
# class Video_admin(ImportExportModelAdmin):
#     pass

# admin.site.register(VideoContent, VideoContentAdmin)
# admin.site.register(Video_admin)

@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'video', 'video_imgs', 'preview_gif','id','viewCount')
    search_fields = ['title', 'description']