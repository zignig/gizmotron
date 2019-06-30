from nmigen import *


class UART(Elaboratable):
    def __init__(self,tx,rx, clock,baud, data_bits=8):
        self.data_bits = data_bits
        self.divisor   = round(2 ** 32 * baud / clock)
        self.tx_o    = tx 
        self.rx_i    = rx 

        self.tx_data = Signal(data_bits)
        self.tx_rdy  = Signal()
        self.tx_ack  = Signal()

        self.rx_data = Signal(data_bits)
        self.rx_err  = Signal()
        self.rx_ovf  = Signal()
        self.rx_rdy  = Signal()
        self.rx_ack  = Signal()

    def elaborate(self, platform):
        m = Module()

        tx_phase = Signal(max=self.divisor)
        tx_shreg = Signal(1 + self.data_bits + 1, reset=-1)
        tx_count = Signal(max=len(tx_shreg) + 1)

        m.d.comb += self.tx_o.eq(tx_shreg[0])
        with m.If(tx_count == 0):
            m.d.comb += self.tx_ack.eq(1)
            with m.If(self.tx_rdy):
                m.d.sync += [
                    tx_shreg.eq(Cat(C(0, 1), self.tx_data, C(1, 1))),
                    tx_count.eq(len(tx_shreg)),
                    tx_phase.eq(self.divisor - 1),
                ]
        with m.Else():
            with m.If(tx_phase != 0):
                m.d.sync += tx_phase.eq(tx_phase - 1)
            with m.Else():
                m.d.sync += [
                    tx_shreg.eq(Cat(tx_shreg[1:], C(1, 1))),
                    tx_count.eq(tx_count - 1),
                    tx_phase.eq(self.divisor - 1),
                ]

        rx_phase = Signal(max=self.divisor)
        rx_shreg = Signal(1 + self.data_bits + 1, reset=-1)
        rx_count = Signal(max=len(rx_shreg) + 1)

        m.d.comb += self.rx_data.eq(rx_shreg[1:-1])
        with m.If(rx_count == 0):
            m.d.comb += self.rx_err.eq(~(~rx_shreg[0] & rx_shreg[-1]))
            with m.If(~self.rx_i):
                with m.If(self.rx_ack | ~self.rx_rdy):
                    m.d.sync += [
                        self.rx_rdy.eq(0),
                        self.rx_ovf.eq(0),
                        rx_count.eq(len(rx_shreg)),
                        rx_phase.eq(self.divisor // 2),
                    ]
                with m.Else():
                    m.d.sync += self.rx_ovf.eq(1)
        with m.Else():
            with m.If(rx_phase != 0):
                m.d.sync += rx_phase.eq(rx_phase - 1)
            with m.Else():
                m.d.sync += [
                    rx_shreg.eq(Cat(rx_shreg[1:], self.rx_i)),
                    rx_count.eq(rx_count - 1),
                    rx_phase.eq(self.divisor - 1),
                ]
                with m.If(rx_count == 1):
                    m.d.sync += self.rx_rdy.eq(1)

        return m


if __name__ == "__main__":
    tx = Signal()
    rx = Signal()
    uart = UART(tx,rx,9600,300)
    ports = [
        uart.tx_o, uart.rx_i,
        uart.tx_data, uart.tx_rdy, uart.tx_ack,
        uart.rx_data, uart.rx_rdy, uart.rx_err, uart.rx_ovf, uart.rx_ack
    ]

    import argparse

    parser = argparse.ArgumentParser()
    p_action = parser.add_subparsers(dest="action")
    p_action.add_parser("simulate")
    p_action.add_parser("generate")

    args = parser.parse_args()
    if args.action == "simulate":
        from nmigen.hdl.ast import Passive
        from nmigen.back import pysim

        with pysim.Simulator(uart,
                vcd_file=open("uart.vcd", "w"),
                gtkw_file=open("uart.gtkw", "w"),
                traces=ports) as sim:
            sim.add_clock(1e-6)

            def loopback_proc():
                yield Passive()
                while True:
                    yield uart.rx_i.eq((yield uart.tx_o))
                    yield
            sim.add_sync_process(loopback_proc())

            def transmit_proc():
                assert (yield uart.tx_ack)
                assert not (yield uart.rx_rdy)

                yield uart.tx_data.eq(0x5A)
                yield uart.tx_rdy.eq(1)
                yield
                yield uart.tx_rdy.eq(0)
                yield
                assert not (yield uart.tx_ack)

                for _ in range(uart.divisor * 12): 
                    print(uart.tx_o)
                    yield

                assert (yield uart.tx_ack)
                assert (yield uart.rx_rdy)
                assert not (yield uart.rx_err)
                assert (yield uart.rx_data) == 0x5A

                yield uart.rx_ack.eq(1)
                yield
            sim.add_sync_process(transmit_proc())

            sim.run()

    if args.action == "generate":
        from nmigen.back import verilog

        print(verilog.convert(uart, ports=ports))
