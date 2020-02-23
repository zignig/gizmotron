# return simulator data
from nmigen import *


def char(c):
    d = "{:08b}".format(ord(c))
    print(c, ord(c))
    data = []
    for i in d:
        data.append(int(i))
    data.reverse()
    return data


def str_data(s):
    data = []
    for i in s:
        data.append(char(i))
    return data


def test_rx(data, dut):
    print("test RX")

    def wait():
        print("waiting")
        for i in range(14):
            yield from B(1)

    def T():
        for i in range(dut.RX.divisor):
            yield

    def B(bit):
        yield dut.RX.rx.eq(bit)
        yield from T()

    def S():
        print("START BIT")
        yield from B(0)

    def D(bit):
        print("DATA BIT ", bit)
        yield from B(bit)

    def E():
        print("END BIT")
        yield from B(1)

    def O(bits):
        print("OUT")
        yield from S()
        for bit in bits:
            yield from D(bit)
        yield from E()

    yield dut.RX.rx.eq(1)
    for i in data:
        yield from O(i)
        #yield from wait()


if __name__ == "__main__":
    rx = Signal()
    a = test_rx(rx)
    for i in a:
        i
