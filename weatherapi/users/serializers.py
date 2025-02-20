from rest_framework import serializers
from django.contrib.auth import get_user_model
from cities.models import City  

User = get_user_model()

# Serializer for registration 
class UserRegisterSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "city"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# Serializer for user details
class UserSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(read_only=True)  # City cannot be changed after registration

    class Meta:
        model = User
        fields = ["username", "email", "city"]
