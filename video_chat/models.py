from datetime import date
from django.db import models
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
# from django.db.models.fields import DateField


class Chat(models.Model):
    createt_at = models.DateField(default = date.today)


class Message(models.Model):
    text = models.CharField (max_length=500)
    created_at = models.DateField(default = date.today)
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE,related_name='chat_message_set', default = None, blank = True, null = True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='author_message_set')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='receiver_message_set')


class RegisterForm(UserCreationForm):
    # Optional: Füge zusätzliche Felder hinzu, wenn benötigt
    # email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

# Create your models here.
