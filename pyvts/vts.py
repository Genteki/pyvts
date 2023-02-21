import asyncio
import websockets
import os
import json
from pyvts import vts_request

API_VERSION = "1.0"
API_NAME = "VTubeStudioPublicAPI"
PLUGIN_NAME = "your plugin name"
REQUEST_ID = "test"
DEVELOPERER = "genteki"

class vts:
    def __init__(self, port=8001, **kwd) -> None:
        self.port = port
        self.websocket = None
        self.authentic_token = None
        self.connection_status = 0 
        self.plugin_info = {
                "pluginName": PLUGIN_NAME,
                "pluginDeveloper": DEVELOPERER
        }
    
    async def connect(self):
        try:
            self.websocket = await websockets.connect('ws://localhost:' + str(self.port))
        except:
            print("connection failed")
            print("please ensure VTubeStudio is running and \nthe API is running on ws://localhost:"+str(self.port))
    
    async def close(self) -> None:
        await self.websocket.close(code=1000, reason="user closed")
    
    async def send(self, request_msg:dict) -> dict:
        await self.websocket.send(json.dumps(request_msg))
        response_msg = await self.websocket.recv()
        response_dict = json.loads(response_msg)
        return response_dict
        
    
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


    # async def request(self, request_msg:dict) -> dict:
    #     # send request with request_msg with "vts_request.py"
    #     await self.websocket.send(json.dumps(request_msg))
    #     response_msg = await self.websocket.recv()
    #     response_dict = json.loads(response_msg)
    #     return response_dict
    




    

