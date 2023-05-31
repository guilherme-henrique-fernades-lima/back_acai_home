from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from delivery.core.models import Pedidos 
from delivery.core.serializer import PedidosMS 

import pandas as pd
from datetime import datetime


class PedidosViewSet(viewsets.ModelViewSet):
    queryset = Pedidos.objects.all()
    serializer_class = PedidosMS
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        return serializer

    def list(self, request):

        date = request.GET.get("date", datetime.now().date())

        try:
            pedidos = Pedidos.objects.filter(data=date).order_by('-data', '-hora')
            data = PedidosMS(pedidos, many=True).data

            if not data:
                return Response(data={'success': False, 'message': 'nenhum pedido encontrado.'}, status=status.HTTP_404_NOT_FOUND)

            df_pedidos = pd.DataFrame(data)
            contagem_status = df_pedidos['status'].value_counts()

            new_data = {'data': data, 'status': contagem_status.to_dict()}

            return Response(data=new_data, status=status.HTTP_200_OK)

        except Exception as err:
            return Response(data={'success': False, 'message': err}, status=status.HTTP_400_BAD_REQUEST)
