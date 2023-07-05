import json
import pandas as pd
from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from delivery.core.models import Pedidos
from delivery.core.serializer import PedidosMS
from delivery.core.usecases.pedidos import CasePedidos
from delivery.core.repository.pedidos import RepoPedidos
from delivery.core.utils import dispatch_event_socket


class PedidosViewSet(viewsets.ModelViewSet):
    queryset = Pedidos.objects.all()
    serializer_class = PedidosMS
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        return serializer

    def list(self, request):

        date = request.GET.get("date", datetime.now().date())
        status_pedido = request.GET.get("status")
        forma_pagamento = request.GET.get("tp_pag")

        try:
            pedido_case = CasePedidos()
            data = pedido_case.get_pedidos(date, status_pedido, forma_pagamento)

            if not data:
                return Response(data={'success': False, 'message': 'nenhum pedido encontrado.'}, status=status.HTTP_404_NOT_FOUND)

            df_pedidos = pd.DataFrame(data)
            contagem_status = df_pedidos['status'].value_counts()
            total = contagem_status.sum()
            contagem_status['TOTAL'] = total

            new_data = {'data': data, 'status': contagem_status.to_dict()}

            return Response(data=new_data, status=status.HTTP_200_OK)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='pendentes')
    def pedidos_pendentes(self, request):

        bairro = request.GET.get("bairro")

        try:
            pedido_case = CasePedidos()
            data = pedido_case.get_pedidos_pendentes(bairro)

            if not data:
                return Response(data={'success': False, 'message': 'nenhum pedido encontrado.'}, status=status.HTTP_404_NOT_FOUND)

            df_pedidos = pd.DataFrame(data)
            contagem_status = df_pedidos['status'].value_counts()
            total = contagem_status.sum()
            contagem_status['TOTAL'] = total

            new_data = {'data': data, 'status': contagem_status.to_dict()}

            return Response(data=new_data, status=status.HTTP_200_OK)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='entrega')
    def pedidos_entrega(self, request):

        motorista = request.GET.get("cpf_motorista")

        try:
            pedido_rep = RepoPedidos()
            data = pedido_rep.get_entrega(motorista)

            if not data:
                return Response(data={'success': False, 'message': 'nenhum pedido encontrado.'}, status=status.HTTP_404_NOT_FOUND)

            return Response(data=data, status=status.HTTP_200_OK)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='enviar')
    def enviar_pedidos(self, request):

        data = request.data

        try:
            if data:
                pedido_case = CasePedidos()
                response = pedido_case.enviar_pedido(data)

                dispatch_event_socket(tp_evento="NEW_ORDER_DELIVERY", payload=data)
                return Response(data={"errors": response}, status=status.HTTP_200_OK)

            return Response(data={'success': False, 'message': 'nenhum pedido informado.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='remover')
    def remover_pedidos(self, request):

        data = request.data

        try:
            if data:
                pedido_case = CasePedidos()
                response = pedido_case.remover_pedido(data)

                dispatch_event_socket(tp_evento="REMOVE_ORDER_DELIVERY", payload=data)
                return Response(data={"errors": response}, status=status.HTTP_200_OK)

            return Response(data={'success': False, 'message': 'nenhum pedido informado.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='finalizar')
    def finalizar_pedido(self, request):

        data = request.data

        try:
            if data:
                pedido_case = CasePedidos()
                response = pedido_case.finalizar_pedido(data)

                dispatch_event_socket(tp_evento="FINISH_ORDER_DELIVERY", payload=data)
                return Response(data=response, status=status.HTTP_200_OK)

            return Response(data={'success': False, 'message': 'nenhum pedido informado.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='bairros')
    def get_bairros(self, request):

        try:
            pedido_rep = RepoPedidos()
            response = pedido_rep.get_bairros()

            return Response(data=response, status=status.HTTP_200_OK)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)
