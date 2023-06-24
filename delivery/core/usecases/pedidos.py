from delivery.core.repository.pedidos import RepoPedidos


class CasePedidos():


    def __init__(self, rep=RepoPedidos()):
        self.pedidos_rep = rep

    def get_pedidos(self, date, status_pedido, forma_pagamento):

        pedidos = self.pedidos_rep.get_all(date, status_pedido, forma_pagamento)
        produtos = self.pedidos_rep.get_all_produtos(date)

        data = self.associar_produtos_pedido(pedidos, produtos)

        return data

    def get_pedidos_pendentes(self, date):

        pedidos = self.pedidos_rep.get_open_orders(date)
        produtos = self.pedidos_rep.get_all_produtos(date)

        data = self.associar_produtos_pedido(pedidos, produtos)

        return data

    def associar_produtos_pedido(self, pedidos, produtos):

        if not pedidos:
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
