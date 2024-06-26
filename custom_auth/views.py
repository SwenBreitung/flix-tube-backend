import uuid
from django.shortcuts import render
from .serializers import UserSerializer, UserRegistrationSerializer

from .serializers import  UserRegistrationSerializer, UserSerializer,LoginSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRegistrationView(APIView):
    print("User created: ")
    def post(self, request):
        print("User created: ", self)
        serializer = UserRegistrationSerializer(data=request.data)
        print("User created: ", serializer)
        if serializer.is_valid():
            user = serializer.save()  # User wird erstellt und gespeichert
            token, created = Token.objects.get_or_create(user=user)  # Token wird erstellt
            return Response({
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def create_temporary_user():
    unique_username = f"guest_{uuid.uuid4().hex[:8]}"
    new_user = User.objects.create_user(username=unique_username, password=uuid.uuid4().hex)
    new_user.save()
    return new_user





class LoginView(APIView):
    def post(self, request):
        print("Start api_login view")
        print("Received data:", request.data)

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            print("Serializer is valid")

            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            if username == 'gast':
                return self.handle_guest_login()
            else:
                return self.handle_standard_login(username, password)
        else:
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def handle_guest_login(self):
        new_user = self.create_temporary_user()
        token, created = Token.objects.get_or_create(user=new_user)
        print("Temporary user created:", new_user.username)
        print("Token created for temporary user:", token.key)
        return Response({'message': 'Temporary guest account created', 'token': token.key}, status=status.HTTP_201_CREATED)

    def handle_standard_login(self, username, password):
        token_key = self.authenticate_and_get_token(username, password)
        if token_key:
            print("User authenticated successfully")
            print("Token created:", token_key)
            return Response({'token': token_key})
        else:
            print("Invalid credentials")
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    def create_temporary_user(self):
        unique_username = f"guest_{uuid.uuid4().hex[:8]}"
        new_user = User.objects.create_user(username=unique_username, password=uuid.uuid4().hex)
        new_user.save()
        return new_user


    def authenticate_and_get_token(self, username, password):
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return token.key
        else:
            return None


class CreateTemporaryUserView(APIView):
     def post(self, request, *args, **kwargs):
         new_user = create_temporary_user()  # Erstellt einen neuen temporären Benutzer
         serializer = UserSerializer(new_user)
         return Response(serializer.data, status=status.HTTP_201_CREATED)


            

