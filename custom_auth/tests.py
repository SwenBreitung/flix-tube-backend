from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.response import Response
from custom_auth.views import create_temporary_user
from rest_framework.views import APIView
from rest_framework.test import APITestCase, APIClient

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
    

# class LoginViewTests(APITestCase):
#     def setUp(self):
#         self.username = 'veroxa'
#         self.password = 'Forstwirt1'
#         self.user = User.objects.create_user(username=self.username, password=self.password)

#     def test_successful_login(self):
#         """
#         Test that a user can log in successfully and that the response contains the correct HttpOnly cookie.
#         """
#         url = reverse('login')  # Update this with the correct URL name for your login view
#         data = {
#             'username': self.username,
#             'password': self.password
#         }
#         response = self.client.post(url, data, format='json')

#         # Assert the response is 200 OK
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json().get('message'), 'Login successful')

#         # Assert the auth_token cookie is set and is HttpOnly
#         self.assertIn('auth_token', response.cookies)
#         self.assertTrue(response.cookies['auth_token'].httponly)

#     def test_failed_login(self):
#         """
#         Test that a user login fails with incorrect credentials.
#         """
#         url = reverse('login')  # Update this with the correct URL name for your login view
#         data = {
#             'username': self.username,
#             'password': 'wrongpassword'
#         }
#         response = self.client.post(url, data, format='json')

#         # Assert the response is 400 BAD REQUEST
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.json().get('error'), 'Invalid credentials')


class SimpleLoginViewTests(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'password'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_successful_login(self):
        """
        Test that a user can log in successfully and that the response contains the correct token.
        """
        url = reverse('simple_login')
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(url, data, format='json')

        # Assert the response is 200 OK
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('message'), 'Login successful')

        # Assert the auth_token cookie is set and is HttpOnly
        self.assertIn('auth_token', response.cookies)
        auth_cookie = response.cookies['auth_token']
        self.assertTrue(auth_cookie.get('httponly'))

        # Assert the token is correct
        self.assertEqual(response.json().get('token'), auth_cookie.value)

    def test_failed_login(self):
        """
        Test that a user login fails with incorrect credentials.
        """
        url = reverse('simple_login')
        data = {
            'username': self.username,
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')

        # Assert the response is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json().get('error'), 'Invalid credentials')