from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from delivery.core.models import *
from delivery.core.serializer import *


"""
class PedidosViewSet(viewsets.ModelViewSet):
    queryset = Pedidos.objects.all()
    serializer_class = PedidosMS
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        return serializer

    @action(detail=False, methods=['get'], url_path='pedidos')
    def pedidos(self, request):

        data = []

        if not data:
            return Response(data={'success': False, 'message': 'Sem motivos encontrados.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(data=data, status=status.HTTP_200_OK)
"""

class PedidosViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['get'], url_path='teste')
    def pedidos(self, request):

        data = {'data': 'retornando os pedidos...'}

        return Response(data=data, status=status.HTTP_200_OK)
