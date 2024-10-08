from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        #fields= '__all__'
        exclude = ['password']
        read_only_field = ['is_active', 'created']
