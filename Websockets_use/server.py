import asyncio
from concurrent.futures import ProcessPoolExecutor
import time
import websockets
import json

class Server():
    def __init__(self):
        self.port = 9905
        self.host = 'localhost'
        self.sleep = 1

    async def consumer(self, message, queue):
        print('request dict from client', message)
        await queue.put(message)
        print('Client connect')

    async def listen(self, websocket, path, queue):
        print('ready to listen')
        async for message in websocket:
            await self.consumer(message, queue)

    async def send(self, websocket, path, queue): 
        while True:
            time.sleep(self.sleep)
            try:
                request_dict = await asyncio.wait_for(queue.get(), timeout=0.1)
                request_dict = json.loads(request_dict)
            except asyncio.TimeoutError:
                pass
                request = request_dict
                message = json.dumps(request)
                #print('mes is ready to be send')
                await websocket.send(message)  
                #print('mes was sent') 
        
    async def handler(self, websocket, path):
        queue = asyncio.Queue()

        listen_task = asyncio.ensure_future(self.listen(websocket, path, queue))
        send_task = asyncio.ensure_future(self.send(websocket, path, queue))

        done, pending = await asyncio.wait(
            [send_task, listen_task],
            return_when=asyncio.ALL_COMPLETED,)
        for task in pending:
            task.cancel()

    def sub_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(websockets.serve(self.handler, self.host, self.port))
        loop.run_forever()

    async def start(self, executor):
        await asyncio.get_event_loop().run_in_executor(executor, self.sub_loop)


if __name__ == '__main__':
    server = Server()
    executor = ProcessPoolExecutor()
    asyncio.get_event_loop().run_until_complete(server.start(executor))
    