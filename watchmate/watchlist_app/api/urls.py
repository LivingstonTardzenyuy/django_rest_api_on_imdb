from django.urls import path, include
from watchlist_app.api.views import *

urlpatterns = [
    path('', movie_list, name='movie_list'),
]
