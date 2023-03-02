import asyncio, json
import websockets


class FakeVtubeStudioAPIServer:
    def __init__(self):
        self.server = None
        self.token = "sfijgrnjoghpk394u85"

    async def start(self, port=8001):
        self.server = await websockets.serve(self.handler, "localhost", port)

    async def stop(self):
        self.server.close()
        await self.server.wait_closed()

    async def authen_token(self):
        return self.token

    async def handler(self, websocket, path):
        while True:
            message = await websocket.recv()
            # Handle the message as needed
            dict_msg = json.loads(message)
            send_msg = {"name": "FakeVtubeStuidioServer", "data": {}}
            if dict_msg["messageType"] == "AuthenticationTokenRequest":
                send_msg["data"]["authenticationToken"] = self.token
            elif dict_msg["messageType"] == "AuthenticationRequest":
                if dict_msg["data"]["authenticationToken"] == self.token:
                    send_msg["data"]["authenticated"] = True
                else:
                    send_msg["data"]["authenticated"] = False
                    send_msg["data"]["reason"] = "wrong token"
            await websocket.send(json.dumps(send_msg))
