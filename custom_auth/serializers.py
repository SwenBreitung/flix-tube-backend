from django.apps import AppConfig
from django.shortcuts import render
from rest_framework import viewsets, serializers
from rest_framework.authtoken.models import Token
from django import forms
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['image']
        
        
class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'profile']
        
        

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')


    """
    Validates the password fields in the data. Ensures that 'password' and 'password2' match.
    Raises a ValidationError if the passwords do not match.
    
    :param data: The dictionary containing the input data to validate.
    :return: The validated data if the passwords match.
    :raises ValidationError: If the passwords do not match.
    """
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data


    """
    Creates a new user instance using the validated data.
    Removes the 'password2' field from the data before creating the user.

    :param validated_data: The dictionary containing validated user data, including 'password' but excluding 'password2'.
    :return: The newly created User instance.
    """
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()  
    password = serializers.CharField()