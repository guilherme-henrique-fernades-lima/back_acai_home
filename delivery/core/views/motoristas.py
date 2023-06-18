import pandas as pd
from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from delivery.core.usecases.motoristas import CaseMotoristas


class MotoristasViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'], url_path='ativos')
    def motoristas_ativos(self, request):

        try:
            motoristas = CaseMotoristas()
            data = motoristas.get_all()

            if not data:
                return Response(data={'success': False, 'message': 'nenhum motorista ativo.'}, status=status.HTTP_404_NOT_FOUND)

            return Response(data=data, status=status.HTTP_200_OK)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': err}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='disponiveis')
    def motoristas_disponiveis(self, request):

        try:
            motoristas = CaseMotoristas()
            data = motoristas.get_disponiveis()

            if not data:
                return Response(data={'success': False, 'message': 'nenhum motorista disponivel.'}, status=status.HTTP_404_NOT_FOUND)

            return Response(data=data, status=status.HTTP_200_OK)

        except Exception as err:
            print("ERROR>>>", err)
            return Response(data={'success': False, 'message': err}, status=status.HTTP_400_BAD_REQUEST)
