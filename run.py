#!/usr/bin/python

import argparse
import construct
from plat import BB
from nmigen.hdl.ir import Fragment
from nmigen.back import pysim, rtlil, verilog


from boneless.arch.asm import Assembler
import array
import intelhex
from sim import Simulator
from utils.serial_write import writer
import firmware

from firmware.loader import convert, load, char_convert
from firmware.registers import MetaSub

import sim_data

def show_firmware():
    fw_list = firmware.show()
    for i, j in enumerate(fw_list):
        print(i, " : ", j)

def check_firmware(name):
    " returns true if firmware does NOT exist"
    if name not in firmware.available:
        print("Firmware does not exist")
        show_firmware()
        return True
    return False 

if __name__ == "__main__":
    print("Gizmotronic Boneless")
    p = argparse.ArgumentParser()
    action = p.add_subparsers(dest="action")

    action.add_parser("info")

    action.add_parser("list")

    action.add_parser("build")

    action.add_parser("program")

    action.add_parser("simulate")

    action.add_parser("gatesim")

    p.add_argument("-f", action="store", help="asm file to include", default=None)

    p.add_argument(
        "-p",
        action="store",
        help="firmware to run , use list to show",
        default="uLoader",
    )

    p.add_argument(
        "-l", action="store", help="firmware to load in the sim", default=None
    )

    args = p.parse_args()

    platform = BB()
    if args.action == "list":
        show_firmware()

    if args.action == "info":
        print("Show info")
        if check_firmware(args.p): raise 
        cpu = construct.CPU(platform, fw=args.p, asm_file=args.f)
        cpu.b.fw.show()
        print("Length" , len(cpu.b.code))

    if args.action == "build":
        print("Build")
        if check_firmware(args.p): raise 
        cpu = construct.CPU(platform, fw=args.p, asm_file=args.f)
        platform.build(cpu, do_program=True)

    if args.action == "program":
        print("Program")
        if check_firmware(args.p): raise 
        cpu = construct.CPU(platform, fw=args.p, asm_file=args.f)
        io_map = cpu.b.io_map
        load_ware = firmware.available[args.p](io_map)
        #print(load_ware.code())
        fw = load_ware.assemble()
        print(fw)
        print("Length ",len(fw))
        data = char_convert(fw)
        #print(data)
        load(data)

    if args.action == "simulate":
        print("Simulate")
        if check_firmware(args.p): raise 
        s = Simulator(fw=args.p,asm_file=args.f)
        s.run()

    if args.action == "gatesim":
        print("Gateware Simulation")
        if check_firmware(args.p): raise 
        design = construct.simCPU(platform, fw=args.p, asm_file=args.f)
        fragment = Fragment.get(design, platform)
        f = open("test.vcd", "w")
        dut = design.b.serial_port
        data = []
        if args.l is None:
            st = "the quick brown fox jumps over the lazy dog"
            data = sim_data.str_data(st)
        else:
            # clean the meta sub
            for i in MetaSub.subroutines:
                print(i.__class__, i._called)
                i._called = False
            print(args.l)
            io_map = design.b.io_map
            load_ware = firmware.available[args.l](io_map)
            print(load_ware.code())
            for i in MetaSub.subroutines:
                print(i.__class__, i._called)
            fw = load_ware.assemble()
            data = convert(fw)
        print("data to load ", data)

        with pysim.Simulator(fragment, vcd_file=f, traces=()) as sim:
            sim.add_clock(100e-6)
            sim.add_sync_process(sim_data.test_rx(data, dut))
            sim.run_until(100e-6 * 300000, run_passive=True)
