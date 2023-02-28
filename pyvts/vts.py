import os, json, asyncio
import websockets
import aiofiles
from pyvts import vts_request, config

API_VERSION = config.vts_api["version"]
API_NAME = config.vts_api["name"]
PLUGIN_NAME = "your plugin name"
REQUEST_ID = "test"
DEVELOPERER = "genteki"

class vts:
    def __init__(self, plugin_info: dict = config.plugin_default,
                 vts_api_info: dict = config.vts_api, **kwargs) -> None:
        '''
        plugin_info: {
            "plugin_name": your plugin name (str),
            "developer": your name (str),
            "icon": (optional) your icon if exist (img),
            "authentication_token_path": str
        }
        vts_api_info: {
            "version": str,
            "name": str,
            "port": int
        }
        '''
        self.port = vts_api_info["port"]
        self.websocket = None
        self.authentic_token = None
        self._connection_status = 0  # 0: not connected, 1: connected
        self._authentic_status = 0 # 0: no authen & no token, 1: no authen & yes token, 2: authen, -1: wrong token
        self.plugin_name = plugin_info["plugin_name"]
        self.plugin_developer = plugin_info["developer"]
        self.plugin_icon = plugin_info["icon"] if "icon" in plugin_info.keys() else None
        self.token_path = plugin_info["authentication_token_path"]
        self.vts_request = vts_request.VTSRequest(developer=self.plugin_developer, 
                                                  plugin_name=self.plugin_name, **kwargs)
        for key, value in kwargs.items():
            setattr(self, key ,value)
    
    async def connect(self):
        try:
            self.websocket = await websockets.connect('ws://localhost:' + str(self.port))
        except:
            print("connection failed")
            print("Please ensure VTubeStudio is running and")
            print("the API is running on ws://localhost:", str(self.port))
    
    async def close(self) -> None:
        await self.websocket.close(code=1000, reason="user closed")
    
    async def send(self, request_msg: dict) -> dict:
        await self.websocket.send(json.dumps(request_msg))
        response_msg = await self.websocket.recv()
        response_dict = json.loads(response_msg)
        return response_dict
        
    async def authenticateTokenRequest(self) -> None:
        ''' get authentication code from VTubeStudio '''
        request_msg = self.vts_request.authenticationToken()
        response_dict = await self.request(request_msg)
        try:
            self.authentic_token = response_dict["data"]["authenticationToken"]
            if self._authentic_status == 0 or self._authentic_status == -1:
                self._authentic_status = 1
        except:
            print("authentication failed")
    
    async def authenticate(self) -> bool:
        ''' get authenticated from vtubestudio to have more access '''
        require_msg = self.vts_request.authentication(self.authentic_token)
        responese_dict = await self.request(require_msg)
        try:
            assert responese_dict["data"]["authenticated"], "Authentication Failed"
            self._authentic_status = 2
        except:
            self._authentic_status = -1
            print(responese_dict["data"])
        return self._authentic_status == 2

    async def read_token(self) -> str:
        ''' read authentic token from the token file wrote before '''
        async with aiofiles.open(self.token_path, mode='r') as f_token:
            await f_token.seek(0)
            self.authentic_token = await f_token.read()
        return self.authentic_token
    
    async def write_token(self) -> None:
        ''' write authentic token '''
        try:
            assert self.authentic_token is not None, "Has Not Got Authentic Code From VtubeStudio"
            async with aiofiles.open(self.token_path, mode='w') as f_token:
                await f_token.seek(0)
                await f_token.write(self.authentic_token)
        except:
            print("write authentic token files failed")