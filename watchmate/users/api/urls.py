from django.urls import path, include 
from rest_framework.authtoken.views import obtain_auth_token
from users.api.views import registration_view, logout,change_password, registration_view_jwt,delete_view_jwt



#jwt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('login/', obtain_auth_token, name='Login in user'),
    path('register/', registration_view, name = 'Registration'),
    path('logout/', logout, name = 'log-out'),
    path('change-password/', change_password, name = 'Change Password'),


    #jwt
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/signup/', registration_view_jwt, name='sign-up'),
    path('api/signout/', delete_view_jwt, name = 'sign-out'),
]

