""" test vts/vts_request.py """
from pyvts import config

API_NAME = config.vts_api["name"]
API_VERSION = config.vts_api["version"]


class VTSRequest:
    """VtubeStudio API Request Generator"""

    def __init__(
        self,
        developer: str = config.plugin_default["developer"],
        plugin_name: str = config.plugin_default["plugin_name"],
        **kwargs
    ):
        """
        VtubeStudio API Request Generator

        Parameters
        ----------
        developer : str
            developer the your plugin
        plugin_name : dict
            plugin name
        **kwargs
            other parameters like ``api_version``, ``api_version``,
            not needed in most cases

        Returns:
            pyvts.VTSRequest
                request generator
        """
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
        """
        Standard Request

        Parameters
        ----------
        message_type : str
            Message type of request
        data : dict
            optional, relavent data sending to ``VTubeStudio API``
        request_id : str
            string to mark the request, not important

        Returns
        -------
        dict of {"apiName: str, "apiVersion": str, "requestID": str, "messageType: str, "data": dict}
            the organized message sending to ``Vtubestudio API``
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
        ------
        dict
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
        if self.icon is not None:
            data["pluginIcon"] = self.icon
        return self.BaseRequest(msg_type, data)

    def authentication(self, token) -> dict:
        """
        use auth_token to get more access

        Parameters
        ----------
        token : str
            authenication token

        Returns
        -------
        dict
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

        Parameters
        -----------
            x, y : float
                location of model,
                if relative == False:  [0, 0] means the middle of the model in the middle of the screen
                else if relative == True: [0, 0] means location of model center point
            rot : float
                rotation angle, range [-360, 360]
            size : float
                zoom ratio, default: 1
            relative : bool
                whether the values are considered to be relative to the current model position
            move_time : float
                time of the move motion

        Returns
        -------
        dict of {data: dict}
            the organized message sending to ``Vtubestudio API``
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

    def requestTriggerHotKey(self, hotkeyID):
        """TODO"""
        pass

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

        Parameters
        -----------
        parameter : str
            name of parameter
        min : float
            minimum bound for the parameter
        max : float
            maximum bound for the parameter
        default_value : float
            default value
        info : str
            description of this parameter

        Returns
        -------
        dict
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

        Parameters
        ----------
        parameter : str
            name of the parameter
        value : float
            value of the data from -1000000 to 1000000
        weight : float
            you can mix the your value with vts face tracking parameter, from 0 to 1,
            defualt(no mixture): 1
        face_found : bool
            if true, you will tell VTubeStudio to consider the user face as found,
            s.t. you can control when the "tracking lost"

        Returns
        -------
        dict
            the organized message sending to ``Vtubestudio API``
        """
        data = {
            "faceFound": face_found,
            "mode": mode,
            "parameterValues": [{"id": parameter, "weight": weight, "value": value}],
        }
        return self.BaseRequest("InjectParameterDataRequest", data=data)

    def requestDeleteCustomParameter(self, parameter):
        data = {"parameterName": parameter}
        return self.BaseRequest("ParameterDeletionRequest", data=data)

    def eventSubscription(
        self, event_name: str, on: bool = True, cfg: dict = {"0": 0}
    ) -> dict:
        """
        subscribe event from vtubestudio api (base function, seldom directly used)

        Parameters
        ----------
        event_name : string
            event name you want to substribe
        on : bool
            turn on or turn off
        cfg : dict
            optional, config message
        """
        msg_type = "EventSubscriptionRequest"
        data = {"eventName": event_name, "subscribe": on, "config": cfg}
        return self.BaseRequest(msg_type, data)

    def eventSubscriptionTest(self, test_msg="text the event will return"):
        """
        test event
        recv msg type: "TestEvent"
        """
        cfg = {"testMessageForEvent": test_msg}
        return self.eventSubscription(event_name="TestEvent", cfg=cfg)

    def eventSubscriptionModelLoaded(self, modelID: list = []) -> dict:
        """
        subscribe message of model loaded/unloaded
        recv msg type: "ModelLoadedEvent"
        recv msg data: {
            "modelLoaded": true/false,
            "modelName": "My VTS Model Name",
            "modelID": "165131471d8a4e42aae01a9738f255ef"
        }
        """
        event_name = "ModelLoadedEvent"
        cfg = {"modelID": modelID}
        return self.eventSubscription(event_name=event_name, cfg=cfg)

    def eventSubscriptionTrackingStatusChanged(self) -> dict:
        """
        subscribe message of tracking lost/found
        recv msg type: "TrackingStatusChangedEvent"
        recv msg data: {
            "faceFound": true/false,
            "leftHandFound": true/false,
            "rightHandFound": true/false
        }
        """
        return self.eventSubscription(event_name="TrackingStatusChangedEvent")

    def eventSubscribtionModelMoved(self) -> dict:
        """
        subscribe message of model moved/resized/rotated
        recv msg type: "ModelMovedEvent"
        recv msg data: {
            "modelID": "UniqueIDToIdentifyThisModelBy",
            "modelName": "My Cool Model",
            "modelPosition": {
                "positionX": -0.20491,
                "positionY": 0.1,
                "size": -74.49664306640625,
                "rotation": 341.3
        }
        """
        return self.eventSubscription(event_name="ModelMovedEvent")

    def eventSubsribtionModelOutline(self, draw=False) -> dict:
        """
        subscribe message of model outline
        draw: if is True, then the outline will show on VTubeStudio App
        recv msg type: "ModelOutlineEvent"
        recv msg data: {
            "modelName": "My VTS Model Name",
            "modelID": "165131471d8a4e42aae01a9738f255ef",
            "convexHull": [
                {"x": 0.200516939163208, "y": 0.8014626502990723}, {...}
            ],
            "convexHullCenter": {"x": 0.3527252674102783, "y": -0.24669097363948822},
            "windowSize": {"x": 1920, "y": 1080}
        }
        """
        event_name = "ModelOutlineEvent"
        cfg = {"draw": draw}
        return self.eventSubscription(event_name, cfg)
