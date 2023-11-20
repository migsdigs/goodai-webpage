# IMPORTS
import asyncio
from aiohttp import web, WSMsgType
import random
import json
import ssl

# Create Websocket request handler 
async def websocket_handler(request):
    """
    Function to handle websocket requests from a client.
    Recieves request as JSON containing a frequency value.
    Send respsonse to request as a random generated value at specified frequency.
    """

    ws = web.WebSocketResponse()    # Create instance of WebSocket
    await ws.prepare(request)       # Wait for request

    frequency = 10                  # Initial frequency value

    async def send_data():  
        while True:
            await asyncio.sleep(1/frequency)                    # do not send anything for 1/frequency seconds
            await ws.send_json({'size':random.random()})        # send JSON with 'size' parameter, a random float generated between 0-1
            # await ws.send_str(str(random.randint(1,1000)))
            
    
    # can execute the send_data coroutine in background without waiting for it to finish
    asyncio.ensure_future(send_data())

    # To handle request messages from client:
    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            data = json.loads(msg.data)             # Load JSON data from request
            data_frequency = data['frequency']      # Extract frequency value
            # data = msg.data

            try:                                    # Update frequency value if it is not equal to 0 and greater than 0.
                if float(data_frequency) != 0 and float(data_frequency) >= 0:
                    frequency = float(data_frequency)
                    print(f"Frequency: {int(frequency)} Hz")
            except:                                 # If frequency value is invalid, frequency remains the same.
                print(data)
                frequency = frequency
                print("Frequency given was not a number.")
                
    
    return ws

# Create an instance of the application
app = web.Application()

# Add route
app.add_routes([web.get('/ws', websocket_handler)])


if __name__ == '__main__':
    web.run_app(app)



# # New stuff added for SSL
# async def create_server():
#     app = web.Application()
#     # app.router.add_get('/ws', websocket_handler)
#     app.add_routes([web.get('/ws', websocket_handler)])

#     ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
#     ssl_context.load_cert_chain('/home/miguel/goodai-webpage/certificate.crt', '/home/miguel/goodai-webpage/private.key')

#     runner = web.AppRunner(app)
#     await runner.setup()
#     site = web.TCPSite(runner, 'localhost', 8080, ssl_context=ssl_context)
#     await site.start()

#     print("Server started")
#     return runner, site

# async def close_server(runner, site):
#     await runner.cleanup()
#     await site.stop()

# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     server, site = loop.run_until_complete(create_server())

#     try:
#         loop.run_forever()
#     except KeyboardInterrupt:
#         loop.run_until_complete(close_server(server, site))
            


