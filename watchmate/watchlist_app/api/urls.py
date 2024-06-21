from django.urls import path, include
from watchlist_app.api.views import (WatchListListAV,WatchListDetailsAV, StreamPlatFormAV,
                                     StreamPlatFormDetails,StreamPlatFormDetails,
                                     StreamPlatFormDetails
                                     )

urlpatterns = [
    path('', WatchListListAV.as_view(), name='movie_list'),
    path('<int:pk>', WatchListDetailsAV.as_view(), name='movie_details'),


    path('stream/', StreamPlatFormAV.as_view(), name='stream'),
    path('stream/<int:pk>/', StreamPlatFormDetails.as_view(), name = 'streamplatform-detail'),
    
    path('stream/<int:pk>/review', StreamPlatFormDetails.as_view(), name = 'review-list'),
    path('reviews/<int:pk>', StreamPlatFormDetails.as_view(), name='reviews-retrive'),    
]
