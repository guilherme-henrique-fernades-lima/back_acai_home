from datetime import datetime
from delivery.core.repository.motoristas import RepoMotoristas
from delivery.core.repository.pedidos import RepoPedidos


class CaseMotoristas():

    def __init__(self, rep=RepoMotoristas(), rep_pedidos=RepoPedidos()):
        self.motoristas_rep = rep
        self.pedidos_rep = rep_pedidos

    def add_produtos_motorista(self, date, cpf_motorista):

        pedidos = self.motoristas_rep.get_pedidos(date, cpf_motorista)
        dt_pedido = pedidos['pendentes'][0]['dt_pedido'] if pedidos['pendentes'][0] else pedidos['concluidos'][0]['dt_pedido']
        produtos = self.pedidos_rep.get_all_produtos(dt_pedido)

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

            pendentes = []
            for ped in pedidos['pendentes']:
                ped.update({'produtos': new_produtos[ped['idPedido']]})
                pendentes += [ped]

            concluidos = []
            for ped in pedidos['concluidos']:
                ped.update({'produtos': new_produtos[ped['idPedido']]})
                concluidos += [ped]

            return {'pendentes': pendentes, 'concluidos': concluidos} 

        except Exception as err:
            print("Ocorreu um erro ao tentar associar os produtos!", err)
