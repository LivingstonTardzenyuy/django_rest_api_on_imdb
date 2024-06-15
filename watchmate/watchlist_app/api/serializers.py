from rest_framework import serializers
from watchlist_app.models import Movie 

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    active = serializers.BooleanField(read_only=True)
    
    def validate_name(self, value):
        if len(value) < 5 or len(value) > 50:
            raise serializers.ValidationError('Name must be at least 5 and at most 50')
        return value
    
    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description),
        instance.active = validated_data.get('active', instance.active)
        
        instance.save()
        return instance