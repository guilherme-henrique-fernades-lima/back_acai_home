from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, username, password=None, nr_matricula=None, funcao=None, **kwargs):

        if username is None:
            raise TypeError('Informe o username.')
        if nr_matricula is None:
            raise TypeError('Informe a matricula.')

        user = self.model(username=username, nr_matricula=nr_matricula, funcao=funcao)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, nr_matricula, password):

        if password is None:
            raise TypeError('Superusers must have a password.')
        if nr_matricula is None:
            raise TypeError('Superusers must have an matricula.')
        if username is None:
            raise TypeError('Superusers must have an username.')

        user = self.create_user(username, nr_matricula, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255)
    email = models.EmailField(db_index=True, null=True, blank=True)
    nr_matricula = models.DecimalField(max_digits=8, decimal_places=0, unique=True)
    funcao = models.CharField(db_index=True, max_length=255)
    created = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'nr_matricula'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.nr_matricula}"
