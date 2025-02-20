import requests
from datetime import timedelta
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Weather
from cities.models import City
from .serializers import WeatherSerializer
from django.conf import settings

from django.contrib.auth.decorators import login_required
# from .weather_service import get_weather_data

class WeatherAPIView(APIView):
    def get(self, request, city_name):
        city, _ = City.objects.get_or_create(name=city_name)  

        # Checking if data is obsolote or not
        ten_minutes_ago = now() - timedelta(minutes=10)
        weather = Weather.objects.filter(city=city, timestamp__gte=ten_minutes_ago).first()

        if not weather:
            # Retrieving data from OpenWeatherAPI
            api_key = settings.OPENWEATHER_API_KEY
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
            response = requests.get(url)

            if response.status_code != 200:
                return Response({"error": "Failed to fetch weather data"}, status=status.HTTP_400_BAD_REQUEST)

            data = response.json()
            weather, _ = Weather.objects.update_or_create(
                city=city,
                defaults={
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "timestamp": now(),
                },
            )

        serializer = WeatherSerializer(weather)
        return Response(serializer.data, status=status.HTTP_200_OK)

# from datetime import timedelta
# from django.utils.timezone import now
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from django.conf import settings
# import requests

# from .models import Weather
# from cities.models import City
# from .serializers import WeatherSerializer

# class WeatherAPIView(APIView):
#     permission_classes = []  # Require user authentication

#     def get(self, request):
#         # Get the user's registered city
#         user = request.user
#         if not user.city:
#             return Response({"error": "User has no city assigned."}, status=status.HTTP_400_BAD_REQUEST)

#         city = user.city

#         # Check if recent weather data exists (last 10 minutes)
#         ten_minutes_ago = now() - timedelta(minutes=10)
#         weather = Weather.objects.filter(city=city, timestamp__gte=ten_minutes_ago).first()

#         if not weather:
#             # Fetch fresh weather data from OpenWeatherAPI
#             api_key = settings.OPENWEATHER_API_KEY
#             url = f"http://api.openweathermap.org/data/2.5/weather?q={city.name}&appid={api_key}&units=metric"
#             response = requests.get(url)

#             if response.status_code != 200:
#                 return Response({"error": "Failed to fetch weather data"}, status=status.HTTP_400_BAD_REQUEST)

#             data = response.json()
#             weather, _ = Weather.objects.update_or_create(
#                 city=city,
#                 defaults={
#                     "temperature": data["main"]["temp"],
#                     "description": data["weather"][0]["description"],
#                     "timestamp": now(),
#                 },
#             )

#         serializer = WeatherSerializer(weather)
#         return Response(serializer.data, status=status.HTTP_200)
