import websockets
import json
from sinric.command._mainqueue import queue
import asyncio
import time


class SinricPro:

    def __init__(self, apiKey, deviceId):
        self.apiKey = apiKey
        self.deviceIds = deviceId
        self.connection = None
        pass

    async def connect(self):  # Producer
        self.connection = await websockets.client.connect('ws://23.95.122.232:3001',
                                                          extra_headers={'Authorization': self.apiKey,
                                                                         'deviceids': self.deviceIds})
        if self.connection.open:
            print('Client Connected')
            return self.connection

    async def sendMessage(self, message):
        await self.connection.send(message)

    async def receiveMessage(self, connection):
        while True:
            try:
                message = await connection.recv()
                queue.put(json.loads(message))
                print(queue.qsize(), ' : Queue Size')
                await self.handle()
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break

    async def heartbeat(self, connection):
        while True:
            try:
                await connection.send('H')
                await asyncio.sleep(5)
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break

    async def handle(self):
        while queue.qsize() > 0:
            print(queue.get())