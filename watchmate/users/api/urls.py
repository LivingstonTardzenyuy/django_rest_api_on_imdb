from django.urls import path, include 
from rest_framework.authtoken.views import obtain_auth_token
from users.api.views import registration_view

urlpatterns = [
    path('login/', obtain_auth_token, name='Login in user'),
    path('register/', registration_view, name = 'Registration')
]
