# user_management/views.py
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
import uuid
from .serializers import UserRegisterSerializer, UserSerializer, CustomTokenObtainPairSerializer

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token view that uses our serializer"""
    serializer_class = CustomTokenObtainPairSerializer

class UserRegisterView(generics.CreateAPIView):
    """View for user registration"""
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create verification token
        verification_token = str(uuid.uuid4())
        
        # Save user with token
        user = serializer.save(verification_token=verification_token)
        
        # Here you would typically send email verification
        # For this project, we'll just assume it's sent
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"detail": "User created successfully. Please check your email for verification."},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class VerifyEmailView(APIView):
    """View for email verification"""
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request, token):
        try:
            user = User.objects.get(verification_token=token)
            if not user.is_email_verified:
                user.is_email_verified = True
                user.verification_token = None  # Clear the token
                user.save()
                return Response({"detail": "Email verified successfully."}, status=status.HTTP_200_OK)
            return Response({"detail": "Email already verified."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Invalid verification token."}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    """View for retrieving and updating user profile"""
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        return self.request.user