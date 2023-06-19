from django.db import connections
from delivery.core.utils import dictfetchall


class CaseMotoristas():

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
                SELECT u.*
                  FROM users_module_user u
                  JOIN pedido_entrega ped
                    ON u.cpf = ped.cpf_motorista
                 WHERE u.is_active = True
                   AND u.funcao = 'ENTREGADOR'
                   AND ped.status NOT IN ('ATRIBUIDO');
            """

            cursor.execute(_sql)
            data = dictfetchall(cursor)

        return data if data else [] 

    def get_pedidos(self, date, cpf_motorista):
        """ BUSCA TODOS OS PEDIDOS ATRIBUIDO AO MOTORISTA """

        with connections["default"].cursor() as cursor:

            sql_pendentes = f"""
                SELECT * FROM pedido_entrega
                WHERE data = '{date}'
                AND status = 'ATRIBUIDO'
                AND cpf_motorista = {cpf_motorista};
            """

            sql_concluidos = f"""
                SELECT * FROM pedido_entrega
                WHERE data = '{date}'
                AND status = 'CONCLUIDO'
                AND cpf_motorista = {cpf_motorista};
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
