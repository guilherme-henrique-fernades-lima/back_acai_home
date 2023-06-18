from django.db import connections
from delivery.core.utils import dictfetchall


class CasePedidos():

    def get_all(self, date, status_pedido, forma_pagamento):
        """ BUSCA TODOS OS PEDIDOS """

        filtros = ""
        if status_pedido: 
            filtros += "AND p.status = '{status}'"

        if forma_pagamento: 
            filtros += "AND p.formaPagamento = '{forma_pagamento}'"

        with connections["default"].cursor() as cursor:

            _sql = f"""
                SELECT p.id, p.data, p.hora, p.status, p.valor, p.formaPagamento, p.observacao, p.taxaentrega, p.trocopara, p.formaEntrega, p.celular,
                       pp.quantidade, pp.valorTotal, pp.numColher,
                       p2.descricao, p2.imagem, p2.titulo,
                       #c.cpf, c.email, c.sexo,
                       c.nome,
                       #e.cep, e.cidade, e.estado,
                       e.logradouro, e.numLogr, e.complLogr, e.pontoreferencia,
                       b.nome as "bairro"
                  FROM pedido p 
                  JOIN pedido_produto pp
                    ON p.id = pp.idPedido 
                  JOIN produto p2 
                    ON pp.idProduto = p2.id 
                  JOIN cliente c
                    ON p.idCliente = c.id
                  JOIN endereco e
                    ON p.idEndereco = e.id
                  JOIN bairro b
                    ON e.bairro = b.id 
                 WHERE p.data = '{date}' 
                 {filtros}
              ORDER BY p.data, p.hora
                  DESC;
            """

            cursor.execute(_sql)
            data = dictfetchall(cursor)

        return data if data else [] 

    def get_open_orders(self, date):
        """ BUSCA OS PEDIDOS PENDENTES """

        with connections["default"].cursor() as cursor:

            _sql = f"""
                SELECT p.id, p.data, p.hora, p.status, p.valor, p.formaPagamento, p.observacao, p.taxaentrega, p.trocopara, p.formaEntrega, p.celular,
                       pp.quantidade, pp.valorTotal, pp.numColher,
                       p2.descricao, p2.imagem, p2.titulo,
                       #c.cpf, c.email, c.sexo,
                       c.nome,
                       #e.cep, e.cidade, e.estado,
                       e.logradouro, e.numLogr, e.complLogr, e.pontoreferencia,
                       b.nome as "bairro"
                  FROM pedido p 
                  JOIN pedido_produto pp
                    ON p.id = pp.idPedido 
                  JOIN produto p2 
                    ON pp.idProduto = p2.id 
                  JOIN cliente c
                    ON p.idCliente = c.id
                  JOIN endereco e
                    ON p.idEndereco = e.id
                  JOIN bairro b
                    ON e.bairro = b.id 
                 WHERE p.data = '{date}'
                   AND p.formaEntrega = 1
                   AND p.status NOT IN ('CANCELADO', 'CONCLUIDO', 'ENVIADO') 
              ORDER BY p.data, p.hora
                  DESC;
            """

            cursor.execute(_sql)
            data = dictfetchall(cursor)

        return data if data else [] 
