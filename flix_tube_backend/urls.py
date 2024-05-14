"""
URL configuration for flix_tube_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from custom_auth.views import  CreateTemporaryUserView, UserRegistrationView, UserViewSet ,LoginView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from likeapp.views import add_like, remove_like
from video_content.views import Video_contentView
from django.urls import path, include

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'video_content', Video_contentView, basename='video_content')

urlpatterns = [ 
    path("", include(router.urls)),
    path("__debug__/", include("debug_toolbar.urls")),
    path('admin/', admin.site.urls),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/create-temp-user/', CreateTemporaryUserView.as_view(), name='create_temp_user'),
    # path('video_content/', Video_contentView.as_view(), name='video_content'),
    path('django-rq/', include('django_rq.urls')),
    path('video_content/<int:video_id>/like/', add_like, name='add_like'),
    path('video_content/<int:video_id>/unlike', remove_like, name='remove_like'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
