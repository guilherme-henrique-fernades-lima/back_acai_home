"""
from rest_framework import serializers
from delivery.core.models import *

class TestMS(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'
"""
