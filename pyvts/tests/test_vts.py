import pytest
import pyvts

pytest_plugins = ('pytest_asyncio',)

@pytest.fixture
def myvts():
    return pyvts.vts()

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
    myvts._authentic_status = 1
    await myvts.write_token() # first write
    myvts.authentic_token = None; myvts._authentic_status = 0  # clear token
    await myvts.read_token()
    assert myvts.authentic_token == first_token_test, \
        "Read Token Is Different To The Written Token"

    # second token test
    myvts.authentic_token = second_token_test; myvts._authentic_status = 1
    await myvts.write_token()
    myvts.authentic_token = None; myvts._authentic_status = 0 # clear token
    await myvts.read_token()
    assert myvts.authentic_token == second_token_test, \
        "Read Token Is Different To The Rewritten Token"
