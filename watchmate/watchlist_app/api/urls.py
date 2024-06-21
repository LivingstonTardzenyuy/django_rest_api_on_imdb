from django.urls import path, include
from watchlist_app.api.views import (WatchListListAV,WatchListDetailsAV, StreamPlatFormAV,
                                     StreamPlatFormDetails,ReviewList,
                                     ReviewDetails
                                     )

urlpatterns = [
    path('', WatchListListAV.as_view(), name='movie_list'),
    path('<int:pk>', WatchListDetailsAV.as_view(), name='movie_details'),


    path('stream/', StreamPlatFormAV.as_view(), name='stream'),
    path('stream/<int:pk>/', StreamPlatFormDetails.as_view(), name = 'streamplatform-detail'),
    
    path('stream/<int:pk>/review', ReviewList.as_view(), name = 'review-list'),
    path('stream/review/<int:pk>', ReviewDetails.as_view(), name='reviews-retrive'),    
]
