# 20191205
# original https://github.com/tpwrules/ice_panel
# converted to tinyfgpa_bx by Simon Kirkby

from nmigen import *
from nmigen.build import *
from nmigen_boards.icebreaker import *
from nmigen_boards.tinyfpga_bx import *

# boneless CPU architecture stuff
from boneless.gateware import ALSRU_4LUT, CoreFSM
from boneless.arch.opcode import Instr
from boneless.arch.opcode import *

import boneload

from pll import PLL
from spram import SPRAM
import uart
import spi


class BonelessBase(Elaboratable):
    def __init__(self, platform):
        self.platform = platform
        if self.platform.device == "iCE40UP5K":
            # lots of spram , use it
            self.depth = 512  # 2 brams for bootloader
            self.split_mem = True
            self.cpu_ram = SPRAM()
        else:
            self.depth = 6 * 1024  # tinyfpga_bx
            self.split_mem = False

        # generate the default memory
        self.cpu_rom = Memory(
            width=16,
            depth=self.depth,
            init=boneload.boneload_fw(platform.user_flash, uart_addr=0, spi_addr=16),
        )

        # create the core
        self.cpu_core = CoreFSM(alsru_cls=ALSRU_4LUT, reset_pc=0xFE00, reset_w=0xFFF8)

        # add a uart
        self.uart = uart.SimpleUART(
            # TODO fix for default clock
            default_divisor=uart.calculate_divisor(12e6, 115200)
        )

        # add the spi flash
        self.spi = spi.SimpleSPI(fifo_depth=512)

    def elaborate(self, platform):
        uart_pins = platform.request("uart")
        spi_pins = platform.request("spi_flash_1x")

        m = Module()
        m.submodules.cpu_core = cpu_core = self.cpu_core
        m.submodules.cpu_rom_r = cpu_rom_r = self.cpu_rom.read_port(transparent=False)
        m.submodules.cpu_rom_w = cpu_rom_w = self.cpu_rom.write_port()

        m.submodules.uart = uart = self.uart
        m.submodules.spi = spi = self.spi

        # split up main bus
        # if this is running on 5k , split the memory into bram and spram
        if self.split_mem:
            m.submodules.cpu_ram = cpu_ram = self.cpu_ram
            rom_en = Signal()
            ram_en = Signal()
            m.d.comb += [
                rom_en.eq(cpu_core.o_bus_addr[-1] == 1),
                ram_en.eq(cpu_core.o_bus_addr[-1] == 0),
            ]
            # we need to know who was enabled one cycle later so we can route the
            # read result back correctly.
            rom_was_en = Signal()
            ram_was_en = Signal()
            m.d.sync += [rom_was_en.eq(rom_en), ram_was_en.eq(ram_en)]
            m.d.comb += [
                # address bus to the memories
                cpu_rom_r.addr.eq(cpu_core.o_bus_addr),
                cpu_rom_w.addr.eq(cpu_core.o_bus_addr),
                cpu_ram.i_addr.eq(cpu_core.o_bus_addr),
                # write data to memories
                cpu_rom_w.data.eq(cpu_core.o_mem_data),
                cpu_ram.i_data.eq(cpu_core.o_mem_data),
                # selects to memories
                cpu_rom_r.en.eq(rom_en & cpu_core.o_mem_re),
                cpu_rom_w.en.eq(rom_en & cpu_core.o_mem_we),
                cpu_ram.i_re.eq(ram_en & cpu_core.o_mem_re),
                cpu_ram.i_we.eq(ram_en & cpu_core.o_mem_we),
            ]
            # read results back to cpu
            with m.If(rom_was_en):
                m.d.comb += cpu_core.i_mem_data.eq(cpu_rom_r.data)
            with m.Elif(ram_was_en):
                m.d.comb += cpu_core.i_mem_data.eq(cpu_ram.o_data)
        else:
            # single bram array for memory
            m.d.comb += [
                # address bus to the memories
                cpu_rom_r.addr.eq(cpu_core.o_bus_addr),
                cpu_rom_w.addr.eq(cpu_core.o_bus_addr),
                # write data to memories
                cpu_rom_w.data.eq(cpu_core.o_mem_data),
                # selects to memories
                cpu_rom_r.en.eq(cpu_core.o_mem_re),
                cpu_rom_w.en.eq(cpu_core.o_mem_we),
                cpu_core.i_mem_data.eq(cpu_rom_r.data),
            ]

        # TODO , this is a simple reg layout that works well
        # TODO , convert to Peripheral form

        # split up the external bus into 8 regions of 16 registers. this way,
        # all of them can be addressed absolutely. of course, the panel
        # framebuffer is special and gets the entire top half of the address
        # space to itself.
        periph_en = Signal(8)
        ext_addr = cpu_core.o_bus_addr
        ext_old_addr = Signal(16)
        for x in range(8):
            m.d.comb += periph_en[x].eq((ext_addr[-1] == 0) & (ext_addr[4:7] == x))
        m.d.sync += ext_old_addr.eq(ext_addr)

        periph_was_en = Signal(8)
        m.d.sync += periph_was_en.eq(periph_en)

        # plus the UART as peripheral 0
        uart_en = periph_en[0]
        uart_was_en = periph_was_en[0]
        m.d.comb += [
            # peripheral to bus
            uart.i_re.eq(cpu_core.o_ext_re & uart_en),
            uart.i_we.eq(cpu_core.o_ext_we & uart_en),
            uart.i_addr.eq(ext_addr[:2]),
            uart.i_wdata.eq(cpu_core.o_ext_data),
            # peripheral to outside world
            uart.i_rx.eq(uart_pins.rx),
            uart_pins.tx.eq(uart.o_tx),
        ]
        with m.If(uart_was_en):
            m.d.comb += cpu_core.i_ext_data.eq(uart.o_rdata)

        # plus the SPI flash as peripheral 1
        spi_en = periph_en[1]
        spi_was_en = periph_was_en[1]
        m.d.comb += [
            # peripheral to bus
            spi.i_re.eq(cpu_core.o_ext_re & spi_en),
            spi.i_we.eq(cpu_core.o_ext_we & spi_en),
            spi.i_addr.eq(ext_addr[:1]),
            spi.i_wdata.eq(cpu_core.o_ext_data),
            # peripheral to outside world
            spi_pins.clk.eq(spi.o_clk),
            spi_pins.cs.eq(~spi.o_cs),
            spi_pins.mosi.eq(spi.o_mosi),
            spi.i_miso.eq(spi_pins.miso),
        ]
        with m.If(spi_was_en):
            m.d.comb += cpu_core.i_ext_data.eq(spi.o_rdata)

        return m


# super top domain to manage clock stuff
class Top(Elaboratable):
    def __init__(self, platform, led_freq_mhz=12):
        self.led_freq_mhz = led_freq_mhz
        self.platform = platform

    def elaborate(self, platform):
        m = Module()
        # TODO , get default clock instead , Boneless can run @ 24MHz ,
        if self.led_freq_mhz != 12:
            # we need a PLL so we can boost the clock. reserve the clock pin
            # before it gets switched to the default domain.
            clk_pin = platform.request(platform.default_clk, dir="-")
            # then create the PLL
            pll = PLL(
                12,
                self.led_freq_mhz,
                clk_pin,
                orig_domain_name="cpu",  # runs at 12MHz
                pll_domain_name="base",  # runs at the LED frequency
            )
            m.submodules.pll = pll
            base_domain = "base"
        else:
            # the user doesn't want to run faster and the PLL can't make
            # input = output, so just create the CPU domain using the default
            # clock and run the LEDs in that domain too.
            cpu = ClockDomain("cpu")
            m.domains += cpu
            m.d.comb += ClockSignal("cpu").eq(ClockSignal("sync"))
            base_domain = "cpu"

        # create the actual processor and tell it to run in the domain we made
        # for it above
        boneless_base = BonelessBase(platform)

        # remap the default sync domain to the CPU domain, since most logic
        # should run there.
        boneless_base = DomainRenamer("cpu")(boneless_base)

        m.submodules.boneless_base = boneless_base

        return m


if __name__ == "__main__":
    from cli import main

    def make(simulating):
        design = Top(
            # we can't simulate with different LED and CPU frequencies
            led_freq_mhz=12
        )
        # platform = ICEBreakerPlatform()
        platform = TinyFPGABXPlatform()
        platform.add_resources(
            [
                Resource(
                    "uart",
                    0,
                    Subsignal("tx", Pins("19", conn=("gpio", 0), dir="o")),
                    Subsignal("rx", Pins("20", conn=("gpio", 0), dir="i")),
                )
            ]
        )
        return design, platform

    main(maker=make, build_args={"synth_opts": "-abc9"})
