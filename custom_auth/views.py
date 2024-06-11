import uuid
from django.http import JsonResponse
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
from django.views.decorators.csrf import ensure_csrf_cookie
import requests
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def create_temporary_user():
    unique_username = f"guest_{uuid.uuid4().hex[:8]}"
    new_user = User.objects.create_user(username=unique_username, password=uuid.uuid4().hex)
    token, created = Token.objects.get_or_create(user=new_user)
    return new_user, token.key

def get_token(username, password):
    response = requests.post('http://127.0.0.1:8000/login/', data={'username': username, 'password': password})
    if response.status_code == 200:
        return response.json().get('token')
    else:
        return None
    
    
class UserRegistrationView(APIView): 

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            response = Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            response.set_cookie(
                key='auth_token',
                value=token.key,
                httponly=True,
                secure=True,  # Ensure this is True in production to use HTTPS
                samesite='Strict'  # Adjust based on your needs
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# This class represents a view for handling user login functionality in a Python API.
@csrf_exempt
@permission_classes([AllowAny])
def get_csrf_token(request):
    response = JsonResponse({'message': 'CSRF token set'})
    response.set_cookie('csrftoken', request.META.get('CSRF_COOKIE'), httponly=True, secure=True, samesite='Strict')
    return response

class LoginView(APIView):
    @csrf_exempt
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # Authentication successful, create or get token
            token, created = Token.objects.get_or_create(user=user)
            response = JsonResponse({'message': 'Login successful'})
            response.set_cookie('auth_token', token.key, httponly=True, secure=True, samesite='Strict')
            return response
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class TemporaryUserView(APIView):

    def post(self, request):
        try:
            new_user, token = create_temporary_user()
            response = Response({'message': 'Temporary user created successfully'}, status=status.HTTP_201_CREATED)
            response.set_cookie(
                key='auth_token',
                value=token,
                httponly=True,
                secure=True,  # Ensure this is True in production to use HTTPS
                samesite='Strict'  # Adjust based on your needs
            )
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class SimpleLoginView(APIView):
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            response = Response({'message': 'Login successful', 'token': token.key}, status=status.HTTP_200_OK)
            response.set_cookie(
                key='auth_token',
                value=token.key,
                httponly=True,
                secure=True,
                samesite='Strict'
            )
            return response
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        

class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'message': 'User is authenticated',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }, status=status.HTTP_200_OK)

