""" Generate vts request """
from pyvts import config

API_NAME = config.vts_api["name"]
API_VERSION = config.vts_api["version"]


class VTSRequest:
    """
    VtubeStudio API Request Generator

    Args
    ----------
    developer : str
        developer the your plugin
    plugin_name : dict
        plugin name
    plugin_icon: str
        plugin icon
    **kwargs : optional
        other parameters like ``api_version``,
    """

    def __init__(
        self,
        developer: str = config.plugin_default["developer"],
        plugin_name: str = config.plugin_default["plugin_name"],
        plugin_icon: str = config.plugin_default["plugin_icon"],
        **kwargs
    ):
        """ """
        self.developer = developer
        self.plugin_name = plugin_name
        self.plugin_icon = plugin_icon
        self.api_version = API_VERSION
        self.api_name = API_NAME
        for key, value in kwargs.items():
            setattr(self, key, value)

    def BaseRequest(
        self, message_type: str, data: dict = None, request_id: str = "SomeID"
    ) -> dict:
        """
        Standard Request

        Args
        ----------
        message_type : str
            Message type of request
        data : dict, optional
            Relavent data sending to ``VTubeStudio API``
        request_id : str, optional
            String to mark the request, not important

        Returns
        -------
            Organized message sending to ``Vtubestudio API``
        """

        msg = {
            "apiName": self.api_name,
            "apiVersion": self.api_version,
            "requestID": request_id,
            "messageType": message_type,
            "data": data,
        }
        return msg

    def authentication_token(self) -> dict:
        """
        generate request msg to requirer authentication_token

        Returns
        -------
            the organized message sending to ``Vtubestudio API``

        Examples
        ---------
        >>> message = myvts.vts_request.authentication_token()
        >>> return_msg = await myvts.request(message)
        """
        # Plugin icons should be 128x128 pixel Base64-encoded PNGs.
        msg_type = "AuthenticationTokenRequest"
        data = {
            "pluginName": self.plugin_name,
            "pluginDeveloper": self.developer,
        }
        if self.plugin_icon is not None:
            data["pluginIcon"] = self.plugin_icon
        return self.BaseRequest(msg_type, data)

    def authentication(self, token) -> dict:
        """
        use auth_token to get more access

        Args
        ----------
        token : str
            authenication token

        Returns
        -------
            the organized message sending to ``Vtubestudio API``
        """
        msg_type = "AuthenticationRequest"
        data = {
            "pluginName": self.plugin_name,
            "pluginDeveloper": self.developer,
            "authenticationToken": token,
        }
        return self.BaseRequest(msg_type, data)

    def requestMoveModel(
        self, x, y, rot=0, size=1, relative=True, move_time=0.2
    ) -> dict:
        """
        request to move the model

        Args
        -----------
            x: float
                Location of model, x
            y: float
                Location of model, y
            rot : float, optional
                Rotating angle, range [-360, 360]
            size : float, optional
                Zoom ratio, default: 1
            relative : bool, optional
                Whether the values are considered to be relative to the current model position
            move_time : float, optional
                Time of the move motion

        Returns
        -------
            Organized message sending to ``Vtubestudio API``
        """
        msg_type = "MoveModelRequest"
        data = {
            "timeInSeconds": move_time,
            "valuesAreRelativeToModel": relative,
            "positionX": x,
            "positionY": y,
            "rotation": rot,
            "size": size,
        }
        return self.BaseRequest(msg_type, data)

    def requestHotKeyList(self) -> dict:
        return self.BaseRequest("HotkeysInCurrentModelRequest")

    def requestTriggerHotKey(self, hotkeyID, itemInstanceID=None) -> dict:
        """
        Trigger hotkey. # TODO, handle `itemInstanceID`

        Args
        -----
            hotkeyID: str
                Hotkey name or unique id of hotkey to execute,
                can be obtained via `VTSRequest.requestHotKeyList()`
            itemInstanceID: str, optional
                Model ID of the hotkey. If left blank,
                it will trigger a hotkey for the currently loaded VTubeStudio model.

        Returns
        -------
            Organized message sending to ``Vtubestudio API``
        """
        msg_type = "HotkeyTriggerRequest"
        data = {"hotkeyID": hotkeyID}
        return self.BaseRequest(msg_type, data)

    def requestTrackingParameterList(self) -> dict:
        return self.BaseRequest("InputParameterListRequest")

    def requestParameterValue(self, parameter: str) -> dict:
        data = {"name": parameter}
        return self.BaseRequest("ParameterValueRequest", data=data)

    def requestCustomParameter(
        self, parameter: str, min=0, max=1, default_value=0, info=""
    ) -> dict:
        """
        Add your own new tracking parameters and use them in your VTube Studio models

        Args
        -----------
        parameter : str
            Name of parameter
        min : float, optional
            Minimum bound for the parameter
        max : float, optional
            Maximum bound for the parameter
        default_value : float, optional
            Default value of this parameter
        info : str, optional
            Description of this parameter

        Returns
        -------
            the organized message sending to ``Vtubestudio API``
        """
        data = {
            "parameterName": parameter,
            "explanation": info,
            "min": min,
            "max": max,
            "defaultValue": default_value,
        }
        return self.BaseRequest("ParameterCreationRequest", data=data)

    def requestSetParameterValue(
        self,
        parameter: str,
        value: float,
        weight: float = 1,
        face_found=False,
        mode="set",
    ) -> dict:
        """
        Set value for any default or custom parameter.

        Args
        ----------
        parameter : str
            Name of the parameter
        value : float
            Value of the data, [-1000000, 1000000]
        weight : float, optional
            You can mix the your value with vts face tracking parameter, from 0 to 1,
        face_found : bool, optional
            if true, you will tell VTubeStudio to consider the user face as found,
            s.t. you can control when the "tracking lost"

        Returns
        -------
            organized message sending to ``Vtubestudio API``
        """
        data = {
            "faceFound": face_found,
            "mode": mode,
            "parameterValues": [{"id": parameter, "weight": weight, "value": value}],
        }
        return self.BaseRequest("InjectParameterDataRequest", data=data)

    def requestSetMultiParameterValue(
        self,
        parameters: list[str],
        values: list[float],
        weight: float = 1,
        face_found=False,
        mode="set",
    ) -> dict:
        """
        Set values for any default or custom parameters.

        Args
        ----------
        parameter : list[str]
            Names of the parameters
        value : list[float]
            Values of the data, [-1000000, 1000000]
        weight : float, optional
            You can mix the your value with vts face tracking parameter, from 0 to 1,
        face_found : bool, optional
            if true, you will tell VTubeStudio to consider the user face as found,
            s.t. you can control when the "tracking lost"

        Returns
        -------
            organized message sending to ``Vtubestudio API``
        """
        data = {
            "faceFound": face_found,
            "mode": mode,
            "parameterValues": [
                {"id": parameters[i], "weight": weight, "value": values[i]}
                for i, _ in enumerate(parameters)
            ],
        }
        return self.BaseRequest("InjectParameterDataRequest", data=data)

    def requestDeleteCustomParameter(self, parameter) -> dict:
        """
        Delete custom parameter

        Args
        ----
        parameter: str
            Name of the parameter to delete

        Returns
        -------
            organized message sending to ``Vtubestudio API``
        """
        data = {"parameterName": parameter}
        return self.BaseRequest("ParameterDeletionRequest", data=data)

    def ColorTintRequest(
        self,
        red: int = 0,
        green: int = 0,
        blue: int = 0,
        alpha: int = 255,
        jeb: bool = False,
        mix_with_scene_lighting_color: float = 1,
        tint_all: bool = False,
        art_mesh_number: list = [],
        name_exact: list = [],
        name_contains: list = [],
        tag_exact: list = [],
        tag_contains: list = [],
    ) -> dict:
        """
        Alter the color of an Artmesh on the current model

        Args
        -----------
        red : int, optional
            red value of tint (0-255)
        green : int, optional
            green value of tint (0-255)
        blue : int, optional
            blue value of tint (0-255)
        alpha : int, optional
            alpha value of tint (0-255)
        jeb : bool, optional
            boolean option to activate "jeb mode"(rainbow cycle) on art meshes
        mix_with_scene_lighting_color: float, optional
            float between 0 and 1, determines how much tint is mixed with scene lighting
        tint_all: bool, optional
            boolean option to tint all
        art_mesh_number: list, optional
            list of ints corresponding to art mesh numbers to color
        name_exact: list, optional
            list of strings of exact names of meshes to color
        name_contains: list, optional
            list of strings of partial names of meshes to color
        tag_exact: list, optional
            list of strings of exact tags of meshes to color
        tag_contains: list, optional
            list of strings of partial names of tags of meshes to color


        Returns
        -------
            the organized message sending to ``Vtubestudio API``
        """
        data = {
            "colorTint": {
                "colorR": red,
                "colorG": green,
                "colorB": blue,
                "colorA": alpha,
                "mixWithSceneLightingColor": mix_with_scene_lighting_color,
                "jeb_": jeb,
            },
            "artMeshMatcher": {
                "tintAll": tint_all,
                "artMeshNumber": art_mesh_number,
                "nameExact": name_exact,
                "nameContains": name_contains,
                "tagExact": tag_exact,
                "tagContains": tag_contains,
            },
        }
        return self.BaseRequest("ColorTintRequest", data=data)

    def eventSubscription(
        self, event_name: str, on: bool = True, cfg: dict = {"0": 0}
    ) -> dict:
        """
        subscribe event from vtubestudio api (base function, seldom directly used)

        Args
        ----------
        event_name : string
            event name you want to substribe
        on : bool, optional
            turn on or turn off
        cfg : dict, optional
            config message

        Returns
        -------
            organized message sending to ``Vtubestudio API``
        """
        msg_type = "EventSubscriptionRequest"
        data = {"eventName": event_name, "subscribe": on, "config": cfg}
        return self.BaseRequest(msg_type, data)

    def eventSubscriptionTest(self, test_msg="text the event will return") -> dict:
        """
        Subscribe test event

        Args
        -----
        test_msg: str, optional
            Text of test message.

        Returns
        --------
            Organized subscription request message.
        """
        cfg = {"testMessageForEvent": test_msg}
        return self.eventSubscription(event_name="TestEvent", cfg=cfg)

    def eventSubscriptionModelLoaded(self, modelID: list = []) -> dict:
        """
        Subscribe message of model loaded/unloaded
        Args
        ----
        modelID : list of int
            ID of model for monitor

        Returns
        --------
            Organized subscription request message.
        """
        event_name = "ModelLoadedEvent"
        cfg = {"modelID": modelID}
        return self.eventSubscription(event_name=event_name, cfg=cfg)

    def eventSubscriptionTrackingStatusChanged(self) -> dict:
        """
        subscribe message of tracking lost/found

        Returns
        --------
            Organized subscription request message.
        """
        return self.eventSubscription(event_name="TrackingStatusChangedEvent")

    def eventSubscribtionModelMoved(self) -> dict:
        """
        Subscribe message of model moved/resized/rotated

        Returns
        -------
            Organized subscription request message.
        """
        return self.eventSubscription(event_name="ModelMovedEvent")

    def eventSubsribtionModelOutline(self, draw=False) -> dict:
        """
        Subscribe message of model outline

        Returns
        --------
            Organized subscription request message.
        """
        event_name = "ModelOutlineEvent"
        cfg = {"draw": draw}
        return self.eventSubscription(event_name, cfg)
