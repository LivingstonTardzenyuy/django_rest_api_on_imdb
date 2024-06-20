from django.urls import path, include
from watchlist_app.api.views import *

urlpatterns = [
    path('', WatchListListAV.as_view(), name='movie_list'),
    path('<int:pk>', WatchListDetailsAV.as_view(), name='movie_details'),


    path('stream/', StreamPlatFormAV.as_view(), name='stream'),
    path('stream/<int:pk>/', StreamPlatFormDetails.as_view(), name = 'streamplatform-detail'),
    
    path('review', ReviewList.as_view(), name = 'review-list')
    ]
