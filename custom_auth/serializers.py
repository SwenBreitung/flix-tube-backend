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
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    image = serializers.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'image']
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Die beiden Passwörter stimmen nicht überein.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        image = validated_data.pop('image', None) 
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()


        # UserProfile.objects.create(user=user)
        UserProfile.objects.create(user=user, image=image)

        token = Token.objects.create(user=user)
        print(f"Token created for user: {user.username}, Token: {token.key}")

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()  
    password = serializers.CharField()