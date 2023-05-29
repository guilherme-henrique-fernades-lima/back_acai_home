import asyncio
import socketio
import requests
import traceback
import json
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

        tasks = [asyncio.create_task(self.send_message(data))]
        await asyncio.gather(*tasks)

    def execute(self, data=None):

        print("DATA>>>", data, "\n", WS_URL)

        try:

            if data['tp_evento'] == 'ws-name':
                new_data = {"event":"NAME", "payload": data['payload']}

            asyncio.get_event_loop().run_until_complete(self.start_server(data=new_data))
            asyncio.get_event_loop().run_until_complete(self.sio.disconnect())

        except Exception as err:
            print(traceback.print_exc())
            raise

if __name__ == '__main__':
    from delivery.core.usecases.socket_io import SocketIO
    websocket = SocketIO()
    data = {'tp_evento': 'ws-name', 'payload': {}}
    websocket.execute(data)
