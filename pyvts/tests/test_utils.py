""" utils for tests """
import json
import websockets


class FakeVtubeStudioAPIServer:
    """fake server for test"""

    def __init__(self):
        self.server = None
        self.token = "sfijgrnjoghpk394u85"
        self.custom_param = {}

    async def start(self, port=8001):
        """start server"""
        self.server = await websockets.serve(self.handler, "127.0.0.1", port)

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
            send_msg = {"apiName": "FakeVtubeStuidioServer", "data": {}}

            # About authentication
            if dict_msg["messageType"] == "AuthenticationTokenRequest":
                send_msg["data"]["authenticationToken"] = self.token
            elif dict_msg["messageType"] == "AuthenticationRequest":
                if dict_msg["data"]["authenticationToken"] == self.token:
                    send_msg["data"]["authenticated"] = True
                else:
                    send_msg["data"]["authenticated"] = False
                    send_msg["data"]["reason"] = "wrong token"

            # About Custom Parameters
            elif dict_msg["messageType"] == "ParameterCreationRequest":
                self.custom_param[dict_msg["data"]["parameterName"]] = {
                    "min": dict_msg["data"]["min"],
                    "max": dict_msg["data"]["max"],
                    "defaultValue": dict_msg["data"]["defaultValue"],
                    "value": dict_msg["data"]["defaultValue"],
                }
                send_msg["data"] = {"parameterName": dict_msg["data"]["parameterName"]}
            elif dict_msg["messageType"] == "ParameterValueRequest":
                pname = dict_msg["data"]["name"]
                if pname in self.custom_param:
                    send_msg["data"] = {
                        "name": pname,
                        "value": self.custom_param[pname]["value"],
                        "max": self.custom_param[pname]["max"],
                        "min": self.custom_param[pname]["min"],
                        "defaultValue": self.custom_param[pname]["defaultValue"],
                    }
                else:
                    send_msg["data"] = {
                        "errorID": 500,
                        "message": "Given parameter start parameter does not exist.",
                    }
            elif dict_msg["messageType"] == "ParameterDeletionRequest":
                pname = dict_msg["data"]["parameterName"]
                if pname in self.custom_param:
                    del self.custom_param[pname]
                    send_msg["data"] = {"parameter": pname, "message": "Deleted"}
            elif dict_msg["messageType"] == "InjectParameterDataRequest":
                pname = dict_msg["data"]["parameterValues"][0]["id"]
                if pname in self.custom_param:
                    self.custom_param[pname]["value"] = float(
                        dict_msg["data"]["parameterValues"][0]["value"]
                    ) * float(dict_msg["data"]["parameterValues"][0]["weight"]) + float(
                        self.custom_param[pname]["value"]
                    ) * float(
                        (1 - dict_msg["data"]["parameterValues"][0]["weight"])
                    )
                    send_msg["data"] = {"parameter": pname, "message": "set"}
                else:
                    send_msg["data"] = {
                        "errorID": 500,
                        "message": "Given parameter start parameter does not exist.",
                    }

            # About event subscribe
            elif dict_msg["messageType"] == "EventSubscriptionRequest":
                event_name = dict_msg["data"]["eventName"]
                # event_cfg = dict_msg["data"]["config"]
                if event_name == "TestEvent":
                    send_msg["data"] = {
                        "yourTestMessage": "text the event will return",
                        "counter": 672,
                    }

            await websocket.send(json.dumps(send_msg))
