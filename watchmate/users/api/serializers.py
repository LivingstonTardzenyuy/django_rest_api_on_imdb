from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password



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
        

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_password_confirmation = serializers.CharField(required=True, write_only=True)
    
    
    # Field level validation checking if old password match.
    def validate_old_password(self, value):
        user = self.context['request'].user 
        if not user.check_password(value):
            raise serializers.ValidationError('Old Password Do not match')
        return value
    
    # Validating object 
    def validate(self, data):
        if data['new_password'] != data['new_password_confirmation']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        validate_password(data['new_password'], self.context['request'].user)
        return data
    
    def save(self, **kwargs):
        user = self.context['request'].user 
        user.set_password(self.validated_data['new_password'])  
        user.save()
        return user 
        
        