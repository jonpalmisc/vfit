#!/usr/bin/env python3

# VFIT - Variable Font Instancing Tool
# Copyright (c) 2020 Jon Palmisciano

import argparse
import json
import sys

from . import core


# Loads and validates the config from the given path.
def loadConfig(path):
    config = {}

    # Attempt to read and parse the config file.
    with open(path, "r") as cfg_file:
        config = json.load(cfg_file)

    # Regular subfamily should be the default if subfamily is not specified.
    for style in config:
        if style.get("subfamily") is None:
            style["subfamily"] = "Regular"

    return config


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser(
        prog="vfit",
        description=
        "Generate backwards-compatible, static instances of variable fonts.")

    parser.add_argument("config", help="the metadata/style definition file")
    parser.add_argument("source", help="the font to generate instances of")

    parser.add_argument("-o",
                        dest="outputPath",
                        metavar="PATH",
                        default=".",
                        help="where to place output files")

    parser.add_argument("-f",
                        dest="format",
                        default=None,
                        choices=["woff", "woff2"],
                        help="which format to output as")

    parser.add_argument("-C",
                        dest="fixContour",
                        action="store_true",
                        help="fix contours for macOS (side effects unknown)")

    args = parser.parse_args()

    try:
        cfg = loadConfig(args.config)
    except ValueError as error:
        print(f"error: failed to load config, check your JSON\n{error}")
        sys.exit(1)

    core.generateInstances(cfg, args)
