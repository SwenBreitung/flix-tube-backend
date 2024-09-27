# from django.contrib import admin
# from likes.models import Like

# admin.site.register(Like)
# Register your models here.
from django.contrib import admin
from .models import Like

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'up_like', 'down_like')