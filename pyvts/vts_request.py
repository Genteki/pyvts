API_VERSION = "1.0"
API_NAME = "VTubeStudioPublicAPI"
PLUGIN_NAME = "your plugin name"
REQUEST_ID = "test"
DEVELOPERER = "genteki"

class vts_request:
    def __init__(self, developer=DEVELOPERER, plugin_name=PLUGIN_NAME, **kwd) -> None:
        self.developer = developer
        self.plugin_name = plugin_name
        self.api_version = API_VERSION
        self.api_name = API_NAME
        self.request_id = REQUEST_ID
        self.icon = None

    def simple_request(self, message_type) -> dict:
        msg = {
            "apiName": self.api_name,
            "apiVersion": self.api_version,
            "requestID": self.request_id,
            "messageType": message_type
        }
        return msg
    
    def authentication_request(self) -> dict:
        # Plugin icons should be 128x128 pixel Base64-encoded PNGs.
        msg = {
            "apiName": self.api_name,
            "apiVersion": self.api_version,
            "requestID": self.request_id,
            "messageType": "AuthenticationTokenRequest",
            "data": {
                "pluginName": self.plugin_name,
                "pluginDeveloper": self.developer,
            }
        }
        if self.icon is not None:
            msg["data"]["pluginIcon"] = self.icon
        return msg

APIState = {
    "apiName": API_NAME,
    "apiVersion":API_VERSION,
    "requestID": REQUEST_ID,
    "messageType": "APIStateRequest"
}

AuthenticationRequest = {
	"apiName": API_NAME,
	"apiVersion": API_VERSION,
	"requestID": REQUEST_ID,
	"messageType": "AuthenticationTokenRequest",
	"data": {
		"pluginName": PLUGIN_NAME,
		"pluginDeveloper": DEVELOPERER,
		# "pluginIcon": "iVBORw0.........KGgoA=" # ADDITIONALLY
	}
}

VTS_folder_info_request = {
    "apiName": API_NAME,
    "apiVersion":API_VERSION,
    "requestID": REQUEST_ID,
    "messageType": "VTSFolderInfoRequest"
}