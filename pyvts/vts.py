""" main class """
import json
import websockets
import aiofiles
from pyvts import vts_request, config, error


class vts:
    """
    ``VtubeStudio API`` Connector

    Args
    ----------
    plugin_info : dict of {"plugin_name", "developer", "icon", "authentication_token_path"}

        Information about your plugin.

    vts_api_info: dict of {"version", "name", "port"}
        Informatiopn about VtubeStudio API.

    **kwarg :
        In case you just want to change serveral of the plugin/api Args,
        input your data here

    Examples
    --------
    Using ``Args``

    >>> info = {"plugin_name": "a","developer": "b",
    ...         "authentication_token_path": "./token.txt"}
    >>> pyvts.vts(plugin_info=info)

    Using ``**kwarg``

    >>> pyvts.vts(plugin_name="a", developer="b")

    """

    def __init__(
        self,
        plugin_info: dict = config.plugin_default,
        vts_api_info: dict = config.vts_api,
        **kwargs
    ) -> None:
        self.port = vts_api_info["port"]
        self.websocket = None
        self.authentic_token = None
        self.__connection_status = 0  # 0: not connected, 1: connected
        self.__authentic_status = (
            0  # 0:no authen & token, 1:has token, 2:authen, -1:wrong token
        )
        self.api_name = vts_api_info["name"]
        self.api_version = vts_api_info["version"]
        self.plugin_name = plugin_info["plugin_name"]
        self.plugin_developer = plugin_info["developer"]
        self.plugin_icon = plugin_info["icon"] if "icon" in plugin_info.keys() else None
        self.token_path = plugin_info["authentication_token_path"]
        self.icon = None
        self.vts_request = vts_request.VTSRequest(
            developer=self.plugin_developer, plugin_name=self.plugin_name, **kwargs
        )
        self.event_list = []
        self.recv_histroy = []
        for key, value in kwargs.items():
            setattr(self, key, value)

    async def connect(self) -> None:
        """Connect to VtubeStudio API server"""
        try:
            self.websocket = await websockets.connect(
                "ws://localhost:" + str(self.port)
            )
            self.__connection_status = 1
        except error.ConnectionError as e:
            print("Error: ", e)
            print("Please ensure VTubeStudio is running and")
            print("the API is running on ws://localhost:", str(self.port))

    async def close(self) -> None:
        """
        Close connection
        """
        await self.websocket.close(code=1000, reason="user closed")
        self.__connection_status = 0

    async def request(self, request_msg: dict) -> dict:
        """
        Send request to VTubeStudio

        Args
        ----------
        request_msg : dict
            Message generated from `VTSRequest`

        Returns
        -------
        response_dict
            Message from VTubeStudio API, data is stored in ``return_dict["data"]``

        Examples
        --------
        >>> recv_msg = await myvts.request(send_msg)
        >>> recv_data = recv_msg["data"]
        """
        await self.websocket.send(json.dumps(request_msg))
        response_msg = await self.websocket.recv()
        response_dict = json.loads(response_msg)
        return response_dict

    async def request_authenticate_token(self) -> None:
        """Get authentication code from VTubeStudio"""
        request_msg = self.vts_request.authentication_token()
        response_dict = await self.request(request_msg)
        try:
            assert "authenticationToken" in response_dict["data"].keys(), response_dict
            self.authentic_token = response_dict["data"]["authenticationToken"]
            if self.__authentic_status == 0 or self.__authentic_status == -1:
                self.__authentic_status = 1
        except AssertionError:
            print("authentication failed")

    async def request_authenticate(self) -> bool:
        """
        Get authenticated from vtubestudio to have more access

        Returns
        --------
            Whether the plugin has been authenticated by VTS
        """
        require_msg = self.vts_request.authentication(self.authentic_token)
        responese_dict = await self.request(require_msg)
        try:
            assert responese_dict["data"]["authenticated"], "Authentication Failed"
            self.__authentic_status = 2
        except AssertionError:
            self.__authentic_status = -1
            print(responese_dict)
        return self.__authentic_status == 2

    async def read_token(self) -> str:
        """
        Read authentic token from the token file wrote before

        Returns
        -------
        Token string
        """
        async with aiofiles.open(self.token_path, mode="r") as f_token:
            await f_token.seek(0)
            self.authentic_token = await f_token.read()
        return self.authentic_token

    async def write_token(self) -> None:
        """Write authentic token into localfile"""
        try:
            assert (
                self.authentic_token is not None
            ), "Has Not Got Authentic Code From VtubeStudio"
            async with aiofiles.open(self.token_path, mode="w") as f_token:
                await f_token.seek(0)
                await f_token.write(self.authentic_token)
        except FileNotFoundError:
            print("write authentic token files failed")

    def get_authentic_status(self) -> int:
        """
        Get authentic status

        Returns
        --------
            Authentic status,
            0 - no authen & token, 1 - has token, 2 - authen, -1 - wrong token
        """
        return self.__authentic_status

    def get_connection_status(self) -> int:
        """
        Get connection status

        Returns
        --------
            Connection status, 0: not connected, 1: connected
        """
        return self.__connection_status

    async def event_subscribe(self, msg: dict) -> dict:
        """
        subscribe event from vts api

        Args
        -----------
        msg : dict
            Event subscription message generated from method of `VTSRequest`

        Returns
        -------
            Message returned from VTube Studio API
        """
        # set up lisening action
        return await self.request(msg)
