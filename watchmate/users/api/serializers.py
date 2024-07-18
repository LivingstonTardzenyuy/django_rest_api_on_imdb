from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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
        
    def save(self):
        email = self.validated_data['email']
        username = self.validated_data['username']
        password = self.validated_data['password']
        password_confirmation = self.validated_data['password_confirmation']
        
        if password !=password_confirmation:
            raise serializers.ValidationError({'error': 'The Password are not the same'})
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'error': 'Username already exists'})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'Email already exists'})
        
        account = User(
            username=username,
            email=email,
        )
        
        account.set_password(password)
        account.save()
        return account
        