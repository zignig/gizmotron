# Firmware infrastructure for boneless 

from .lister import register

from .uload import uLoader
from .echo import Echo
from .leds import Blinker
from .call_test import Caller

__all__ = ['registers','uart','leds']

def get_bootloader(io=None):
    " get a bootloader image"
    from .uload import uLoader,FakeIO
    if io is None:
        io = FakeIO()
    ul = uLoader(io)
    return ul


available = lister.available

def show():
    return lister.show()
available
