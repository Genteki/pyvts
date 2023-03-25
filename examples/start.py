import sys
sys.path.insert(0, "../pyvts")

import asyncio
import pyvts

async def main():
    # init vts object
    plugin_info = {
        "plugin_name": "start pyvts",
        "developer": "Genteki",
        "authentication_token_path": "./token.txt"
    }
    vts = pyvts.vts(plugin_info=plugin_info)

    # Connect
    await vts.connect()

    # Authenticate
    await vts.request_authenticate_token() # get token
    await vts.request_authenticate() # use token

    # Custom new parameter named "start_parameter"
    new_parameter_name = "start_parameter"
    msg_new_parameter = vts.vts_request.requestCustomParameter(new_parameter_name) # the message to request custum parameter
    recv_new_parameter = await vts.request(msg_new_parameter) # request custum parameter
    print("received msg after adding the parameter: \n", recv_new_parameter["data"]) # print response message

    # Get the value of "start_parameter"
    msg_get_parameter_value = vts.vts_request.requestParameterValue(new_parameter_name) # the message to get value of new paramter
    new_paraemter_value = await vts.request(msg_get_parameter_value) # request to get value
    print("new parameter value info: \n", new_paraemter_value["data"]) # show
    

    # Delete that parameter
    await asyncio.sleep(10) # sleep 10 seconds
    await vts.request(vts.vts_request.requestDeleteCustomParameter(new_parameter_name)) # delete the parameter

if __name__ == "__main__":
    asyncio.run(main())