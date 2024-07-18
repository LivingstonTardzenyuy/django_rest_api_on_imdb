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
        if serializer.is_valid():
            response = {}
            
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)      

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
