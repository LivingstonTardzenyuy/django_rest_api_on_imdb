from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import (WatchListListAV,WatchListDetailsAV, StreamPlatFormAV,
                                     StreamPlatFormDetails,ReviewList,
                                     ReviewDetails, ReviewCreate, StreamPlatFormV,
                                     ReviewsUser,
                                     )

router = DefaultRouter()
router.register(r'stream', StreamPlatFormV, basename='streamplatform')

urlpatterns = [
    path('', WatchListListAV.as_view(), name='movie_list'),
    path('<int:pk>', WatchListDetailsAV.as_view(), name='movie_details'),

    # path('stream/', StreamPlatFormAV.as_view(), name='stream'),
    # path('stream/<int:pk>/', StreamPlatFormDetails.as_view(), name = 'streamplatform-detail'),
    
    path('<int:pk>/review', ReviewList.as_view(), name = 'review-list'),
    path('<int:pk>/review-create', ReviewCreate.as_view(), name = 'review-list'),
    path('review/<int:pk>', ReviewDetails.as_view(), name='reviews-retrive'),    
    path('reviews/<str:username>/', ReviewsUser.as_view({'get': 'list'}), name='review-user'),
    
    path('', include(router.urls)),

]


