#from ecommerce.users.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers
#from rolepermissions.permissions import available_perm_status

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields= '__all__'
        read_only_field = ['is_active', 'created']
