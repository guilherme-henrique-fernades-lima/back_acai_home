from django.db import models


class Pedidos(models.Model):
    id = models.BigAutoField(primary_key=True)
    idCliente = models.BigIntegerField(null=True)
    data = models.DateField(null=True)
    hora = models.TimeField(null=True)
    status = models.CharField(max_length=20, null=True)
    valor = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    formaPagamento = models.CharField(max_length=20, null=True)
    observacao = models.CharField(max_length=255, null=True)
    idEmpresa = models.BigIntegerField(null=True)
    taxaentrega = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    trocopara = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    formaEntrega = models.IntegerField(null=True)
    valorcartao = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    idEndereco = models.BigIntegerField(null=True)
    numColher = models.IntegerField(default=0)
    celular = models.CharField(max_length=20, null=True)

    class Meta:
        managed = False
        db_table = 'pedido'
