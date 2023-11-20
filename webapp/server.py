import asyncio
import random
import json

from aiohttp import web, WSMsgType
from aiohttp.web import Request, WebSocketResponse


async def websocket_handler(request: Request) -> WebSocketResponse:
    """
    Function to handle websocket requests from a client.
    
    Attributes:
        request (aiohttp.web.Request): used for receiving request's information
        by websocket handler.
    
    Returns:
        Websocket response containing JSON response.
    """

    frequency = 10

    ws = WebSocketResponse()    # Create instance of WebSocket
    await ws.prepare(request)       # Wait for request
    

    async def send_data():
        while True:
            # do not send anything for 1/frequency seconds
            await asyncio.sleep(1/frequency)

            # send JSON with 'size' parameter, a random float generated between 0-1
            await ws.send_json({'size': random.random()})



    # can execute the send_data coroutine in background without waiting for it to finish
    asyncio.ensure_future(send_data())

    # To handle request messages from client:
    async for msg in ws:
        if msg.type == WSMsgType.TEXT:

            # frequency = update_frequency(msg=msg, frequency=frequency)
            data = json.loads(msg.data)             # Load JSON data from request
            data_frequency = data['frequency']      # Extract frequency value
            # data = msg.data

            # Update frequency value if it is not equal to 0 and greater than 0.
            try:
                if float(data_frequency) != 0 and float(data_frequency) >= 0:
                    frequency = float(data_frequency)
                    print(f"Frequency: {int(frequency)} Hz")
            except TypeError:
                print(data)
                print("Frequency given was not a number.")

    return ws

# Create an instance of the application
app = web.Application()

# Add route
app.add_routes([web.get('/ws', websocket_handler)])


if __name__ == '__main__':
    web.run_app(app)



# # Function declarations
# def update_frequency(msg: WSMsgType.TEXT, frequency: int) -> int:
#     """
#     Function to update the frequency at which server sends messages to client.

#     Attributes:
#         msg (WSMsgType.TEXT): Websocket message of text type 
#         containing the new frequency value.

#         frequency (int): current frequency value

#     Returns:
#         frequency int with new frequency value
#     """


#     data = json.loads(msg.data)             # Load JSON data from request
#     data_frequency = data['frequency']      # Extract frequency value

#     # Update frequency value if it is not equal to 0 and greater than 0.
#     try:
#         if float(data_frequency) != 0 and float(data_frequency) >= 0:
#             print(f"Frequency: {int(data_frequency)} Hz")
#             return data_frequency
#     except TypeError:
#         print(data)
#         print("Frequency given was not a number.")
#         return frequency
