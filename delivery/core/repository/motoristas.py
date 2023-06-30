from django.db import connections
from delivery.core.utils import dictfetchall


class RepoMotoristas():

    def get_all(self):
        """ BUSCA TODOS OS MOTORISTAS ATIVOS """

        with connections["default"].cursor() as cursor:

            _sql = f"""
                SELECT * FROM users_module_user u
                 WHERE is_active = True
                   AND funcao = 'ENTREGADOR';
            """

            cursor.execute(_sql)
            data = dictfetchall(cursor)

        return data if data else [] 

    def get_disponiveis(self):
        """ BUSCA TODOS OS MOTORISTAS DISPONIVEIS """

        with connections["default"].cursor() as cursor:

            _sql = f"""
                SELECT umu.*
                  FROM users_module_user umu
             LEFT JOIN pedido_entrega pe
                    ON umu.cpf = pe.cpf_motorista
                   AND pe.status = 'ATRIBUIDO'
                 WHERE umu.is_active = True
                   AND umu.funcao = 'entregador'
                   AND pe.cpf_motorista IS NULL;
            """

            cursor.execute(_sql)
            data = dictfetchall(cursor)

        return data if data else [] 

    def get_pedidos(self, date, cpf_motorista):
        """ BUSCA TODOS OS PEDIDOS ATRIBUIDO AO MOTORISTA """

        with connections["default"].cursor() as cursor:

            sql_pendentes = f"""
                SELECT pe.*, p.formaPagamento, p.id as "idPedido", p.data as "dt_pedido", p.valor, c.nome, c.celular, e.logradouro , e.numLogr, e.cidade, e.estado, b.nome as "bairro"
                  FROM pedido_entrega pe
                  JOIN pedido p
                    ON pe.idPedido = p.id
             LEFT JOIN cliente c
                    ON p.idCliente = c.id
             LEFT JOIN endereco e
                    ON p.idEndereco = e.id
             LEFT JOIN bairro b
                    ON e.bairro = b.id
                 WHERE pe.data = '{date}'
                   AND pe.status = 'ATRIBUIDO'
                   AND pe.cpf_motorista = '{cpf_motorista}';
            """

            sql_concluidos = f"""
                SELECT pe.*, p.formaPagamento, p.id as "idPedido", p.data as "dt_pedido", p.valor, c.nome, c.celular, e.logradouro , e.numLogr, e.cidade, e.estado, b.nome as "bairro"
                  FROM pedido_entrega pe
                  JOIN pedido p
                    ON pe.idPedido = p.id
             LEFT JOIN cliente c
                    ON p.idCliente = c.id
             LEFT JOIN endereco e
                    ON p.idEndereco = e.id
             LEFT JOIN bairro b
                    ON e.bairro = b.id
                 WHERE pe.data = '{date}'
                   AND pe.status = 'CONCLUIDO'
                   AND pe.cpf_motorista = '{cpf_motorista}';
            """

            cursor.execute(sql_pendentes)
            pendentes = dictfetchall(cursor)

            cursor.execute(sql_concluidos)
            concluidos = dictfetchall(cursor)

            data = {
                'pendentes': pendentes if pendentes else [],
                'concluidos': concluidos if concluidos else []
            }

        return data
