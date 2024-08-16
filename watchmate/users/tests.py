from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse
from rest_framework.authtoken.models import Token

class RegisterTestCase(APITestCase):
    def test_register(self):
        # Creating a new user
        data = {
            "username": "testcase",
            "password": "TypeScript01@",
            "email": "testcase@example.com",
            "password_confirmation": "TypeScript01@"
        }
        
        url = reverse('sign-up')
        response = self.client.post(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testcase')
        

class LoginTestCase(APITestCase):
    def setUp(self):
        # Creating a user account instance
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass'
            # email = 'testcase@example.com'
            )
    
    
    def test_login(self):
        data = {
            "username": "testuser",
            "password": "testpass"
        }
        url = reverse('token_obtain_pair')
        response = self.client.post(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    # def test_logout(self):
    #     # The 2 lines log in a user
    #     self.token = Token.objects.get(user__username="testuser")
    #     self.client.credentials(HTTP_AUTHORIZATION='Token' + self.token.key)
        
    #     url = reverse('log-out')
    #     response = self.client.post(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)