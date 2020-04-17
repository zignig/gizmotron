# fifo wrapped uart

from nmigen import *
from nmigen.lib.fifo import SyncFIFO

from .uart import RX, TX
from .gizmo import Gizmo, IO

# need to split this into two FIFO , with a state machine for the strobes
# if this is done in code it is not fast enough and data falls of the end


class _FIFORX(Elaboratable):
    def __init__(self, rx, clk_freq, baud_rate, depth=128):
        # create the components
        self.RX = RX(rx, clk_freq, baud_rate)
        self.RX_FIFO = SyncFIFO(width=8, depth=depth)

        # expose the interface
        self.rx_rdy = self.RX_FIFO.r_rdy
        self.rx_data = self.RX_FIFO.r_data
        self.rx_en = self.RX_FIFO.r_en
        self.rx_strobe = Signal()

    def elaborate(self, platform):
        m = Module()

        # add the UART
        m.submodules.rx = self.RX

        # add the FIFOs
        m.submodules.rx_fifo = self.RX_FIFO

        # bind them together
        # RX
        m.d.comb += [
            self.RX.rx_ack.eq(self.RX_FIFO.w_rdy),
            self.RX_FIFO.w_en.eq(self.RX.rx_ready),
            self.RX_FIFO.w_data.eq(self.RX.rx_data),
        ]
        # state machine for the strobe
        with m.FSM() as fsm:
            with m.State("START"):
                with m.If(self.rx_strobe == 1):
                    m.d.sync += self.rx_en.eq(1)
                    m.next = "DOWN"

            with m.State("DOWN"):
                m.d.sync += self.rx_en.eq(0)
                m.next = "WAIT"

            with m.State("WAIT"):
                with m.If(self.rx_strobe == 0):
                    m.next = "START"

        return m


# This is still broken , fills the FIFO
# the logic to empty it is broken


class _FIFOTX(Elaboratable):
    def __init__(self, tx, clk_freq, baud_rate, depth=128):
        # create the components
        self.TX = TX(tx, clk_freq, baud_rate)
        self.TX_FIFO = SyncFIFO(width=8, depth=depth)

        # expose the interface
        self.tx_rdy = self.TX_FIFO.w_rdy
        self.tx_data = self.TX_FIFO.w_data
        self.tx_en = self.TX_FIFO.w_en
        self.tx_strobe = Signal()

    def elaborate(self, platform):
        m = Module()

        # add the UART
        m.submodules.tx = self.TX

        # add the FIFO
        m.submodules.tx_fifo = self.TX_FIFO

        # TX
        m.d.comb += [
            self.TX_FIFO.r_en.eq(self.TX.tx_ready),
            # self.TX.tx_ready.eq(self.TX_FIFO.r_rdy),
            self.TX.tx_ready.eq(self.TX_FIFO.r_rdy),
            self.TX.tx_data.eq(self.TX_FIFO.r_data),
        ]

        # state machine for the strobe
        with m.FSM() as fsm:
            with m.State("START"):
                with m.If(self.tx_strobe == 1):
                    m.d.sync += self.tx_en.eq(1)
                    m.next = "DOWN"

            with m.State("DOWN"):
                m.d.sync += self.tx_en.eq(0)
                m.next = "WAIT"

            with m.State("WAIT"):
                with m.If(self.tx_strobe == 0):
                    m.next = "START"

        return m


class _FIFOUart(Elaboratable):
    def __init__(self, rx, tx, clk_freq, baud_rate, depth=128):
        self.TX_FIFO = _FIFOTX(tx, clk_freq, baud_rate, depth=depth)
        self.TX = self.TX_FIFO.TX
        self.RX_FIFO = _FIFORX(rx, clk_freq, baud_rate, depth=depth)
        self.RX = self.RX_FIFO.RX

    def elaborate(self, platform):
        m = Module()
        m.submodules.RX_FIFO = self.RX_FIFO
        m.submodules.TX_FIFO = self.TX_FIFO
        return m


class FIFOLoopback(Elaboratable):
    def __init__(self, rx, tx, clk_freq, baud_rate, depth=128):
        self.TX_FIFO = _FIFOTX(tx, clk_freq, baud_rate, depth=depth)
        self.RX_FIFO = _FIFORX(rx, clk_freq, baud_rate, depth=depth)

    def elaborate(self, platform):
        m = Module()
        m.submodules.RX_FIFO = self.RX_FIFO
        m.submodules.TX_FIFO = self.TX_FIFO

        m.d.comb += [
            self.TX_FIFO.w_data.eq(self.RX_FIFO.r_data),
            self.TX_FIFO.r_en.eq(self.RX_FIFO.r_rdy),
        ]

        return m


class FIFOUart(Gizmo):
    def build(self, **kwargs):
        serial = self.platform.request("uart", self.number)
        clock = self.platform.lookup(self.platform.default_clk).clock

        u = _fifouart(
            serial.rx, serial.tx, clock.frequency, self.baud, depth=self.depth
        )
        self.add_device(u)

        # TX
        tx_status = IO(
            sig_out=u.TX_FIFO.tx_strobe, sig_in=u.TX_FIFO.tx_rdy, name="tx_status"
        )
        self.add_reg(tx_status)

        tx_data = IO(sig_out=u.TX_FIFO.tx_data, name="tx_data")
        self.add_reg(tx_data)

        # RX
        rx_status = IO(
            sig_in=u.RX_FIFO.rx_rdy, sig_out=u.RX_FIFO.rx_strobe, name="rx_status"
        )
        self.add_reg(rx_status)

        rx_data = IO(sig_in=u.RX_FIFO.rx_data, name="rx_data")
        self.add_reg(rx_data)


if __name__ == "__main__":
    from ..sim_data import test_rx
    from nmigen.back import pysim, rtlil, verilog

    st = "the quick brown fox jumps over the lazy dog"
    data = sim_data.str_data(st)
    tx = Signal()
    rx = Signal(reset=1)
    fragment = FIFOLoopback(rx, tx, int(16e6), 115200)
    with pysim.Simulator(fragment, vcd_file="fifo_loop.vcd", traces=()) as sim:
        sim.add_clock(100e-6)
        sim.add_sync_process(test_rx(data, dut))
        sim.run_until(100e-6 * 300000, run_passive=True)
