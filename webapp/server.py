# IMPORTS
import asyncio
from aiohttp import web, WSMsgType
import random
import json

# Create Websocket request handler
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    frequency = 10

    async def send_data():
        while True:
            await asyncio.sleep(1/frequency)
            # await ws.send_json({'size':random.randint(1,1000)})
            await ws.send_str(str(random.randint(1,1000)))
    
    # can execute coroutine in background without waiting for it to finish
    asyncio.ensure_future(send_data())

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            # data = json.loads(msg.data)
            data = msg.data
            frequency = float(data)
            print(frequency)
    
    return ws
            

app = web.Application()
app.add_routes([web.get('/ws', websocket_handler)])


if __name__ == '__main__':
    web.run_app(app)

# # Create Websocket request handler
# async def websocket_handler(request):

#     # create websocket response object
#     ws = web.WebSocketResponse()
#     await ws.prepare(request)   # asynchronous: perform other tasks while waiting for request


#     async for msg in ws:
#         while True:
#             try:
#                 # Generate random value
#                 random_value = random.randint(1,1000)   # Probs need to adjust this later
                
#                 print(f"message from client: {msg.data}")
#                 # send random value to frontend as string
#                 await ws.send_str(str(random_value))
                
#                 # delay according to frequency in textbox on frontend
#                 try:
#                     await asyncio.sleep(1/int(msg.data))
#                 except:
#                    await asyncio.sleep(1)
            

#             except asyncio.CancelledError:
#                 break
    
        
#     return ws


# app = web.Application()
# app.add_routes([web.get('/ws', websocket_handler)])


# if __name__ == '__main__':
#     web.run_app(app)








# from aiohttp import web, WSMsgType
# import random

# async def websocket_handler(request):
#     ws = web.WebSocketResponse()
#     await ws.prepare(request)

#     async for msg in ws:
#         # Generate random value
#         random_value = random.randint(1,1000)   # Probs need to adjust this later
#         if msg.type == WSMsgType.TEXT:
#             await ws.send_str(f"you have send {msg.data} and we return {random_value}")
#         elif msg.type == WSMsgType.BINARY:
#             await ws.send_bytes(msg.data)
#         elif msg.type == WSMsgType.ERROR:
#             break

#     return ws

# app = web.Application()
# app.router.add_get('/ws', websocket_handler)

# if __name__ == '__main__':
#     web.run_app(app)

