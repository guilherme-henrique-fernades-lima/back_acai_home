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

class Categoria(models.Model):
    id = models.BigAutoField(primary_key=True)
    descricao = models.CharField(max_length=255, null=True)
    ativo = models.IntegerField(default=1)
    idEmpresa = models.BigIntegerField(null=True)

    class Meta:
        managed = False
        db_table = 'categoria'

class Produtos(models.Model):
    id = models.BigAutoField(primary_key=True)
    descricao = models.CharField(max_length=500, null=True)
    valor = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    validade = models.DateField(null=True)
    ativo = models.IntegerField(null=True)
    imagem = models.CharField(max_length=255, null=True)
    idCategoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, db_column='idCategoria', related_name='produtos')
    titulo = models.CharField(max_length=255, null=True)
    idEmpresa = models.BigIntegerField(null=True)
    limiteopc = models.IntegerField(null=True)
    exibeopc = models.IntegerField(default=10)

    class Meta:
        managed = False
        db_table = 'produto'

class PedidoProduto(models.Model):
    id = models.BigAutoField(primary_key=True)
    idPedido = models.BigIntegerField(null=True)
    idProduto = models.BigIntegerField(null=True)
    quantidade = models.IntegerField(null=True)
    valorTotal = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    obs = models.CharField(max_length=255, null=True)
    numColher = models.IntegerField(default=1)
    #pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, related_name='produtos')

    class Meta:
        managed = False
        db_table = 'pedido_produto'
