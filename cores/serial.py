import itertools

from nmigen.build import Resource, Subsignal, Pins
from nmigen.build import ResourceError

# from .peripheral import Periph, IO, BIT
from .gizmo import Gizmo, IO, BIT

from nmigen import *
from .uart import UART, Loopback
from .uart_nm import UART_nm


class Serial_nm(Gizmo):
    " Uart connection in 4 registers"

    def build(self):
        serial = self.platform.request("uart", self.number)
        print(serial)
        clock = self.platform.lookup(self.platform.default_clk).clock
        uart = UART_nm(serial.tx, serial.rx, clock.frequency, self.baud)
        self.add_device(uart)

        # TX
        tx_status = IO(sig_in=uart.tx_ack, sig_out=uart.tx_rdy, name="tx_status")
        self.add_reg(tx_status)

        tx_data = IO(sig_out=uart.tx_data, name="tx_data")
        self.add_reg(tx_data)

        # RX
        rx_status = IO(sig_in=uart.rx_rdy, sig_out=uart.rx_ack, name="rx_status")
        self.add_reg(rx_status)

        rx_data = IO(sig_in=uart.rx_data, name="rx_data")
        self.add_reg(rx_data)

    def simulate(self):
        pass


class Serial(Gizmo):
    " Uart connection in 4 registers"

    def build(self):
        serial = self.platform.request("uart", self.number)
        print(serial)
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
