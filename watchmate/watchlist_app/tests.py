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
        self.token, created = Token.objects.get_or_create(user = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    
        # Creating a steam
        self.stream = models.StreamPlatForm.objects.create(
            name="Netflix",
            about="Best movie on earth",
            website="https://netflix.com"
        )
    def test_streamplatform_create(self):
        data = {
            "name": "Best movie",
            "website": "https://netflix.com",
            "about": "Streaming PlatForm"
        }
        url = reverse('streamplatform-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
            
    def test_streamplatform_list(self):
        url = reverse('streamplatform-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_streamplatform_ind(self):
        url = reverse('streamplatform-detail', args=[self.stream.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
    

class WatchListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password123@")
        self.token, created = Token.objects.get_or_create(user = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        self.stream = models.StreamPlatForm.objects.create(
            name="NetFlix",
            about="best platform for movies",
            website="https://netflix.com"
        )
        
        self.watchlist = models.WatchList.objects.create(
            title="Watchlist 1",
            description="This is my first watchlist",
            # user=self.user,
            platForm=self.stream,
            active=True
        )
    def test_watchlist_create(self):
        data = {
            "title": "The Shawshank Redemption",
            "description": "A movie about a man who is wrongfully convicted and sent to prison",
            "acitve": True,
            "platForm": self.stream.id
        }
        
        url = reverse('movie_list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)    
        
    def test_watchlist_list(self):
        url = reverse('movie_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_watchlist_id(self):
        url = reverse('movie_details', args=[self.watchlist.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        