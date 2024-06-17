from watchlist_app.models import WatchList, StreamPlatForm
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatFormSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView



class StreamPlatFormAV(APIView):
    def get(self, request):
        streamPlatForm = StreamPlatForm.objects.all()
        serializer = StreamPlatFormSerializer(streamPlatForm, many=True)
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


