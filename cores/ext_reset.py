from nmigen import *
import itertools

from nmigen.build import Resource, Subsignal, Pins
from nmigen.build import ResourceError

# external reset ( used on DTR pin )
# count the pin toggles within the timeout
# warm boot based on count


class ExternalReset(Elaboratable):
    def __init__(self, select, image, boot, pin):
        self.select = select
        self.image = image
        self.boot = boot
        self.pin = pin
        self.timeout = int(8e6)

    def elaborate(self, platform):
        m = Module()

        # leds for debug
        leds = []
        for n in itertools.count():
            try:
                l = platform.request("blinky", n)
                leds.append(l)

            except ResourceError:
                # print("run out of blinky", n)
                break
        print(leds)
        leds_cat = Cat(led.o for led in leds)

        counter = Signal(32)
        enable = Signal()  # enable the counter
        current = Signal()  # get the current pin state
        toggle_count = Signal(5)  # count the pin toggles

        with m.If(enable == 1):
            m.d.sync += counter.eq(counter + 1)

        # display the pin status on the first led
        # m.d.sync += self.status.eq(self.pin)
        # m.d.sync += leds_cat.eq(self.pin)
        m.d.sync += leds_cat.eq(toggle_count)

        with m.FSM() as fsm:
            with m.State("INIT"):
                # get the current pin state
                m.d.sync += current.eq(self.pin)
                # reset everything
                m.d.sync += enable.eq(0)
                m.d.sync += counter.eq(0)
                m.d.sync += toggle_count.eq(0)
                m.next = "START"

            with m.State("START"):
                # if the pin state has changed
                with m.If(self.pin != current):
                    # start the counter
                    m.d.sync += toggle_count.eq(toggle_count + 1)
                    m.d.sync += enable.eq(1)
                    # save the new state
                    m.d.sync += current.eq(self.pin)
                    m.next = "COUNT"

            with m.State("COUNT"):
                # count the toggles
                with m.If(self.pin != current):
                    m.d.sync += toggle_count.eq(toggle_count + 1)
                    m.next = "NEXT"
                with m.If(counter == self.timeout):
                    m.next = "CHOOSE"

            with m.State("NEXT"):
                m.d.sync += current.eq(self.pin)
                m.next = "COUNT"

            with m.State("CHOOSE"):
                # switch the warmboot to external
                m.d.sync += self.select.eq(1)
                # select the image count based on toggles
                with m.Switch(toggle_count):
                    with m.Case(4):
                        m.next = "IMAGE1"
                    with m.Case(8):
                        m.next = "IMAGE2"
                    with m.Default():
                        m.next = "INIT"
                # ? 7 reset the boneless ?

            with m.State("IMAGE1"):
                # select image 0
                m.d.sync += self.image.eq(0)
                m.next = "WARMBOOT"

            with m.State("IMAGE2"):
                # select image 1
                m.d.sync += self.image.eq(1)
                m.next = "WARMBOOT"

            with m.State("WARMBOOT"):
                # warmboot
                m.d.sync += self.boot.eq(1)
        return m
