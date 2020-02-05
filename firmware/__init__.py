# Firmware infrastructure for boneless 

def get_bootloader(io=None):
    " get a bootloader image"
    from .uload import uLoader,FakeIO
    if io is None:
        io = FakeIO()
    ul = uLoader(io)
    return ul
