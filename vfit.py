#!/usr/bin/env python3

# VFIT - Variable Font Instancing Tool
# Copyright (c) 2020 Jon Palmisciano

import argparse
import os
import sys

from fontTools import varLib
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._n_a_m_e import NameRecord
from fontTools.varLib.instancer import instantiateVariableFont as instantiateFont

import yaml
from tqdm import tqdm


# Removes spaces from a string.
def sanitize(string):
    return string.replace(" ", "")


# Produces a unique ID for a style.
def getUniqueStyleID(style):
    id = style["name"]
    if "subfamily" in style:
        id = f"{style['subfamily']}-{id}"

    return sanitize(id)


# Loads and validates the config from the given path.
def loadConfig(path):
    config = {}

    # Attempt to read and parse the config file.
    with open(path, "r") as cfg_file:
        try:
            config = yaml.safe_load(cfg_file)
        except yaml.YAMLError as error:
            raise ValueError("malformed YAML")

    # Ensure a metadata block has been provided.
    if "metadata" not in config:
        raise ValueError("no metadata")

    # Ensure a family has been specified.
    if "family" not in config["metadata"]:
        raise ValueError("family must be defined")

    # Verify that at least one style has been provided.
    if "styles" not in config or len(config["styles"]) < 1:
        raise ValueError("no styles")

    # Keep a list of defined styles to make sure there are no duplicates.
    definedStyles = []

    # Validate each style.
    for index, style in enumerate(config["styles"]):
        if "name" not in style:
            raise ValueError(f"unnamed style at index {index}")
        if "axes" not in style:
            raise ValueError(f"no axes for style at index {index}")

        # Ensure this style is not a duplicate of another.
        styleId = getUniqueStyleID(style)
        if styleId in definedStyles:
            raise ValueError(f"duplicate style \"{styleId}\" at index {index}")

        definedStyles.append(styleId)

    return config


# Processes and maps family/style metadata to name table records.
# https://docs.microsoft.com/en-us/typography/opentype/spec/name#name-ids
def mapRecords(metadata, style):
    records = {}

    familyName = metadata["family"]
    styleName = style["name"]

    # Handle subfamilies properly.
    if "subfamily" in style:
        subfamilyName = style["subfamily"]
        familyName += " " + subfamilyName

        # Set the preferred subfamily.
        records[17] = subfamilyName + " " + styleName

    fullName = familyName + " " + styleName

    records[0] = metadata.get("copyright")
    records[1] = familyName
    records[2] = styleName
    records[3] = fullName.replace(" ", "-")
    records[4] = fullName
    records[5] = metadata.get("version")
    records[6] = fullName.replace(" ", "-")
    records[7] = metadata.get("trademark")
    records[8] = metadata.get("manufacturer")
    records[9] = metadata.get("designer")
    records[10] = metadata.get("description")
    records[11] = metadata.get("vendor_url")
    records[12] = metadata.get("designer_url")
    records[13] = metadata.get("license")
    records[14] = metadata.get("license_url")
    records[16] = metadata.get("family")

    return records


# Rewrites the name table with new metadata.
def updateMetadata(font, metadata, style):
    nameTable = font["name"]

    # Clear existing table values.
    nameTable.names = []

    # Add each defined record to the table.
    records = mapRecords(metadata, style)
    for id in records:
        if records[id] is not None:
            nameTable.setName(records[id], id, 1, 0, 0)


# Generates and writes each defined instance.
def generateFonts(config, args):
    metadata = config["metadata"]
    familyName = sanitize(metadata["family"])

    # Create the output path if it doesn't exist.
    if not os.path.exists(args.outputPath):
        os.makedirs(args.outputPath)

    for style in tqdm(config["styles"], ascii=True, leave=False):
        font = TTFont(args.source)

        instantiateFont(font, style["axes"], inplace=True, overlap=True)
        updateMetadata(font, metadata, style)

        styleName = sanitize(style["name"])
        subfamilyName = style.get("subfamily") if "subfamily" in style else ""

        filename = f"{familyName}{sanitize(subfamilyName)}-{styleName}.ttf"
        outputPath = os.path.join(args.outputPath, filename)

        font.save(outputPath)


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser(prog="vfit")
    parser.add_argument("config", help="the metadata/style definition file")
    parser.add_argument("source", help="the font to generate instances of")
    parser.add_argument("-o", dest="outputPath", metavar="path", default=".",
                        help="where to place output files")

    args = parser.parse_args()

    try:
        config = loadConfig(args.config)
    except ValueError as error:
        print(f"error: failed to load configuration ({error})")
        sys.exit(1)

    generateFonts(config, args)


if __name__ == '__main__':
    main()
