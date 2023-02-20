import asyncio
import websockets
import os
import json
from pyvts import vts_request

class vts:
    def __init__(self, port=8001) -> None:
        self.port = port
        self.websocket = None
        self.authentic_token = None
    
    async def authenticate(self, vts_req=None) -> None:
        # get authenticate code from VTubeStudio
        if vts_req is None:
            request_msg = json.dumps(vts_request.Authentication)
        else:
            request_msg = vts_req.authentication_request()

        async with websockets.connect('ws://127.0.0.1:' + str(self.port)) as self.websocket:
            await self.websocket.send(request_msg)
            response_msg = await self.websocket.recv()
            response_dict = json.loads(response_msg)
        try:  
            self.authentic_token = response_dict["data"]["authenticationToken"]
        except:
            print("authenticate failed")

    async def request(self, request_msg) -> dict:
        # send request with request_msg with "vts_request.py"
        async with websockets.connect('ws://127.0.0.1:' + str(self.port)) as self.websocket:
            await self.websocket.send(json.dumps(request_msg))
            response_msg = await self.websocket.recv()
            response_dict = json.loads(response_msg)
        return response_dict
    




    

