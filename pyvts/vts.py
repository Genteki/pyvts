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
        self.isAuth = False
    
    async def authenticateTokenRequest(self, vts_req:vts_request.VTSRequest=None) -> None:
        # get authentication code from VTubeStudio
        if vts_req is None:
            request_msg = json.dumps(vts_request.Authentication)
        else:
            request_msg = vts_req.authenticationToken()

        response_dict = await self.request(request_msg)
        try:  
            self.authentic_token = response_dict["data"]["authenticationToken"]
        except:
            print("authentication failed")
    
    async def authenticate(self, vts_req:vts_request.VTSRequest) -> bool:
        # get authenticated from vts
        require_msg = vts_req.authentication(self.authentic_token)
        responese_dict = await self.request(require_msg)
        isAuth = False
        try:
            isAuth = responese_dict["data"]["authenticated"]
        except:
            print("authentic failed")
            print(responese_dict["data"])
        self.isAuth = isAuth
        return isAuth


    async def request(self, request_msg:dict) -> dict:
        # send request with request_msg with "vts_request.py"
        async with websockets.connect('ws://127.0.0.1:' + str(self.port)) as self.websocket:
            await self.websocket.send(json.dumps(request_msg))
            response_msg = await self.websocket.recv()
            response_dict = json.loads(response_msg)
        return response_dict
    




    

