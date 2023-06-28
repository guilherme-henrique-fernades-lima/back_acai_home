import pandas as pd
from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from delivery.core.usecases.motoristas import CaseMotoristas
from delivery.core.repository.motoristas import RepoMotoristas


class MotoristasViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['get'], url_path='ativos')
    def motoristas_ativos(self, request):

        try:
            motoristas = RepoMotoristas()
            data = motoristas.get_all()

            if not data:
                return Response(data={'success': False, 'message': 'nenhum motorista ativo.'}, status=status.HTTP_404_NOT_FOUND)

            return Response(data=data, status=status.HTTP_200_OK)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='disponiveis')
    def motoristas_disponiveis(self, request):

        try:
            motoristas = RepoMotoristas()
            data = motoristas.get_disponiveis()

            if not data:
                return Response(data={'success': False, 'message': 'nenhum motorista disponivel.'}, status=status.HTTP_404_NOT_FOUND)

            return Response(data=data, status=status.HTTP_200_OK)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='pedidos')
    def pedidos_motorista(self, request):

        date = request.GET.get("date", datetime.now().date())
        motorista = request.GET.get("cpf_motorista")

        try:
            motoristas = CaseMotoristas()
            data = motoristas.add_produtos_motorista(date=date, cpf_motorista=motorista)

            if not data:
                return Response(data={'success': False, 'message': 'nenhum pedido atribuido ao motorista.'}, status=status.HTTP_404_NOT_FOUND)

            return Response(data=data, status=status.HTTP_200_OK)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)
