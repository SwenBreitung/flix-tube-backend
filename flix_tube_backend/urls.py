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
from django.db import router
from django.urls import include, path
from custom_auth.views import CheckAuthView, SimpleLoginView, TemporaryUserView, UserRegistrationView, LoginView, UserViewSet, get_csrf_token
from rest_framework.routers import DefaultRouter

from video_content.views import Video_contentView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'video_content', Video_contentView, basename='video_content')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('django-rq/', include('django_rq.urls')),
    path('temporary_register/', TemporaryUserView.as_view(), name='temporary_register'),
    path('get_csrf_token/', get_csrf_token, name='get_csrf_token'),
    path('simple_login/', SimpleLoginView.as_view(), name='simple_login'),
    path('check_auth/', CheckAuthView.as_view(), name='check_auth'),
]
