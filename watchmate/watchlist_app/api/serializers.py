from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatForm, Reviews

    
class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        # fields = "__all__"
        exclude = ["watchlist",]

class WatchListSerializer(serializers.ModelSerializer):
    
    # reviews = ReviewsSerializer(read_only=True, many = True) 
    reviews = serializers.StringRelatedField(read_only=True, many=True)  
    class Meta:
        model = WatchList
        fields = "__all__"
        # exclude = ['id', 'active']

    def validate(self, object):
        if object['title'] == object['description']:
            raise serializers.ValidationError('Name should be diferent from description')
        return object

    
class StreamPlatFormSerializer(serializers.ModelSerializer):
    # watchlist = serializers.StringRelatedField(many=True)
    # watchlist = serializers.StringRelatedField(many=True)
    watchlist = WatchListSerializer(many =True, read_only = True)
    class Meta:
        model = StreamPlatForm
        fields = "__all__"
        # exclude = ['id', 'active']
    
