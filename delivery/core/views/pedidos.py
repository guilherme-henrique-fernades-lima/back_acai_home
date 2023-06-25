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

        date = request.GET.get("date", datetime.now().date())

        try:
            pedido_case = CasePedidos()
            data = pedido_case.get_pedidos_pendentes(date)

            if not data:
                return Response(data={'success': False, 'message': 'nenhum pedido encontrado.'}, status=status.HTTP_404_NOT_FOUND)

            return Response(data=data, status=status.HTTP_200_OK)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='entrega')
    def pedidos_entrega(self, request):

        date = request.GET.get("date", datetime.now().date())

        try:
            pedido_rep = RepoPedidos()
            data = pedido_rep.get_entrega(date)

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
                pedido_rep = RepoPedidos()

                insert_error = []
                for pedido in data['pedidos']:

                    date = datetime.now()
                    payload = {
                        'data': date.date(),
                        'hora': date.time(),
                        'idPedido': pedido,
                        'status': 'ATRIBUIDO',
                        'cpf_motorista': data['cpf_motorista'],
                        'motorista': data['motorista'],
                        'cpf_user': data['cpf_user'],
                        'usuario': data['usuario']
                    }

                    atribuir_ped = pedido_rep.envia_pedido(payload)

                    if not atribuir_ped['success']:
                        insert_error += [pedido]

                return Response(data={"errors": insert_error}, status=status.HTTP_200_OK)

            return Response(data={'success': False, 'message': 'nenhum pedido informado.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='remover')
    def remover_pedidos(self, request):

        data = request.data

        try:
            if data:
                pedido_rep = RepoPedidos()

                insert_error = []
                for pedido in data['pedidos']:

                    date = datetime.now()
                    payload = {
                        'data': date.date(),
                        'hora': date.time(),
                        'idPedido': pedido,
                        'status': 'REMOVIDO',
                        'cpf_motorista': data['cpf_motorista'],
                        'motorista': data['motorista'],
                        'cpf_user': data['cpf_user'],
                        'usuario': data['usuario']
                    }

                    atribuir_ped = pedido_rep.remove_pedido(payload)

                    if not atribuir_ped['success']:
                        insert_error += [pedido]

                return Response(data={"errors": insert_error}, status=status.HTTP_200_OK)

            return Response(data={'success': False, 'message': 'nenhum pedido informado.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='finalizar')
    def finalizar_pedido(self, request):

        data = request.data

        try:
            if data:
                pedido_rep = RepoPedidos()

                date = datetime.now()
                payload = {
                    'data': date.date(),
                    'hora': date.time(),
                    'idPedido': data['idPedido'],
                    'status': 'CONCLUIDO',
                    'cpf_motorista': data['cpf_motorista'],
                    'motorista': data['motorista'],
                    'observacao': data['observacao']
                }

                finalizar = pedido_rep.finalizar_pedido(payload)

                if not finalizar['success']:
                    return Response(data={'success': False, 'message': finalizar['message']}, status=status.HTTP_400_BAD_REQUEST)

                return Response(data={'success': True, 'message': 'Pedido finalizado com sucesso!'}, status=status.HTTP_200_OK)

            return Response(data={'success': False, 'message': 'nenhum pedido informado.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)
