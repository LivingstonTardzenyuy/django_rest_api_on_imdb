from rest_framework.decorators import api_view 
from users.api.serializers import RegistrationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

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
    
