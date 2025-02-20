from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .permissions import IsManager
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class ManagerOnlyView(APIView):
    # permission_classes = [IsAuthenticated, IsManager]

    def get(self, request):
        return Response({'message':'Hello, Manager!'})


User = get_user_model()

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # Anyone can register
    serializer_class = UserSerializer

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "username": user.username, "city": user.city.name if user.city else None})