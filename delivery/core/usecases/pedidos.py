from datetime import datetime
from delivery.core.repository.pedidos import RepoPedidos


class CasePedidos():


    def __init__(self, rep=RepoPedidos()):
        self.pedidos_rep = rep

    def get_pedidos(self, date, status_pedido, forma_pagamento):

        pedidos = self.pedidos_rep.get_all(date, status_pedido, forma_pagamento)

        if not pedidos:
            return pedidos

        data = self.associar_produtos_pedido(pedidos)
        data_pedidos = self.associar_entregas(data)

        return data_pedidos

    def get_pedidos_pendentes(self, bairro):

        pedidos = self.pedidos_rep.get_open_orders(bairro)

        if not pedidos:
            return pedidos

        data = self.associar_produtos_pedido(pedidos)

        return data

    def associar_produtos_pedido(self, pedidos):

        pedidos_array = [x['id'] for x in pedidos]
        produtos = self.pedidos_rep.get_all_produtos(pedidos_array)

        if not produtos:
            return pedidos 

        try:
            new_produtos = {}
            for item in produtos:
                if new_produtos.get(item['idPedido']):
                    new_produtos[item['idPedido']] += [item]
                else:
                    new_produtos.update({item['idPedido']: [item]})

            data = []
            for ped in pedidos:
                ped.update({'produtos': new_produtos[ped['id']]})
                data += [ped]

            return data

        except Exception as err:
            print("Ocorreu um erro ao tentar associar os produtos!", err)

    def associar_entregas(self, data):

        pedidos_array = [x['id'] for x in data]
        entregas = self.pedidos_rep.get_info_entrega(pedidos_array)

        if not entregas:
            for x in data:
                x['entrega'] = {}
            return data

        try:

            new_pedido = {}
            for item in entregas:
                new_pedido.update({item['idPedido']: item})

            new_data = []
            for ped in data:
                if new_pedido.get(ped['id']):
                    ped.update({'entrega': new_pedido[ped['id']]})

                else:
                    ped.update({'entrega': {}})

                new_data += [ped]

            return new_data

        except Exception as err:
            print("Ocorreu um erro ao tentar associar a entrega!", err)

    def enviar_pedido(self, data):

        insert_error = []
        for id_pedido in data['pedidos']:

            payload = self.create_payload_entrega(id_pedido=id_pedido, data=data, status="ATRIBUIDO")
            atribuir_ped = self.pedidos_rep.enviar_pedido(payload)

            if not atribuir_ped.get('success'):
                insert_error += [id_pedido]

        return insert_error

    def remover_pedido(self, data):

        insert_error = []
        for id_pedido in data['pedidos']:

            payload = self.create_payload_entrega(id_pedido=id_pedido, data=data, status="REMOVIDO")
            atribuir_ped = self.pedidos_rep.remover_pedido(payload)

            if not atribuir_ped.get('success'):
                insert_error += [id_pedido]

        return insert_error

    def finalizar_pedido(self, data):

        payload = self.create_payload_entrega(id_pedido=data['idPedido'], data=data, status="FINALIZADO")
        finalizar_ped = self.pedidos_rep.finalizar_pedido(payload)

        return finalizar_ped

    def concluir_pedido(self, data):

        payload = self.create_payload_entrega(id_pedido=data['idPedido'], data=data, status="CONCLUIDO")
        finalizar_ped = self.pedidos_rep.concluir_pedido(payload)

        return finalizar_ped

    def create_payload_entrega(self, id_pedido=None, data=None, status=None):

        cliente = self.pedidos_rep.get_cliente_from_pedido(id_pedido=id_pedido)
        date = datetime.now()

        payload = {
            'data': date.date(),
            'hora': date.time().strftime("%H:%M:%S"),
            'idPedido': id_pedido,
            'cliente': cliente.get('nome'),
            'celular': cliente.get('celular'),
            'status': status,
            'cpf_motorista': data.get('cpf_motorista'),
            'motorista': data.get('motorista'),
            'cpf_user': data.get('cpf_user'),
            'usuario': data.get('usuario')
        }

        if data.get('observacao'):
            payload.update({'observacao': data['observacao']})

        return payload
