""" test vts/vts_request.py """
from pyvts import config

API_NAME = config.vts_api["name"]
API_VERSION = config.vts_api["version"]


class VTSRequest:
    """VtubeStudio API Request Generator"""

    def __init__(
        self,
        developer: dict = config.plugin_default["developer"],
        plugin_name: dict = config.plugin_default["plugin_name"],
        **kwargs
    ) -> None:
        self.developer = developer
        self.plugin_name = plugin_name
        self.api_version = API_VERSION
        self.api_name = API_NAME
        self.icon = None
        for key, value in kwargs.items():
            setattr(self, key, value)

    def BaseRequest(
        self, message_type: str, data: dict = None, request_id: str = "SomeID"
    ) -> dict:
        """Standard Request"""
        msg = {
            "apiName": self.api_name,
            "apiVersion": self.api_version,
            "requestID": request_id,
            "messageType": message_type,
            "data": data,
        }
        return msg

    def authentication_token(self) -> dict:
        """generate request msg to requirer authentication_token"""
        # Plugin icons should be 128x128 pixel Base64-encoded PNGs.
        msg_type = "AuthenticationTokenRequest"
        data = {
            "pluginName": self.plugin_name,
            "pluginDeveloper": self.developer,
        }
        if self.icon is not None:
            data["pluginIcon"] = self.icon
        return self.BaseRequest(msg_type, data)

    def authentication(self, token) -> dict:
        """
        use auth_token to get more access
        token: authenication token (str)
        """
        msg_type = "AuthenticationRequest"
        data = {
            "pluginName": self.plugin_name,
            "pluginDeveloper": self.developer,
            "authenticationToken": token,
        }
        return self.BaseRequest(msg_type, data)
