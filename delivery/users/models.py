from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, username=None, password=None, cpf=None, funcao=None, \
                          email=None, cep=None, logradouro=None, numLogr=None, \
                          complLogr=None, bairro=None, cidade=None, estado=None, \
                          avatar=None, observacao=None, **kwargs):

        if username is None:
            raise TypeError('Informe o username.')
        if cpf is None:
            raise TypeError('Informe o CPF.')

        user = self.model(username=username, cpf=cpf, funcao=funcao, \
                          email=email, cep=cep, logradouro=logradouro, \
                          numLogr=numLogr, complLogr=complLogr, bairro=bairro, \
                          cidade=cidade, estado=estado, avatar=avatar, observacao=observacao)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, cpf, password):

        if password is None:
            raise TypeError('Superusers must have a password.')
        if cpf is None:
            raise TypeError('Superusers must have an CPF.')
        if username is None:
            raise TypeError('Superusers must have an username.')

        user = self.create_user(username, cpf, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255)
    email = models.EmailField(db_index=True, null=True, blank=True)
    cpf = models.DecimalField(max_digits=11, decimal_places=0, unique=True)
    funcao = models.CharField(db_index=True, max_length=255)
    created = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    cep = models.CharField(max_length=20, null=True)
    logradouro = models.CharField(max_length=255, null=True)
    numLogr = models.CharField(max_length=255, null=True)
    complLogr = models.CharField(max_length=255, null=True)
    bairro = models.CharField(max_length=255, null=True)
    cidade = models.CharField(max_length=255, null=True)
    estado = models.CharField(max_length=10, null=True)
    avatar = models.CharField(max_length=100, null=True)
    observacao = models.TextField(null=True)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.cpf}"
