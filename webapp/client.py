import asyncio
import websockets


# async def hello():
#     async with websockets.connect('ws://0.0.0.0:8080/ws') as websocket:
#         await websocket.send("3")
#         response = await websocket.recv()
#         print(f"Received: {response}")

# asyncio.get_event_loop().run_until_complete(hello())

async def mock_client():
    async with websockets.connect('ws://0.0.0.0:8080/ws') as websocket:
        try:
            while True:
                # recieve message from server
                await websocket.send("10")
                message = await websocket.recv()
                print(f"Recieved message: {message}")


        except websockets.exceptions.ConnectionClosed:
            print("Websocket connection closed")

asyncio.get_event_loop().run_until_complete(mock_client())