# Firmware infrastructure for boneless 

__all__ = ['registers','uart','leds']

def get_bootloader(io=None):
    " get a bootloader image"
    from .uload import uLoader,FakeIO
    if io is None:
        io = FakeIO()
    ul = uLoader(io)
    return ul
