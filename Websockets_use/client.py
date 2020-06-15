import asyncio
from concurrent.futures import ProcessPoolExecutor
import websockets
import time
import json

async def consumer(message):
    print('Client connect')
    print('message', message)

async def listen(websocket):
    print('listen works')
    while 1:
        try:
            response = await websocket.recv()
            print('Mes from server', response)
        except:
            continue

async def send(websocket):
    print('send works')
    data={"five": 5, "six": 6}
    message = json.dumps(data)
    await websocket.send(message)
        
async def handler():
    uri = "ws://localhost:9905"
    async with websockets.connect(uri) as websocket:

        send_task = asyncio.ensure_future(send(websocket))
        listen_task = asyncio.ensure_future(listen(websocket))

        done, pending = await asyncio.wait(
            [send_task, listen_task],
            return_when=asyncio.ALL_COMPLETED,)
        for task in pending:
            task.cancel()

def sub_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(handler())
    loop.run_forever()

async def start(executor):
    await asyncio.get_event_loop().run_in_executor(executor, sub_loop)

if __name__ == '__main__':
    executor = ProcessPoolExecutor()
    asyncio.get_event_loop().run_until_complete(start(executor))

