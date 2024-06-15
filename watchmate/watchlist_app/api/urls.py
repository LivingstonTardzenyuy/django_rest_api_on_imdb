from django.urls import path, include
from watchlist_app.api.views import *

urlpatterns = [
    path('', MovieListAV.as_view(), name='movie_list'),
    path('<int:pk>', MovieDetailsAV.as_view(), name='movie_details'),
]
