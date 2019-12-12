import itertools

from nmigen.build import Resource, Subsignal, Pins
from nmigen.build import ResourceError
from nmigen import *


class Leds(Elaboratable):
    def __init__(self):
        self.i_re = Signal()
        self.i_we = Signal()
        self.i_addr = Signal(1)
        self.o_rdata = Signal(16)
        self.i_wdata = Signal(16)
        self.val = Signal(16)

    def elaborate(self,platform):
        m = Module()

        def get_all_resources(name):
            resources = []
            for number in itertools.count():
                try:
                    resources.append(platform.request(name, number))
                except ResourceError:
                    break
            return resources

        leds = [res.o for res in get_all_resources("led")]
        leds = Cat(led for led in leds)
        with m.If(self.i_we):
            m.d.sync += leds.eq(self.i_wdata)
            m.d.sync += self.val.eq(self.i_wdata)
        with m.If(self.i_re):
            m.d.sync += self.o_rdata.eq(self.val)
        return m
