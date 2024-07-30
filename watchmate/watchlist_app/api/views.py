from watchlist_app.models import WatchList, StreamPlatForm, Reviews
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatFormSerializer, ReviewsSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import AdminUserOrReadOnly, IsReviewUserOrReadOnly 
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend


class ReviewsUser(viewsets.ViewSet):
    filter_backends = [DjangoFilterBackend]
    def list(self, request):
        username = self.request.query_params.get('username')
        if username:
        
            queryset = Reviews.objects.filter(review_user__username = username)
            serializer = ReviewsSerializer(queryset, many=True )
            return Response(serializer.data)
        return Response('error', 'Username parameter is required', status = status.HTTP_400_BAD_REQUEST)
        
class ReviewList(generics.ListAPIView):   #Getting user specific reviews
    serializer_class = ReviewsSerializer
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['active', 'review_user__username']

    def get_queryset(self):
        pk = self.kwargs['pk']   #pk of the current user
        queryset = Reviews.objects.filter(watchlist = pk)
        return queryset

class ReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewsSerializer
    throttle_classes = [ReviewCreateThrottle]
    def perform_create(self, serializer):
        pk = self.kwargs['pk']      
        watchlist_id = WatchList.objects.get(pk=pk)   # get the ID of the watchlist
       
        user_review = self.request.user       
        if Reviews.objects.filter(watchlist = watchlist_id, review_user=user_review).exists():
            raise ValidationError('You have already Reviewed')
        
        if watchlist_id.num_ratings == 0:
            watchlist_id.avg_rating = serializer.validated_data['rating']
            # watchlist_id.num_ratings = 1
        else:
            watchlist_id.avg_rating = (serializer.validated_data['rating'] + watchlist_id.avg_rating) / 2
        
        watchlist_id.num_ratings = watchlist_id.num_ratings + 1
        watchlist_id.save()
        
        return serializer.save(watchlist = watchlist_id, review_user = user_review)
        

    def get_queryset(self):
        return Reviews.objects.all()
    
        
class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsReviewUserOrReadOnly]
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer

class StreamPlatFormV(viewsets.ViewSet):
    def list(self, request):
        queryset = StreamPlatForm.objects.all()
        serializer = StreamPlatFormSerializer(queryset, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def retrieve(self,request, pk=None):
        queryset = StreamPlatForm.objects.all()
        streamPlatForm = get_object_or_404(queryset, pk=pk)
        streamSerializer = StreamPlatFormSerializer(streamPlatForm)
        return Response(streamSerializer.data, status =status.HTTP_200_OK)
    
    def create(self, request):
        serializer = StreamPlatFormSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        streamPlatForm = StreamPlatForm.objects.all()
        streamPlatFormDetail = get_object_or_404(streamPlatForm, pk=pk)
        streamPlatFormDetail.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
        
    def update(self, request, pk=None):
        stramPlatForm = StreamPlatForm.objects.all()
        streamPlatformDetail = get_object_or_404(stramPlatForm, pk=pk)
        serializer = StreamPlatFormSerializer(streamPlatformDetail, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    
class StreamPlatFormAV(APIView):
    def get(self, request):
        streamPlatForm = StreamPlatForm.objects.all()
        serializer = StreamPlatFormSerializer(
            streamPlatForm, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request, format = None):
        serializer = StreamPlatFormSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)    
    
class StreamPlatFormDetails(APIView):
    def get(self, request,pk, format=None):
        try:
            streamPlatForm = StreamPlatForm.objects.get(pk=pk)
        except StreamPlatForm.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatFormSerializer(streamPlatForm) 
        return Response(serializer.data, status = status.HTTP_200_OK)
    
       
    def put(self, request, pk, format=None):
        try:
            streamPlatForm = StreamPlatForm.objects.get(pk=pk)
        except StreamPlatForm.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatFormSerializer(streamPlatForm, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk, format=None):
        try:
            streamPlatForm = StreamPlatForm.objects.get(pk=pk)
        except StreamPlatForm.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        streamPlatForm.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)        


class WatchListSearch(mixins.ListModelMixin, viewsets.GenericViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'active']
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    # return Response(serializer_class.data)
class WatchListListAV(APIView):
    permission_classes =[AdminUserOrReadOnly]
    def get(self, request, format=None):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = WatchListSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class WatchListDetailsAV(APIView):
    permission_classes = [AdminUserOrReadOnly]
    def get(self, request, pk, format=None):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'movie not found'}, status = status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, format=None):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'movie not found'}, status = status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, format=None):
        movie=WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


