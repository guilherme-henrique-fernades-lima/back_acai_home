from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from delivery.users.serializers import UserSerializer

from django.contrib.auth import get_user_model

User = get_user_model()

class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(timezone.localtime(), self.user)

        return data

class RegistrationSerializer(UserSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
    cpf = serializers.CharField(max_length=11, write_only=True, required=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):

        try:
            user = User.objects.get(email=validated_data['cpf'])

        except ObjectDoesNotExist:
            user = User.objects.create_user(**validated_data)

        return user
