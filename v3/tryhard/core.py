from nmigen import *

from opcode_v3 import *

# from .formal import *
from alsru import *


class Arbiter:
    MUX_ADDR_REG = 0b0
    MUX_ADDR_PTR = 0b1

    MUX_REG_x = 0
    MUX_REG_A = 0b00
    MUX_REG_B = 0b01
    MUX_REG_SD = 0b10

    MUX_OP_RD = 0b0
    MUX_OP_WR = 0b1

    CTRL_SIZE = 4

    CTRL_LD_PTR = Cat(C(MUX_ADDR_PTR, 1), C(MUX_REG_x, 2), C(MUX_OP_RD, 1))
    CTRL_ST_PTR = Cat(C(MUX_ADDR_PTR, 1), C(MUX_REG_x, 2), C(MUX_OP_WR, 1))
    CTRL_LD_RA = Cat(C(MUX_ADDR_REG, 1), C(MUX_REG_A, 2), C(MUX_OP_RD, 1))
    CTRL_LD_RB = Cat(C(MUX_ADDR_REG, 1), C(MUX_REG_B, 2), C(MUX_OP_RD, 1))
    CTRL_LD_RSD = Cat(C(MUX_ADDR_REG, 1), C(MUX_REG_SD, 2), C(MUX_OP_RD, 1))
    CTRL_ST_RSD = Cat(C(MUX_ADDR_REG, 1), C(MUX_REG_SD, 2), C(MUX_OP_WR, 1))

    def __init__(self, rdport, wrport):
        self.rdport = rdport
        self.wrport = wrport

        self.i_w = Signal(13)
        self.i_ra = Signal(3)
        self.i_rb = Signal(3)
        self.i_rsd = Signal(3)
        self.i_ptr = Signal(16)

        self.i_data = Signal(16)
        self.o_data = Signal(16)

        self.s_addr = Signal(16)

        self.ctrl = Record([("addr", 1), ("reg", 2), ("op", 1)])

    def get_fragment(self, platform):
        m = Module()

        m.submodules.rdport = self.rdport
        m.submodules.wrport = self.wrport

        with m.Switch(self.ctrl.addr):
            with m.Case(self.MUX_ADDR_REG):
                with m.Switch(self.ctrl.reg):
                    with m.Case(self.MUX_REG_A):
                        m.d.comb += self.s_addr.eq(Cat(self.i_ra, self.i_w))
                    with m.Case(self.MUX_REG_B):
                        m.d.comb += self.s_addr.eq(Cat(self.i_rb, self.i_w))
                    with m.Case(self.MUX_REG_SD):
                        m.d.comb += self.s_addr.eq(Cat(self.i_rsd, self.i_w))
            with m.Case(self.MUX_ADDR_PTR):
                m.d.comb += self.s_addr.eq(self.i_ptr)

        with m.Switch(self.ctrl.op):
            m.d.comb += self.rdport.en.eq(1)
            with m.Case(self.MUX_OP_RD):
                m.d.comb += self.wrport.en.eq(0)
            with m.Case(self.MUX_OP_WR):
                m.d.comb += self.wrport.en.eq(1)

        m.d.comb += [
            self.rdport.addr.eq(self.s_addr),
            self.wrport.addr.eq(self.s_addr),
            self.o_data.eq(self.rdport.data),
            self.wrport.data.eq(self.i_data),
        ]

        return m.lower(platform)


class Decoder:
    IMM3_AL_TABLE = Array([0x0000, 0x0001, 0, 0, 0, 0x00FF, 0xFF00, 0xFFFF])
    IMM3_SR_TABLE = Array([1, 2, 3, 4, 5, 6, 7, 8])

    CTRL_CI_ZERO = 0b00
    CTRL_CI_ONE = 0b01
    CTRL_CI_FLAG = 0b10

    CTRL_SI_ZERO = 0b0
    CTRL_SI_MSB = 0b1

    CTRL_OPB_REG = 0b0
    CTRL_OPB_IMM = 0b1

    CTRL_LS_READ = 0b0
    CTRL_LS_WRITE = 0b1

    def __init__(self, alsru_cls):
        self.alsru_cls = alsru_cls

        self.i_insn = Signal(16)

        self.o_ra = Signal(3)
        self.o_rb = Signal(3)
        self.o_rsd = Signal(3)
        self.o_imm = Signal(16)

        self.c_alsru = Signal(alsru_cls.CTRL_BITS, decoder=alsru_cls.ctrl_decoder)
        self.c_ci = Signal(2)
        self.c_si = Signal(1)
        self.c_opb = Signal(1)
        self.c_ls_rw = Signal()
        self.c_ls_ra = Signal()
        self.c_ls_pc = Signal()

        self.r_ext13 = Signal(13)
        self.r_ext_v = Signal()

    def get_fragment(self, platform):
        m = Module()

        def decode(v):
            d = Signal.like(v, src_loc_at=1)
            m.d.comb += d.eq(v)
            return d

        i_insn = self.i_insn

        d_code3 = decode(i_insn[13:16])
        d_code4 = decode(i_insn[12:16])
        d_code5 = decode(i_insn[11:16])
        d_ri = decode(i_insn[11])
        d_type2 = decode(i_insn[3:5])

        d_imm3 = decode(i_insn[0:3])
        d_imm5 = decode(i_insn[0:5])
        d_imm8 = decode(i_insn[0:8])
        d_imm13 = decode(i_insn[0:13])

        d_cond = decode(i_insn[8:10])
        d_flag = decode(i_insn[11])

        d_rb = decode(i_insn[0:3])
        d_ra = decode(i_insn[5:8])
        d_rsd = decode(i_insn[8:11])

        m.d.comb += [self.o_ra.eq(d_ra), self.o_rb.eq(d_rb), self.o_rsd.eq(d_rsd)]

        r_ext13 = self.r_ext13
        r_ext_v = self.r_ext_v
        with m.If(d_code3 == OPCODE3_EXTI):
            m.d.sync += r_ext13.eq(d_imm13)
            m.d.sync += r_ext_v.eq(1)
        with m.Else():
            m.d.sync += r_ext_v.eq(0)

        s_imm_w = Signal(2)
        IMM_W_3_AL = 0b00
        IMM_W_3_SR = 0b01
        IMM_W_5 = 0b10
        IMM_W_8 = 0b11

        o_imm = self.o_imm
        with m.If(r_ext_v):
            m.d.comb += o_imm.eq(Cat(d_imm3, r_ext13))
        with m.Else():
            with m.Switch(s_imm_w):
                with m.Case(IMM_W_3_AL):
                    m.d.comb += o_imm.eq(self.IMM3_AL_TABLE[d_imm3])
                with m.Case(IMM_W_3_SR):
                    m.d.comb += o_imm.eq(self.IMM3_SR_TABLE[d_imm3])
                with m.Case(IMM_W_5):
                    m.d.comb += o_imm.eq(Cat(d_imm5, Repl(d_imm5[-1], 11)))
                with m.Case(IMM_W_8):
                    m.d.comb += o_imm.eq(Cat(d_imm8, Repl(d_imm8[-1], 8)))

        alsru_cls = self.alsru_cls
        c_alsru = self.c_alsru
        c_opb = self.c_opb
        c_ci = self.c_ci
        c_si = self.c_si
        with m.Switch(d_code4):
            with m.Case(OPCODE4_LOGIC):
                m.d.comb += c_opb.eq(d_ri)
                with m.Switch(d_type2):
                    with m.Case(OPTYPE2_AND):
                        m.d.comb += c_alsru.eq(alsru_cls.CTRL_AaB)
                    with m.Case(OPTYPE2_OR):
                        m.d.comb += c_alsru.eq(alsru_cls.CTRL_AoB)
                    with m.Case(OPTYPE2_XOR):
                        m.d.comb += c_alsru.eq(alsru_cls.CTRL_AxB)
                    with m.Case(OPTYPE2_CMP):
                        m.d.comb += c_alsru.eq(alsru_cls.CTRL_AmB)
            with m.Case(OPCODE4_ARITH):
                m.d.comb += c_opb.eq(d_ri)
                with m.Switch(d_type2):
                    with m.Case(OPTYPE2_ADD):
                        m.d.comb += c_alsru.eq(alsru_cls.CTRL_ApB)
                        m.d.comb += c_ci.eq(self.CTRL_CI_ZERO)
                    with m.Case(OPTYPE2_ADC):
                        m.d.comb += c_alsru.eq(alsru_cls.CTRL_ApB)
                        m.d.comb += c_ci.eq(self.CTRL_CI_FLAG)
                    with m.Case(OPTYPE2_SUB):
                        m.d.comb += c_alsru.eq(alsru_cls.CTRL_AmB)
                        m.d.comb += c_ci.eq(self.CTRL_CI_ONE)
                    with m.Case(OPTYPE2_SBB):
                        m.d.comb += c_alsru.eq(alsru_cls.CTRL_AmB)
                        m.d.comb += c_ci.eq(self.CTRL_CI_FLAG)
            with m.Case(OPCODE4_SHIFT):
                m.d.comb += c_opb.eq(d_ri)
                with m.Switch(d_type2):
                    with m.Case(OPTYPE2_SLL):
                        m.d.comb += c_alsru.eq(alsru_cls.CTRL_SL)
                        m.d.comb += c_si.eq(self.CTRL_SI_ZERO)
                    with m.Case(OPTYPE2_ROT):
                        m.d.comb += c_alsru.eq(alsru_cls.CTRL_SL)
                        m.d.comb += c_si.eq(self.CTRL_SI_MSB)
                    with m.Case(OPTYPE2_SRL):
                        m.d.comb += c_alsru.eq(alsru_cls.CTRL_SR)
                        m.d.comb += c_si.eq(self.CTRL_SI_ZERO)
                    with m.Case(OPTYPE2_SRA):
                        m.d.comb += c_alsru.eq(alsru_cls.CTRL_SR)
                        m.d.comb += c_si.eq(self.CTRL_SI_MSB)

        return m.lower(platform)


class CoreFSM:
    def __init__(self, mem_rdport, mem_wrport, alsru_cls):
        # self.formal  = BonelessFormalInterface(mem_wrport=mem_wrport)
        self.alsru = alsru_cls(width=16)
        self.decoder = Decoder(alsru_cls)
        self.arbiter = Arbiter(mem_rdport, mem_wrport)

        self.r_pc = Signal(16)
        self.r_w = Signal(13)
        self.r_f = Record([("z", 1), ("s", 1), ("c", 1), ("v", 1)])
        self.r_p = Signal(16)
        self.r_q = Signal(16)
        self.s_r = Signal(16)

    def get_fragment(self, platform):
        m = Module()

        m.submodules.formal = formal = self.formal
        m.submodules.decoder = decoder = self.decoder
        m.submodules.arbiter = arbiter = self.arbiter
        m.submodules.alsru = alsru = self.alsru

        r_pc = self.r_pc
        r_w = self.r_w
        r_f = self.r_f
        r_p = self.r_p
        r_q = self.r_q
        s_r = self.s_r

        m.d.comb += [r_w.eq(0), formal.flags.eq(r_f)]  # FIXME

        m.d.comb += [
            arbiter.i_w.eq(r_w),
            arbiter.i_ra.eq(decoder.o_ra),
            arbiter.i_rb.eq(decoder.o_rb),
            arbiter.i_rsd.eq(decoder.o_rsd),
            arbiter.i_data.eq(s_r),
        ]

        m.d.comb += [
            alsru.a.eq(r_p),
            alsru.b.eq(r_q),
            s_r.eq(alsru.o),
            alsru.ctrl.eq(decoder.c_alsru),
        ]
        with m.Switch(decoder.c_ci):
            with m.Case(decoder.CTRL_CI_ZERO):
                m.d.comb += alsru.ci.eq(0)
            with m.Case(decoder.CTRL_CI_ONE):
                m.d.comb += alsru.ci.eq(1)
            with m.Case(decoder.CTRL_CI_FLAG):
                m.d.comb += alsru.ci.eq(r_f.c)
        with m.Switch(decoder.c_si):
            with m.Case(decoder.CTRL_SI_ZERO):
                m.d.comb += alsru.si.eq(0)
            with m.Case(decoder.CTRL_SI_MSB):
                m.d.comb += alsru.si.eq(s_r[-1])

        with m.FSM():
            with m.State("FETCH"):
                m.d.comb += arbiter.i_ptr.eq(r_pc)
                m.d.comb += arbiter.ctrl.eq(arbiter.CTRL_LD_PTR)
                m.d.sync += formal.pc.eq(r_pc)
                m.next = "DECODE"

            with m.State("DECODE"):
                m.d.sync += decoder.i_insn.eq(arbiter.o_data)
                m.d.sync += formal.insn.eq(arbiter.o_data)
                m.next = "LOAD-P"

            with m.State("LOAD-P"):
                m.d.comb += arbiter.ctrl.eq(arbiter.CTRL_LD_RA)
                m.next = "LOAD-Q"

            with m.State("LOAD-Q"):
                m.d.sync += r_p.eq(arbiter.o_data)
                m.d.comb += arbiter.ctrl.eq(arbiter.CTRL_LD_RB)
                m.next = "EXECUTE"

            with m.State("EXECUTE"):
                with m.Switch(decoder.c_opb):
                    with m.Case(Decoder.CTRL_OPB_REG):
                        m.d.sync += r_q.eq(arbiter.o_data)
                    with m.Case(Decoder.CTRL_OPB_IMM):
                        m.d.sync += r_q.eq(decoder.o_imm)
                m.next = "STORE-R"

            with m.State("STORE-R"):
                m.d.comb += arbiter.ctrl.eq(arbiter.CTRL_ST_RSD)
                m.d.sync += r_pc.eq(r_pc + 1)  # FIXME
                m.d.comb += formal.stb.eq(1)
                m.next = "FETCH"

        return m.lower(platform)


# -------------------------------------------------------------------------------------------------

import argparse
from nmigen import cli


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("type", choices=["arbiter", "decoder", "core-fsm"])
    cli.main_parser(parser)

    args = parser.parse_args()

    if args.type == "arbiter":
        mem = Memory(width=16, depth=256)
        dut = Arbiter(rdport=mem.read_port(transparent=False), wrport=mem.write_port())
        ports = (
            dut.i_w,
            dut.i_ra,
            dut.i_rb,
            dut.i_rsd,
            dut.i_ptr,
            dut.i_data,
            dut.o_data,
            dut.ctrl.ptr,
            dut.ctrl.reg,
            dut.ctrl.op,
        )

    if args.type == "decoder":
        dut = Decoder(alsru_cls=ALSRU_4LUT)
        ports = (
            dut.i_insn,
            dut.o_ra,
            dut.o_rb,
            dut.o_rsd,
            dut.o_imm,
            dut.c_alsru,
            dut.c_ci,
            dut.c_si,
            dut.r_ext13,
            dut.r_ext_v,
        )

    if args.type == "core-fsm":
        mem = Memory(width=16, depth=256)
        import random

        random.seed(0)
        mem.init = [random.randint(0x0000, 0xFFFF) for _ in range(256)]
        dut = CoreFSM(
            mem_rdport=mem.read_port(transparent=False),
            mem_wrport=mem.write_port(),
            alsru_cls=ALSRU_4LUT,
        )
        ports = ()

    cli.main_runner(parser, args, dut, ports=ports)
