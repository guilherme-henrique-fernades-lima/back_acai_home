from django.db import connections
from delivery.core.utils import dictfetchall


class RepoPedidos():


    def get_all(self, date, status_pedido, forma_pagamento):
        """ BUSCA TODOS OS PEDIDOS """

        filtros = ""
        if status_pedido: 
            filtros += f"AND p.status = '{status}'"

        if forma_pagamento: 
            filtros += f"AND p.formaPagamento = '{forma_pagamento}'"

        with connections["default"].cursor() as cursor:

            _sql = f"""
                SELECT p.id, p.data, p.hora, p.status, p.valor, p.formaPagamento, p.observacao, p.taxaentrega, p.trocopara, p.formaEntrega, p.celular,
                       #c.cpf, c.email, c.sexo,
                       c.nome,
                       #e.cep, e.cidade, e.estado,
                       e.logradouro, e.numLogr, e.complLogr, e.pontoreferencia,
                       b.nome as "bairro"
                  FROM pedido p
                  LEFT JOIN cliente c
                    ON p.idCliente = c.id
                  LEFT JOIN endereco e
                    ON p.idEndereco = e.id
                  LEFT JOIN bairro b
                    ON e.bairro = b.id
                 WHERE p.data = '{date}'
                 {filtros}
              ORDER BY p.data, p.hora
                  DESC;
            """

            cursor.execute(_sql)
            data = dictfetchall(cursor)

        return data if data else []

    def get_all_produtos(self, date):

        with connections["default"].cursor() as cursor:
            _sql = f"""
                SELECT pp.idPedido, pp.quantidade, pp.valorTotal, pp.obs, pp.numColher,
                       p2.descricao, p2.valor, p2.imagem, p2.titulo
                  FROM pedido p
                  JOIN pedido_produto pp
                    ON p.id = pp.idPedido
                  JOIN produto p2
                    ON pp.idProduto = p2.id
                 WHERE data = '{date}';
            """

            cursor.execute(_sql)
            data = dictfetchall(cursor)

        return data if data else []

    def get_open_orders(self, date):
        """ BUSCA OS PEDIDOS PENDENTES """

        with connections["default"].cursor() as cursor:

            _sql = f"""
                SELECT p.id, p.data, p.hora, p.status, p.valor, p.formaPagamento, p.observacao, p.taxaentrega, p.trocopara, p.formaEntrega, p.celular,
                       #c.cpf, c.email, c.sexo,
                       c.nome,
                       #e.cep, e.cidade, e.estado,
                       e.logradouro, e.numLogr, e.complLogr, e.pontoreferencia,
                       b.nome as "bairro"
                  #FROM pedido p
                  FROM gtech_pedidos p
                  LEFT JOIN cliente c
                    ON p.idCliente = c.id
                  LEFT JOIN endereco e
                    ON p.idEndereco = e.id
                  LEFT JOIN bairro b
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

    def get_entrega(self, date):
        """ BUSCA OS PEDIDOS EM ROTA DE ENTREGA """

        with connections["default"].cursor() as cursor:

            _sql = f"""
                SELECT * FROM pedido_entrega pe
                 WHERE pe.status NOT IN ('REMOVIDO', 'CONCLUIDO')
                   AND pe.data = '{date}';
            """

            cursor.execute(_sql)
            data = dictfetchall(cursor)

        return data if data else [] 

    def enviar_pedido(self, payload):
        """ ADICIONA PEDIDO PARA ROTA DE ENTREGA """

        sql_insert = f"""
            INSERT INTO pedido_entrega (idPedido, cliente, celular, data, hora, status, cpf_motorista, motorista, cpf_user, usuario)
                 VALUES ({payload['idPedido']}, '{payload['cliente']}', '{payload['celular']}', '{payload['data']}', '{payload['hora']}', '{payload['status']}',
                         {payload['cpf_motorista']}, '{payload['motorista']}', {payload['cpf_user']}, '{payload['usuario']}');
        """

        sql_update = f"""
            UPDATE gtech_pedidos gped
               SET gped.status = 'ENVIADO'
             WHERE gped.id = {payload['idPedido']};
        """

        try:
            with connections["default"].cursor() as cursor:
                cursor.execute(sql_insert)

                if cursor.rowcount == 1:
                    cursor.execute(sql_update)

                    if cursor.rowcount == 1:
                        connections["default"].commit()

                    else:
                        connections["default"].rollback()
                        return {'success': False, 'message': 'operacao falho ao realizar o update!'} 

                else:
                    connections["default"].rollback()
                    return {'success': False, 'message': 'operacao falho ao realizar o insert!'} 

        except Exception as e:
            connections["default"].rollback()
            return f'Erro: {str(e)}'

        return {'success': True, 'message': 'operacao realizada com sucesso!'} 

    def remover_pedido(self, payload):
        """ REMOVE PEDIDO DE ROTA ENTREGA """

        sql_insert = f"""
            INSERT INTO pedido_entrega (idPedido, cliente, celular, data, hora, status, cpf_motorista, motorista, cpf_user, usuario)
                 VALUES ({payload['idPedido']}, '{payload['cliente']}', '{payload['celular']}', '{payload['data']}', '{payload['hora']}', '{payload['status']}',
                         {payload['cpf_motorista']}, '{payload['motorista']}', {payload['cpf_user']}, '{payload['usuario']}');
        """

        sql_update = f"""
            UPDATE gtech_pedidos gped
               SET gped.status = 'EM_ABERTO'
             WHERE gped.id = {payload['idPedido']};
        """

        try:
            with connections["default"].cursor() as cursor:
                cursor.execute(sql_insert)

                if cursor.rowcount == 1:
                    cursor.execute(sql_update)

                    if cursor.rowcount == 1:
                        connections["default"].commit()

                    else:
                        connections["default"].rollback()
                        return {'success': False, 'message': 'operacao falho ao realizar o update!'}

                else:
                    connections["default"].rollback()
                    return {'success': False, 'message': 'operacao falho ao realizar o insert!'}

        except Exception as e:
            connections["default"].rollback()
            return f'Erro: {str(e)}'

        return {'success': True, 'message': 'operacao realizada com sucesso!'}

    def finalizar_pedido(self, payload):
        """ FINALIZA PEDIDO DA ROTA DE ENTREGA """

        sql_insert = f"""
            INSERT INTO pedido_entrega (idPedido, cliente, celular, data, hora, status, cpf_motorista, motorista, cpf_user, usuario)
                 VALUES ({payload['idPedido']}, '{payload['cliente']}', '{payload['celular']}', '{payload['data']}', '{payload['hora']}', '{payload['status']}',
                         {payload['cpf_motorista']}, '{payload['motorista']}', NULL, NULL);
        """

        sql_update = f"""
            UPDATE gtech_pedidos gped
               SET gped.status = 'CONCLUIDO', gped.observacao = '{payload['observacao']}'
             WHERE gped.id = {payload['idPedido']};
        """

        try:
            with connections["default"].cursor() as cursor:
                cursor.execute(sql_insert)

                if cursor.rowcount == 1:
                    cursor.execute(sql_update)

                    if cursor.rowcount == 1:
                        connections["default"].commit()

                    else:
                        connections["default"].rollback()
                        return {'success': False, 'message': 'operacao falho ao realizar o update!'}

                else:
                    connections["default"].rollback()
                    return {'success': False, 'message': 'operacao falho ao realizar o insert!'}

        except Exception as e:
            connections["default"].rollback()
            return f'Erro: {str(e)}'

        return {'success': True, 'message': 'operacao realizada com sucesso!'}

    def get_cliente_from_pedido(self, id_pedido):
        """ BUSCA INFORMACOES DO CLIENTE ATRAVES DO idPedido """

        with connections["default"].cursor() as cursor:

            _sql = f"""
                SELECT c.* FROM pedido p 
                  JOIN cliente c
                    ON p.idCliente = c.id
                 WHERE p.id = {id_pedido};
            """

            cursor.execute(_sql)
            data = dictfetchall(cursor)

        return data[0] if data else [] 
