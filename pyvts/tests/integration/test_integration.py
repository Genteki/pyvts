""" integration test """
import pytest
import pyvts
from ..test_utils import FakeVtubeStudioAPIServer

pytest_plugins = ("pytest_asyncio",)
PORT = 8001


@pytest.mark.asyncio
async def test_integration():
    """integration test
    step 01 make connection
    step 02 get auth code
    step 03 do action needs authentication (rejected)
    step 04 auth
    step 05 do action needs authentication (approved)
    step 06 close
    """
    # step 01
    fake_server = FakeVtubeStudioAPIServer()
    await fake_server.start(port=PORT)
    myvts = pyvts.vts(port=PORT)
    await myvts.connect()
    assert myvts.get_connection_status() == 1

    # step 02
    await myvts.request_authenticate_token()
    assert myvts.get_authentic_status() == 1

    # step 04
    await myvts.request_authenticate()

    # step 06
    await myvts.close()
    await fake_server.stop()
