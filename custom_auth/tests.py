from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.response import Response
from custom_auth.views import create_temporary_user
from rest_framework.views import APIView

class UserRegistrationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='password123')
        self.token = Token.objects.create(user=self.user)
    
    def test_registration_with_authentication(self):
        url = reverse('register')
        data = {'username': 'new_user', 'email': 'new_user@example.com', 'password': 'password123', 'password2': 'password123'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  
        self.assertIn('auth_token', response.cookies)
        cookie = response.cookies['auth_token']
        self.assertTrue(cookie['httponly'])
        
        
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


class TemporaryUserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        self.token = Token.objects.create(user=self.user)

    def test_create_temporary_user(self):
        url = reverse('temporary_register')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)  # Authentifizierungs-Token hinzufügen
        response = self.client.post(url)

        print("Response status code:", response.status_code)  # Erwartet: 201
        print("Response data:", response.data)  # Erwartet: {'message': 'Temporary user created successfully'}
        print("Response cookies:", response.cookies)  # Erwartet: 'auth_token' Cookie vorhanden

        # Ensure that the user is created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check for the presence of the auth_token cookie
        self.assertIn('auth_token', response.cookies)
        cookie = response.cookies['auth_token']
        self.assertTrue(cookie['httponly'])
    
    # def test_login_success(self):
    #     url = reverse('login')
    #     data = {'username': 'test_user', 'password': 'password123'}
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertTrue('auth_token' in response.cookies)
    
    # def test_login_failure(self):
    #     url = reverse('login')
    #     # Send invalid credentials
    #     data = {'username': 'test_user', 'password': 'wrong_password'}
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)