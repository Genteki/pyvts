"""

A python library for interacting with the VTube Studio API

"""

__version__ = "0.3.2"
__all__ = ["vts", "vts_request", "config", "error"]

from .vts import vts
from .vts_request import VTSRequest  # noqa: F401
