
from nmigen.build import Resource, Subsignal, Pins,Attrs
from boneless_base import Top
from nmigen_boards.resources import *
from nmigen_boards.icebreaker import ICEBreakerPlatform
from nmigen_boards.tinyfpga_bx import TinyFPGABXPlatform


class TinyBoneless(TinyFPGABXPlatform):
    resources = TinyFPGABXPlatform.resources + [
        # FTDI link for now
        Resource(
            "uart",
            0,
            Subsignal("tx", Pins("19", conn=("gpio", 0), dir="o")),
            Subsignal("rx", Pins("20", conn=("gpio", 0), dir="i")),
            Subsignal("dtr", Pins("21", conn=("gpio", 0), dir="i")),
        ),
        *LEDResources(
            "blinky", pins="J1 H2 H9 D9", attrs=Attrs(IO_STANDARD="SB_LVCMOS")
        ),
    ]
    user_flash = (0x50000, 0xFBFFF)


class ICEBreakerBoneless(ICEBreakerPlatform):
    user_flash = (0x20000, 0xFFFFF)


deploy_platform = TinyBoneless #ICEBreakerBoneless

if __name__ == "__main__":
    from cli import main

    def make(simulating):
        platform = deploy_platform()
        design = Top(platform, system_freq_mhz=16)
        return design, platform

    main(maker=make, build_args={"synth_opts": "-abc9"})
