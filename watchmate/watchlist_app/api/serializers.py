from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatForm 


class WatchListSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = WatchList
        fields = "__all__"
        # exclude = ['id', 'active']

    def validate(self, object):
        if object['name'] == object['description']:
            raise serializers.ValidationError('Name should be diferent from description')
        return object

    
class StreamPlatFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamPlatForm
        fields = "__all__"
        # exclude = ['id', 'active']
    
    
    
    
    
    
# def name_length(value):
#     if len(value) < 5 or len(value) > 50:
#         raise serializers.ValidationError('Name must be at least 5 and at most 50')
    
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField(read_only=True)
    
    # def validate_name(self, value):
    #     if len(value) < 5 or len(value) > 50:
    #         raise serializers.ValidationError('Name must be at least 5 and at most 50')
    #     return value
    
    # def validate(self, object):
    #     if object['name'] == object['description']:
    #         raise serializers.ValidationError('Name should be diferent from description')
    
    # def create(self, validated_data):
    #     return Movie.objects.create(**validated_data)
    
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.description = validated_data.get('description', instance.description),
    #     instance.active = validated_data.get('active', instance.active)
        
    #     instance.save()
    #     return instance