""" test vts/vts_request.py """
import pytest
from pyvts import vts_request, config


@pytest.fixture
def default_vts_request():
    """default vts_request"""
    return vts_request.VTSRequest()


def test_vts_request_constructor_kwds():
    """test whether vts_request constructor **kwds works properly"""
    vtsr = vts_request.VTSRequest(api_name="it is not vts", icon="it is an icon")
    assert not vtsr.api_name == config.vts_api["name"]
    assert vtsr.icon is not None
