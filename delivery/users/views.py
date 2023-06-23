from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from delivery.users.serializers import UserSerializer

from django.contrib.auth import get_user_model
User = get_user_model()


class UserViewSet(viewsets.ViewSet):
    """
    Classe utilizada para lidar com requisições de usuários.
    """

    permission_classes = (IsAuthenticated,)

    def list(self, request):

        try:
            users = User.objects.all()
            data = UserSerializer(users, many=True).data
            return Response(data=data, status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):

        try:
            user = User.objects.get(id=pk)
            data = UserSerializer(user).data
            return Response(data=data, status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):

        try:
            data = request.data

            user = User.objects.get(cpf=data['cpf'])
            serializer = UserSerializer(user, data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):

        try:
            user = User.objects.get(id=pk)
            user.delete()
            return Response(status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], url_path='change/password')
    def change_pwd(self, request):

        try:
            data = request.data
            user = User.objects.get(cpf=data['cpf'])

            if user.check_password(data['oldPassword']):
                user.set_password(data['password'])
                user.save()

                return Response(status=status.HTTP_200_OK)

            return Response(status=status.HTTP_401_UNAUTHORIZED)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
