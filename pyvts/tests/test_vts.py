""" unit test for vts.py """
import pytest
import pyvts
from .test_utils import FakeVtubeStudioAPIServer

pytest_plugins = ("pytest_asyncio",)
PORT = 8001


@pytest.fixture
def myvts():
    """set up vts class for test"""
    return pyvts.vts(port=PORT)


def test_vts_kwargs():
    """test whether vts constructor **kwargs work properly"""
    api_name = "it is not vts"
    icon = "it is an icon"
    myvts = pyvts.vts(api_name=api_name, icon=icon)
    assert myvts.api_name == api_name
    assert myvts.vts_request.api_name == api_name
    assert myvts.icon == icon
    assert myvts.vts_request.icon == icon


@pytest.mark.asyncio
async def test_vts_write_read_token(myvts: pyvts.vts):
    """test the functions to read token from file and save token to file"""
    first_token_test = "it is a token"
    second_token_test = "it is another token"
    # first token test
    myvts.authentic_token = first_token_test
    await myvts.write_token()  # first write
    myvts.authentic_token = None  # clear token
    await myvts.read_token()
    assert (
        myvts.authentic_token == first_token_test
    ), "Read Token Is Different To The Written Token"

    # second token test
    myvts.authentic_token = second_token_test
    await myvts.write_token()
    myvts.authentic_token = None  # clear token
    await myvts.read_token()
    assert (
        myvts.authentic_token == second_token_test
    ), "Read Token Is Different To The Rewritten Token"


@pytest.mark.asyncio
async def test_vts_connect(myvts: pyvts.vts):
    """test the function to conncect to vts api server"""
    fake_server = FakeVtubeStudioAPIServer()
    await fake_server.start(port=PORT)
    await myvts.connect()
    assert myvts.get_connection_status(), "connection failed"
    await myvts.close()
    assert not myvts.get_authentic_status(), "connection didn't close properly"
    await fake_server.stop()


@pytest.mark.asyncio
async def test_vts_authenticate(myvts: pyvts.vts):
    """test vts functions to get authentic token and get authenicated from vts api"""
    fake_server = FakeVtubeStudioAPIServer()
    await fake_server.start(port=PORT)
    await myvts.connect()
    await myvts.request_authenticate_token()
    assert myvts.get_authentic_status() == 1, myvts.authentic_token
    await myvts.request_authenticate()
    assert myvts.get_authentic_status() == 2

    await myvts.close()
    await fake_server.stop()


@pytest.mark.asyncio
async def test_vts_custon_parameter(myvts: pyvts.vts):
    """test vts functions about custom parameters"""
    fake_server = FakeVtubeStudioAPIServer()
    await fake_server.start(port=PORT)
    await myvts.connect()
    param_name = "test"
    # create custom parameter
    await myvts.request(
        myvts.vts_request.requestCustomParameter(param_name, default_value=0)
    )
    custom_param_value = await myvts.request(
        myvts.vts_request.requestParameterValue(param_name)
    )
    assert custom_param_value["data"]["value"] == 0
    # set value for this parameter
    await myvts.request(
        myvts.vts_request.requestSetParameterValue(parameter=param_name, value=0.5)
    )
    custom_param_value = await myvts.request(
        myvts.vts_request.requestParameterValue(param_name)
    )
    assert custom_param_value["data"]["value"] == 0.5
    # delete parameter
    await myvts.request(myvts.vts_request.requestDeleteCustomParameter(param_name))
    custom_param_value = await myvts.request(
        myvts.vts_request.requestParameterValue(param_name)
    )
    assert custom_param_value["data"]["errorID"] == 500
    await myvts.close()
    await fake_server.stop()


@pytest.mark.asyncio
async def test_vts_event_subscription(myvts: pyvts.vts):
    """test vts functions about event subscribe"""
    fake_server = FakeVtubeStudioAPIServer()
    await fake_server.start(port=PORT)
    await myvts.connect()
    # send subscribe request
    subscribe_msg = myvts.vts_request.eventSubscriptionTest()
    return_msg = await myvts.request(subscribe_msg)
    assert (
        return_msg["data"]["yourTestMessage"]
        == subscribe_msg["data"]["config"]["testMessageForEvent"]
    )
    # end the test
    await myvts.close()
    await fake_server.stop()
