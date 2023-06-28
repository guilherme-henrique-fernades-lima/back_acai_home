import json
import asyncio
import socketio
import requests
import traceback
from django.utils import timezone

from delivery.settings import WS_URL


class SocketIO():

    sio = socketio.AsyncClient()

    @sio.event
    async def connect():
        print('connected to server')

    @sio.event
    async def disconnect():
        print('disconnected from server')

    @sio.on('update-input')
    async def on_message(self, data):
        print('I received a message!....', data)

    @sio.on('*')
    async def on_message(self, data, data2):
        print('I received a message 1!', data)
        print('I received a message 2!', data2)

    async def send_message(self, data):
        tp_evento = data['event']

        await self.sio.emit(tp_evento, data)

    async def start_server(self, data=None):

        resp = requests.get(WS_URL)
        await self.sio.connect(WS_URL)

        tasks = [
            self.send_message(data),
            self.sio.disconnect()
        ]

        await asyncio.gather(*tasks)

    def execute(self, data=None):

        print("DISPATCH EVENT WEBSOCKET>>>", data)

        try:
            asyncio.run(self.start_server(data=data))

        except Exception as err:
            print(traceback.print_exc())
            #raise
            pass

if __name__ == '__main__':
    from delivery.core.usecases.socket_io import SocketIO
    websocket = SocketIO()
    data = {'tp_evento': 'NOVO_PEDIDO', 'payload': {'abc': 'def'}}
    websocket.execute(data)
