from rest_framework import serializers
from django.contrib.auth import get_user_model
from users_app.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user
