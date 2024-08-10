from rest_framework.decorators import api_view 
from users.api.serializers import RegistrationSerializer, PasswordChangeSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


#jwt
from rest_framework_simplejwt.tokens import RefreshToken


# from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie

@api_view(['POST'],)
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data = request.data)
        
        data = {}
        if serializer.is_valid():    
            account = serializer.save()
            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email
            token = Token.objects.get(user=account).key
            data['token'] = token 
            
        else:
            data =serializer.errors
        return Response(data)


@api_view(['POST'],)
def logout(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status = status.HTTP_200_OK)
    

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = PasswordChangeSerializer(data = request.data, context={'request': request})
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "Password Change updated Successfully"
        else:
            data = serializer.errors
        return Response(data)
    
    
    
    
@api_view(['POST'])
def registration_view_jwt(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            
            account = serializer.save()
            refresh = RefreshToken.for_user(account)
            data['name'] = account.username
            data['email'] = account.email
            data['access_token'] = str(refresh.access_token)
            data['refresh_token'] = str(refresh)
            return Response(data)
        else:
            data = serializer.errors 
            return Response(data, status = status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
def delete_view_jwt(request):
    if request.method == 'POST':
        request.user.auth_token.delete()        
        return Response(status = status.HTTP_204_NO_CONTENT)