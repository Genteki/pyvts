import sys

sys.path.insert(0, "../pyvts")

import asyncio
import pyvts


async def main():
    # init vts object
    plugin_info = {
        "plugin_name": "start pyvts",
        "developer": "Genteki",
        "authentication_token_path": "./token.txt",
    }
    vts = pyvts.vts(plugin_info=plugin_info)

    # Connect
    await vts.connect()

    # Authenticate
    await vts.request_authenticate_token()  # get token
    await vts.request_authenticate()  # use token

    # Custom new parameter named "start_parameter"
    new_parameter_name = "start_parameter"
    recv_new_parameter = await vts.request(
        vts.vts_request.requestCustomParameter(new_parameter_name)
    )  # request custum parameter
    print("received msg after adding the parameter:")
    print(recv_new_parameter["data"])  # print response message

    # Get the value of "start_parameter"
    new_paraemter_value = await vts.request(
        vts.vts_request.requestParameterValue(new_parameter_name)
    )  # request to get value
    print("new parameter value info:")
    print(new_paraemter_value["data"])  # show

    # Delete that parameter
    await asyncio.sleep(3)  # sleep for 3 seconds
    return_msg = await vts.request(
        vts.vts_request.requestDeleteCustomParameter(new_parameter_name)
    )  # delete the parameter
    print(return_msg)


if __name__ == "__main__":
    asyncio.run(main())
