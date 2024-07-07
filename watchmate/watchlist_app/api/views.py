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
from .permissions import AdminUserOrReadOnly 

class ReviewList(generics.ListAPIView):   #Getting user specific reviews
    permission_classes =[IsAuthenticated]   
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']   #pk of the current user
        queryset = Reviews.objects.filter(watchlist = pk)
        return queryset

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewsSerializer
    def perform_create(self, serializer):
        pk = self.kwargs['pk']      
        watchlist_id = WatchList.objects.get(pk=pk)   # get the ID of the watchlist
       
        user_review = self.request.user       
        if Reviews.objects.filter(watchlist = watchlist_id, review_user=user_review).exists():
            raise ValidationError('You have already Reviewed')
        else:
            return serializer.save(watchlist = watchlist_id, review_user = user_review)
        
    def get_queryset(self):
        return Reviews.objects.all()
    
        
class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
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


    

class WatchListListAV(APIView):
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


