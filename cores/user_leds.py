import itertools

from nmigen.build import Resource, Subsignal, Pins
from nmigen.build import ResourceError
from .gizmo import Gizmo, IO, BIT

from nmigen import *


class UserLeds(Gizmo):
    def build(self):
        leds = []
        if self.source is None:
            self.source = "user_leds"
        for n in itertools.count():
            try:
                l = self.platform.request(self.source, n)
                print(l)
                leds.append(l)
            except ResourceError:
                break

        leds_cat = Cat(led.o for led in leds)
        o = IO(sig_out=leds_cat, name=self.source)
        for i, j in enumerate(leds):
            o.add_bit(BIT(self.source+"_led_" + str(i), i))
        self.add_reg(o)
