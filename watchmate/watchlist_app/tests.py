from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from watchlist_app.api import serializers
from watchlist_app import models
# Test Cases

class StreamPlatFormTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'example',
            password = 'Password@123'
        )
        self.token = Token.objects.get(user__username = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_streamplatform_create(self):
        data = {
            "name": "Best movie",
            "website": "https://netflix.com",
            "about": "Streaming PlatForm"
        }
        url = reverse('streamplatform-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)