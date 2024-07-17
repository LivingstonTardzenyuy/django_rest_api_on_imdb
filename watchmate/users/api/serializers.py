from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(
        style={
            'input_type':'password'
        },
        write_only=True
        )
    
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmation']        
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }
    # def save(self,)