""" unit test for vts.py """
import pytest
import pyvts
from unittest.mock import patch, AsyncMock, MagicMock
from .test_utils import FakeVtubeStudioAPIServer

pytest_plugins = ("pytest_asyncio",)
PORT = 8456

@pytest.fixture
def myvts():
    return pyvts.vts(port=PORT)


def test_vts_kwargs():
    api_name = "it is not vts"
    icon = "it is an icon"
    myvts = pyvts.vts(api_name=api_name, icon=icon)
    assert myvts.api_name == api_name
    assert myvts.vts_request.api_name == api_name
    assert myvts.icon == icon
    assert myvts.vts_request.icon == icon


@pytest.mark.asyncio
async def test_vts_write_read_token(myvts: pyvts.vts):
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
    fake_server = FakeVtubeStudioAPIServer()
    await fake_server.start(port=PORT)
    await myvts.connect()
    assert myvts.get_connection_status(), "connection failed"
    await myvts.close()
    assert not myvts.get_authentic_status(), "connection didn't close properly"
    await fake_server.stop()


@pytest.mark.asyncio
async def test_vts_authenticate(myvts: pyvts.vts):
    fake_server = FakeVtubeStudioAPIServer()
    await fake_server.start(port=PORT)
    await myvts.connect()
    await myvts.request_authenticate_token()
    assert myvts.get_authentic_status() == 1, myvts.authentic_token
    await myvts.request_authenticate()
    assert myvts.get_authentic_status() == 2

    await myvts.close()
    await fake_server.stop()
