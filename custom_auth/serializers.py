from django.apps import AppConfig
from django.shortcuts import render
from rest_framework import viewsets, serializers
from rest_framework.authtoken.models import Token
from django import forms
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        email = forms.EmailField(required=True)
        model = User
        fields = ['username', 'email', 'password','password2']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        print("Validated Data: ", validated_data)  # Zeigt die validierten Daten

        password = validated_data.pop('password')
        print("Password: ", password)  # Zeigt das extrahierte Passwort
        password2 = validated_data.pop('password2')
        if password != password2:
            print("Password mismatch error triggered")
            raise serializers.ValidationError({'password': 'Die beiden Passwörter stimmen nicht überein.'})

        user = User.objects.create_user(**validated_data)
        print("User created: ", user.username)  # Zeigt den erstellten Benutzernamen

        user.set_password(password)
        print("Password set for user: ", user.username)  # Bestätigt, dass das Passwort gesetzt wurde

        user.save()
        print("User saved: ", user.username)  # Bestätigt, dass der Benutzer gespeichert wurde

        token = Token.objects.create(user=user)
        print("Token created for user: ", user.username, "Token:", token.key)  # Zeigt das erstellte Token

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()  
    password = serializers.CharField()