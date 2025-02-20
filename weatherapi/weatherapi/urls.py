from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from api.views import WeatherAPIView
from users.views import CustomAuthToken, RegisterUserView

urlpatterns = [
    path("admin/", admin.site.urls),  

    # # Authentication endpoints
    # path("api/register/", RegisterUserView.as_view(), name="register"), 
    # path("api/login/", CustomAuthToken.as_view(), name="login"),  
    # path("api/token-auth/", obtain_auth_token, name="token-auth"),  

    # Weather API
    path("api/weather/<str:city_name>/", WeatherAPIView.as_view(), name="weather"),
]
