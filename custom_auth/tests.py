from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
import threading
from .views import LoginView


# Create your tests here.



class LoginViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.login_url = reverse('login')

    def test_incorrect_credentials(self):
        wrong_credentials = {'username': 'user_does_not_exist', 'password': 'wrong_password'}
        response = self.client.post(self.login_url, wrong_credentials)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid credentials')
    
    def test_normal_login(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_guest_login(self):
        response = self.client.post(self.login_url, {'username': 'gast', 'password': 'any'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('Temporary guest account created', response.data['message'])

    def test_simultaneous_guest_logins(self):
        def login_guest():
            response = self.client.post(self.login_url, {'username': 'gast', 'password': 'any'})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        threads = [threading.Thread(target=login_guest) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def test_brute_force_protection(self):
        credentials = {'username': 'testuser', 'password': 'wrong_password'}
        for _ in range(10):
            response = self.client.post(self.login_url, credentials)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
    # def setUp(self):
    #     # Vorbereitung: URL für den Login festlegen
    #     self.login_url = reverse('login-url')
    
    # def setUp(self):
    #     # Erstellt einen Benutzer für den Test des doppelten Namens und normalen Logins
    #     self.user = User.objects.create_user(username='testuser', password='testpassword123')
    #     self.login_url = reverse('login-url')  # Stellen Sie sicher, dass Sie die URL in urls.py richtig benannt haben


    # def test_incorrect_credentials(self):
    #     """
    #     Stellt sicher, dass bei falschen Anmeldeinformationen kein Zugang gewährt wird.
    #     Erwartet wird eine Antwort mit dem Statuscode 400 und einer Nachricht,
    #     die auf ungültige Anmeldeinformationen hinweist.
    #     """
    #     wrong_credentials = {
    #         'username': 'user_does_not_exist',
    #         'password': 'wrong_password'
    #     }
    #     response = self.client.post(self.login_url, wrong_credentials)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('error', response.data)
    #     self.assertEqual(response.data['error'], 'Invalid credentials')
        
    

    # def test_login_duplicate_name(self):
    #     """Testet, ob der Login mit einem bestehenden Namen korrekt abgelehnt wird."""
    #     response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword123'})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertNotIn('error', response.data)  # Erwartet eine erfolgreiche Authentifizierung

    #     # Versucht erneut, den gleichen Benutzernamen und Passwort zu verwenden
    #     response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword123'})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertNotIn('error', response.data)


    # def test_normal_login(self):
    #     """Testet den normalen Login-Prozess."""
    #     response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword123'})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn('token', response.data)


    # def test_guest_login(self):
    #     """Testet den Login als Gastbenutzer."""
    #     response = self.client.post(self.login_url, {'username': 'gast', 'password': 'any'})
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertIn('Temporary guest account created', response.data['message'])


    # def test_simultaneous_guest_logins(self):
    #     """Testet die gleichzeitige Anmeldung mehrerer Gastbenutzer."""


    # def login_guest():
    #     response = self.client.post(self.login_url, {'username': 'gast', 'password': 'any'})
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertIn('Temporary guest account created', response.data['message'])

    #     # Erstellen Sie Threads für gleichzeitige Login-Versuche
    #     threads = [threading.Thread(target=login_guest) for _ in range(5)]
    #     for thread in threads:
    #         thread.start()
    #     for thread in threads:
    #         thread.join()


    # def test_token_validity_on_protected_endpoint(self):
    #     """
    #     Testet die Gültigkeit des zurückgegebenen Tokens, indem es verwendet wird, um auf eine geschützte Ressource zuzugreifen.
    #     """
    #     # Erst erfolgreich einloggen
    #     correct_credentials = {'username': 'testuser', 'password': 'correct_password'}
    #     login_response = self.client.post(self.login_url, correct_credentials)
    #     token = login_response.data['token']
        
    #     # Zugriff auf eine geschützte Ressource versuchen
    #     protected_url = reverse('protected-url')
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    #     protected_response = self.client.get(protected_url)
        
    #     self.assertEqual(protected_response.status_code, status.HTTP_200_OK)
        
        
    # def test_brute_force_protection(self):
    #     """
    #     Testet, ob das System Schutzmechanismen gegen Brute-Force-Angriffe hat.
    #     Hier wird versucht, mehrmals hintereinander mit falschen Daten sich anzumelden,
    #     um zu prüfen, ob das System nach mehreren Fehlversuchen Maßnahmen ergreift.
    #     """
    #     credentials = {'username': 'testuser', 'password': 'wrong_password'}
    #     for _ in range(10):  # Simuliert mehrere Anmeldeversuche
    #         response = self.client.post(self.login_url, credentials)
        
    #     # Überprüfen, ob nach mehreren Versuchen eine spezielle Reaktion erfolgt, z.B. eine Sperrung oder Rate Limit Error
    #     self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        # Diese Zeile sollte angepasst werden, um den spezifischen Mechanismus zu prüfen,
        # den Ihr System implementiert, z.B. könnte hier ein Statuscode für zu viele Anfragen geprüft werden.
