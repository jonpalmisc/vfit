import os

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont as instantiateFont
from tqdm import tqdm

import fontforge

from .util import updateNames, makeSelection, getMacStyle, sanitize


# Generates and writes each defined instance.
def generateInstances(config, args):

    # Create the output path if it doesn't exist.
    if not os.path.exists(args.outputPath):
        os.makedirs(args.outputPath)

    tempPaths = []

    for style in tqdm(config, ascii=True, leave=False):
        font = TTFont(args.source)

        # Instantiate the font and update the name table.
        instantiateFont(font, style["axes"], inplace=True, overlap=True)
        updateNames(font, style)

        family = style.get("prefFamily")
        if family == None:
            family = style.get("family")

        subfamily = style.get("subfamily")
        prefSubfamily = style.get("prefSubfamily")
        if prefSubfamily == None:
            prefSubfamily = subfamily

        prefSubfamily = prefSubfamily.replace(" ", "")

        # Perform additional table fixups.
        font["head"].macStyle = getMacStyle(subfamily)
        font["OS/2"].fsSelection = makeSelection(font["OS/2"].fsSelection,
                                                 subfamily)

        # Override weight if requested.
        weightOverride = style.get("weightOverride")
        if weightOverride != None:
            font["OS/2"].usWeightClass = weightOverride

        # Override width if requested.
        widthOverride = style.get("widthOverride")
        if widthOverride != None:
            font["OS/2"].usWidthClass = widthOverride

        ext = args.format if args.format is not None else "ttf"
        filename = f"{family}-{prefSubfamily}.{ext}"
        outputPath = os.path.join(args.outputPath, filename)

        # Adjust the output path and add it to the list if blessing is enabled.
        if args.bless:
            outputPath += ".tmp"
            tempPaths.append(outputPath)

        font.flavor = args.format
        font.save(outputPath)

    # Bless the font files with FontForge if requested.
    if args.bless:

        # Opening and saving files with FontForge fixes them somehow.
        for path in tempPaths:
            f = fontforge.open(path)
            f.generate(path.replace(".tmp", ""))

            os.unlink(path)
