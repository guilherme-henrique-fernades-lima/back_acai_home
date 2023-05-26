from rest_framework import serializers
from delivery.core.models import *


class PedidosMS(serializers.ModelSerializer):
    class Meta:
        model = Pedidos
        fields = '__all__'
