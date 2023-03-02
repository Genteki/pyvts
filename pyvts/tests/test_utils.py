# pylint: disable=E1101
""" utils for tests """
import json
import websockets


class FakeVtubeStudioAPIServer:
    """fake server for test"""

    def __init__(self):
        self.server = None
        self.token = "sfijgrnjoghpk394u85"

    async def start(self, port=8001):
        """start server"""
        self.server = await websockets.serve(self.handler, "localhost", port)

    async def stop(self):
        """stop server"""
        self.server.close()
        await self.server.wait_closed()

    async def authen_token(self):
        """get the authentic token"""
        return self.token

    async def handler(self, websocket):
        """function of handling massage from vts client"""
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
