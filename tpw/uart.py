# 20191205
# original https://github.com/tpwrules/ice_panel
# converted to tinyfgpa_bx by Simon Kirkby

# a UART for Boneless

from nmigen import *
from nmigen.lib.cdc import FFSynchronizer
from boneless.arch.opcode import *

# Register Map

# 0x0: (W) Baud Rate / (R) Status
#   Write:   15-0: Baud Rate divisor. rate = (input freq/divisor)-1
#    Read: bit 15: 1 if transmission in progress, 0 otherwise. the transmit
#                  FIFO is empty and the bus is idle iff this bit is 0.
#          bit  0: 1 if reception in progress, 0 otherwise

# 0x1: (R/W) Error
#     R/W: bit 15: 1 if reception encountered framing error. write 1 to reset.
#          bit  1: 1 if transmit FIFO overflowed. write 1 to reset.
#          bit  0: 1 if receive FIFO overflowed. write 1 to reset.

# 0x2: (R/W) Transmit Data / TX FIFO Status
#    Read:  bit 0: 1 if the TX FIFO is full, 0 otherwise.
#   Write:    n-0: queue written character for transmission.

# 0x3: (R) RX FIFO Status and Receive Data
#    Read: bit 15: bit 0 of read character, if the RX FIFO is not empty
#          bit 14: 1 if the RX FIFO is empty, 0 otherwise
#         (n-1)-0: remaining n-1 bits of read character, if RX fifo is not empty
#    this bizarre arrangement is so that ROLI(v, v, 1) sets S to 1 if
#    the character is invalid. otherwise, S is 0 and v is the correctly aligned
#    character.


class SetReset(Elaboratable):
    def __init__(self, parent, *, priority, initial=False):
        # if both set and reset are asserted on the same cycle, the value
        # becomes the prioritized state.
        if priority not in ("set", "reset"):
            raise ValueError(
                "Priority must be either 'set' or 'reset', "
                "not '{}'.".format(priority)
            )

        self.priority = priority

        self.set = Signal()
        self.reset = Signal()
        self.value = Signal(reset=initial)

        # avoid the user having to remember to add us
        parent.submodules += self

    def elaborate(self, platform):
        m = Module()

        if self.priority == "set":
            with m.If(self.set):
                m.d.sync += self.value.eq(1)
            with m.Elif(self.reset):
                m.d.sync += self.value.eq(0)
        elif self.priority == "reset":
            with m.If(self.reset):
                m.d.sync += self.value.eq(0)
            with m.Elif(self.set):
                m.d.sync += self.value.eq(1)

        return m


def calculate_divisor(freq, baud):
    return int(freq / baud) - 1


class SimpleUART(Elaboratable):
    def __init__(self, default_divisor=0, char_bits=8):
        self.default_divisor = default_divisor
        self.char_bits = char_bits
        if char_bits > 15 or char_bits < 1:
            raise ValueError("char width '{}' not in 1-15".format(char_bits))

        # boneless bus inputs. we only have four registers.
        self.i_re = Signal()
        self.i_we = Signal()
        self.i_addr = Signal(2)
        self.o_rdata = Signal(16)
        self.i_wdata = Signal(16)

        # UART signals
        self.i_rx = Signal()
        self.o_tx = Signal(reset=1)  # inverted, like usual

    def elaborate(self, platform):
        m = Module()

        # define the signals that make up the registers
        r0_baud_divisor = Signal(16, reset=self.default_divisor)
        r0_tx_active = Signal()
        r0_rx_active = Signal()

        r1_rx_error = SetReset(m, priority="set")
        r1_tx_overflow = SetReset(m, priority="set")
        r1_rx_overflow = SetReset(m, priority="set")

        r2_tx_full = SetReset(m, priority="reset")
        r2_tx_data = Signal(self.char_bits)

        r3_rx_empty = SetReset(m, priority="reset", initial=True)
        r3_rx_data = Signal(self.char_bits)

        # handle the boneless bus.
        read_data = Signal(16)  # it expects one cycle of read latency
        m.d.sync += self.o_rdata.eq(read_data)

        with m.If(self.i_re):
            with m.Switch(self.i_addr):
                with m.Case(0):  # status register
                    m.d.comb += [
                        read_data[15].eq(r0_tx_active),
                        read_data[0].eq(r0_rx_active),
                    ]
                with m.Case(1):  # error register
                    m.d.comb += [
                        read_data[15].eq(r1_rx_error.value),
                        read_data[1].eq(r1_tx_overflow.value),
                        read_data[0].eq(r1_rx_overflow.value),
                    ]
                with m.Case(2):  # tx fifo status register
                    m.d.comb += read_data[0].eq(r2_tx_full.value)
                with m.Case(3):  # rx fifo status + read data register
                    # we don't really have a FIFO, just a buffer register and an
                    # input shift register. so do FIFO-type logic here.
                    m.d.comb += read_data[14].eq(r3_rx_empty.value)
                    # even if the buffer is "empty", the contents are still
                    # defined. read them out so we don't have to have a mux.
                    m.d.comb += read_data[15].eq(r3_rx_data[0])
                    m.d.comb += read_data[: self.char_bits - 1].eq(r3_rx_data[1:])
                    # and since we have read the only thing out of the buffer,
                    # it's now empty
                    m.d.comb += r3_rx_empty.set.eq(1)
        with m.Elif(self.i_we):
            with m.Switch(self.i_addr):
                with m.Case(0):  # baud rate register
                    m.d.sync += r0_baud_divisor.eq(self.i_wdata)
                with m.Case(1):  # error register
                    m.d.comb += [
                        r1_rx_error.reset.eq(self.i_wdata[15]),
                        r1_tx_overflow.reset.eq(self.i_wdata[1]),
                        r1_rx_overflow.reset.eq(self.i_wdata[0]),
                    ]
                with m.Case(2):  # transmit data register
                    # we don't really have a FIFO, just a staging register and
                    # an output shift register. so do FIFO-type logic here.
                    with m.If(~r2_tx_full.value):
                        m.d.sync += r2_tx_data.eq(self.i_wdata[: self.char_bits])
                        # we've put something in the staging register, so we
                        # can't accept anything else.
                        m.d.comb += r2_tx_full.set.eq(1)
                    with m.Else():  # overflowed! drop the write and raise error.
                        m.d.comb += r1_tx_overflow.set.eq(1)

        # transmit data (written in a function to keep locals under control)
        def tx():
            # count out the bits we're sending (including start and stop)
            bit_ctr = Signal(range(self.char_bits + 2 - 1))
            # shift out the data bits and stop bit
            out_buf = Signal(self.char_bits + 1)
            # count cycles per baud
            baud_ctr = Signal(16)

            with m.FSM("IDLE"):
                with m.State("IDLE"):
                    # once again, no real FIFO. if it's full, then there's
                    # something to transmit.
                    with m.If(r2_tx_full.value):
                        # and once we start transmitting, it's empty.
                        m.d.comb += r2_tx_full.reset.eq(1)
                        m.d.sync += [
                            # load data to send, plus stop bit
                            out_buf.eq(Cat(r2_tx_data, 1)),
                            # start counting down the bits
                            bit_ctr.eq(self.char_bits + 2 - 1),
                            # send the start bit first
                            self.o_tx.eq(0),
                            # start counting the baud time for the start bit
                            baud_ctr.eq(r0_baud_divisor),
                            # finally, let it be known that we are sending
                            r0_tx_active.eq(1),
                        ]
                        m.next = "SEND"  # start sending data bits

                with m.State("SEND"):
                    m.d.sync += baud_ctr.eq(baud_ctr - 1)
                    with m.If(baud_ctr == 0):
                        with m.If(bit_ctr == 0):  # we just sent the stop bit?
                            with m.If(~r2_tx_full.value):
                                # we are done! (iff the FIFO is empty)
                                m.d.sync += r0_tx_active.eq(0)
                                # otherwise, we will restart immediately
                            # the stop bit leaves the bus idle
                            m.next = "IDLE"
                        with m.Else():
                            # nope. shift out the next one and wait for the
                            # appropriate time.
                            m.d.sync += [
                                self.o_tx.eq(out_buf[0]),  # bus is LSB first
                                out_buf.eq(out_buf >> 1),
                                bit_ctr.eq(bit_ctr - 1),  # one less bit to go
                                baud_ctr.eq(r0_baud_divisor),
                            ]
                            m.next = "SEND"

        # receive data (written in a function to keep locals under control)
        def rx():
            # count out the bits we're receiving (including start and stop)
            bit_ctr = Signal(range(self.char_bits + 2 - 1))
            # shift in the data bits, plus start and stop
            in_buf = Signal(self.char_bits + 2)
            # count cycles per baud
            baud_ctr = Signal(16)

            # since the rx pin is attached to arbitrary external logic, we
            # should sync it with our domain first.
            i_rx = Signal(reset=1)
            rx_sync = FFSynchronizer(self.i_rx, i_rx, reset=1)
            m.submodules.rx_sync = rx_sync

            with m.FSM("IDLE"):
                with m.State("IDLE"):
                    # has the receive line been asserted? (todo, maybe debounce
                    # this a couple cycles? is that even a problem?)
                    with m.If(~i_rx):
                        m.d.sync += [
                            # start counting down the bits
                            bit_ctr.eq(self.char_bits + 2 - 1),
                            # and tell the user that we're actively receiving
                            r0_rx_active.eq(1),
                        ]
                        # start the baud counter at half the baud time. this way
                        # we end up halfway through the start bit when we next
                        # sample and can make sure that rx is still asserted.
                        # we're also then lined up to sample the rest of the
                        # bits in the middle.
                        m.d.sync += baud_ctr.eq(r0_baud_divisor >> 1)
                        # then just receive the start bit like any other
                        m.next = "RECV"

                with m.State("RECV"):
                    m.d.sync += baud_ctr.eq(baud_ctr - 1)
                    with m.If(baud_ctr == 0):
                        # sample the bit once it's time. we shift bits into the
                        # MSB so the first bit ends up at the LSB once we are
                        # done.
                        m.d.sync += in_buf.eq(Cat(in_buf[1:], i_rx))
                        with m.If(bit_ctr == 0):  # this is the stop bit?
                            # yes, sample it (this cycle) and finish up next
                            m.next = "FINISH"
                        with m.Else():
                            # no, wait to receive another bit
                            m.d.sync += [
                                baud_ctr.eq(r0_baud_divisor),
                                bit_ctr.eq(bit_ctr - 1),
                            ]

                with m.State("FINISH"):
                    # make sure that the start bit is 0 and the stop bit is 1,
                    # like the standard prescribes.
                    with m.If((in_buf[0] == 0) & (in_buf[-1] == 1)):
                        # store the data to the "FIFO" if we have space
                        with m.If(r3_rx_empty.value):
                            # minus start and stop bits
                            m.d.sync += r3_rx_data.eq(in_buf[1:-1])
                            m.d.comb += r3_rx_empty.reset.eq(1)
                        with m.Else():
                            m.d.comb += r1_rx_overflow.set.eq(1)
                    with m.Else():
                        # we didn't actually receive a character. let
                        # the user know that something bad happened.
                        m.d.comb += r1_rx_error.set.eq(1)
                    # but we did finish receiving no matter what happened
                    m.d.sync += r0_rx_active.eq(0)
                    m.next = "IDLE"
                    # technially, there's still half a bit time until the stop
                    # bit is over, but that's ok. the rx line is deasserted
                    # during that time so we won't accidentally start receiving
                    # another bit.

        # define the two engines
        tx()
        rx()

        return m
