from rest_framework import serializers
from delivery.core.models import *


class PedidosMS(serializers.ModelSerializer):
    class Meta:
        model = Pedidos
        fields = '__all__'

class ProdutosMS(serializers.ModelSerializer):
    class Meta:
        model = Produtos 
        fields = '__all__'

class CategoriaMS(serializers.ModelSerializer):
    class Meta:
        model = Categoria 
        fields = '__all__'

class PedidoProdutoMS(serializers.ModelSerializer):
    class Meta:
        model = PedidoProduto 
        fields = '__all__'
