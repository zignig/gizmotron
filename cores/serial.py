import itertools

from nmigen.build import Resource, Subsignal, Pins
from nmigen.build import ResourceError

# from .peripheral import Periph, IO, BIT
from .gizmo import Gizmo, IO, BIT

from nmigen import *
from .uart import UART, Loopback
from .uart_nm import UART_nm


class Serial(Gizmo):
    " Uart connection in 4 registers"

    def build(self):
        serial = self.platform.request("uart", self.number)
        clock = self.platform.lookup(self.platform.default_clk).clock
        uart = UART(serial.tx, serial.rx, clock.frequency, self.baud)
        self.add_device(uart)

        tx_status = IO(
            sig_in=uart.TX.tx_ack, sig_out=uart.TX.tx_ready, name="tx_status"
        )
        self.add_reg(tx_status)

        tx_data = IO(sig_out=uart.TX.tx_data, name="tx_data")
        self.add_reg(tx_data)

        rx_status = IO(
            sig_in=uart.RX.rx_ready, sig_out=uart.RX.rx_ack, name="rx_status"
        )
        self.add_reg(rx_status)

        rx_data = IO(sig_in=uart.RX.rx_data, name="rx_data")
        self.add_reg(rx_data)

    def simulate(self):
        pass
