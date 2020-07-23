#!/usr/bin/env python3

# VFIT - Variable Font Instancing Tool
# Copyright (c) 2020 Jon Palmisciano

import argparse
import sys

from . import config
from . import core


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser(prog="vfit")
    parser.add_argument("config", help="the metadata/style definition file")
    parser.add_argument("source", help="the font to generate instances of")
    parser.add_argument("-o", dest="outputPath", metavar="path", default=".",
                        help="where to place output files")

    args = parser.parse_args()

    try:
        cfg = config.load(args.config)
    except ValueError as error:
        print(f"error: failed to load configuration ({error})")
        sys.exit(1)

    core.generateInstances(cfg, args)