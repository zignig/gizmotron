#!/usr/bin/python

import argparse
import construct
from plat import BB

if __name__ == "__main__":
    print("Gizmotronic Boneless")
    p = argparse.ArgumentParser()
    action = p.add_subparsers(dest="action")

    action.add_parser("info")

    action.add_parser("build")

    action.add_parser("program")

    args = p.parse_args()

    if args.action == "info":
        print("Show info")
        platform = BB()
        cpu = construct.CPU(platform)

    if args.action == "build":
        print("Build")
        platform = BB()
        cpu = construct.CPU(platform)
        platform.build(cpu, do_program=True)
    if args.action == "program":
        print("Program")
