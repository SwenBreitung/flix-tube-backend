import random
import uuid
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import redirect, render
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
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from rest_framework.authentication import TokenAuthentication

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


"""
Creates a temporary user with a unique username and a randomly generated password.
Generates an authentication token for the user and returns the user instance and the token.

:return: A tuple containing the new temporary User instance and the generated token key.
"""
def create_temporary_user():
    unique_username = f"guest_{uuid.uuid4().hex[:8]}"
    new_user = User.objects.create_user(username=unique_username, password=uuid.uuid4().hex)
    token, created = Token.objects.get_or_create(user=new_user)
    return new_user, token.key


"""
Retrieves an authentication token by sending a POST request with the username and password.
If the login is successful (HTTP 200), it returns the token; otherwise, it returns None.

:param username: The username for authentication.
:param password: The password for authentication.
:return: The authentication token if login is successful, or None if it fails.
"""
def get_token(username, password):
    response = requests.post('http://127.0.0.1:8000/login/', data={'username': username, 'password': password})
    if response.status_code == 200:
        return response.json().get('token')
    else:
        return None
    
    
    
class UserRegistrationView(APIView): 
    permission_classes = [AllowAny]
    
    """
    Handles user registration by validating the request data and creating a new user.
    If the registration is successful, an authentication token is generated, and the token is 
    set as an HTTP-only cookie. If validation fails, it returns the corresponding errors.

    :param request: The HTTP request containing user registration data.
    :return: A Response with a success message and token cookie if the user is created,
    or a 400 response with validation errors if the request data is invalid.
    """
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


"""
Sets a CSRF token cookie and returns a JSON response indicating the token has been set.
The CSRF token is stored in an HTTP-only, secure cookie with a 'Strict' SameSite policy.

:param request: The HTTP request from which the CSRF token is retrieved.
:return: A JsonResponse with a message confirming the CSRF token has been set.
"""
@csrf_exempt
@permission_classes([AllowAny])
def get_csrf_token(request):
    response = JsonResponse({'message': 'CSRF token set'})
    response.set_cookie('csrftoken', request.META.get('CSRF_COOKIE'), httponly=True, secure=True, samesite='Strict')
    return response

class LoginView(APIView):
    
    
    
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


    """
    Handles user login by validating the provided username and password.
    If authentication is successful, an authentication token is created or retrieved,
    and it is stored in an HTTP-only, secure cookie. If authentication fails, 
    an error response is returned.

    :param request: The HTTP request containing the username and password for authentication.
    :return: A JsonResponse with a success message and token cookie on successful login,
    or a 400 response with an error message if authentication fails.
    """
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
    
    
    """
    Handles user login by authenticating the provided username and password.
    If authentication is successful, a token is created or retrieved, and is sent in the response
    both as a JSON field and in an HTTP-only, secure cookie. If authentication fails,
    an unauthorized response is returned.

    Permission:
        - Allows any user to access this endpoint (no authentication required).
        - CSRF protection is disabled using @csrf_exempt.

    :param request: The HTTP request containing the 'username' and 'password' for authentication.
    :return: A Response with a success message and the authentication token in both the response body
        and as a secure cookie, or a 401 unauthorized response if authentication fails.
    """
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
                samesite='Lax'
            )
            return response
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        

class CheckAuthView(APIView):
    
    
    """
    Handles a GET request to check if the user is authenticated.
    If the user is authenticated, returns a success response with the user's details.
    If the user is not authenticated, redirects them to the login page.

    Permission:
        - Requires the user to be authenticated (IsAuthenticated).

    :param request: The HTTP request from the client.
    :return: A Response with a success message and the user's details if authenticated,
            or a redirect to the login page if not authenticated.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):
        
        if not request.user.is_authenticated:
            return redirect('simple_login') 
        user = request.user
        return Response({
            'message': 'User is authenticated',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }, status=status.HTTP_200_OK)



class LogoutView(APIView):
    
    
    """
    Handles user logout by deleting the user's authentication token and logging them out.
    If the token does not exist, it returns an error message. If successful, it logs the user out
    and returns a success message.
    Authentication:
        - Requires TokenAuthentication to identify the user.
    Permission:
        - Requires the user to be authenticated (IsAuthenticated).
    :param request: The HTTP request from the client.
    :return: A Response with a success message upon successful logout, 
            or a 400 error if the token is not found.
    """
    authentication_classes = [TokenAuthentication]  
    permission_classes = [IsAuthenticated]  
    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()  
        except Token.DoesNotExist:
            return Response({'error': 'Token not found'}, status=status.HTTP_400_BAD_REQUEST)
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


class GuestLoginView(APIView):
    
    """
    Handles guest login by logging out the current user (if authenticated) and creating a new guest user.
    Generates an authentication token for the guest user and logs them in. Returns the token and guest username.
    Permission:
        - Allows any user (authenticated or not) to access this endpoint (AllowAny).
    :param request: The HTTP request from the client.
    :return: A Response with a success message, the generated token, and the guest username.
    """
    permission_classes = [AllowAny] 
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request) 
        username = f'guest_{random.randint(1000, 9999)}'
        guest_user = User.objects.create_user(username=username, password=None)
        guest_user.save()
        token, created = Token.objects.get_or_create(user=guest_user)
        login(request, guest_user)
        return Response({
            'message': 'Guest login successful',
            'token': token.key, 
            'username': guest_user.username
        }, status=status.HTTP_201_CREATED)
        
        