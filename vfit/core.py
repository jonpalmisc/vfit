import os

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont as instantiateFont
from tqdm import tqdm

import fontforge

from .util import updateMetadata, makeSelection, getMacStyle, sanitize


# Generates and writes each defined instance.
def generateInstances(config, args):

    # Create the output path if it doesn't exist.
    if not os.path.exists(args.outputPath):
        os.makedirs(args.outputPath)

    tempPaths = []

    for style in tqdm(config, ascii=True, leave=False):
        font = TTFont(args.source)

        instantiateFont(font, style["axes"], inplace=True, overlap=True)
        updateMetadata(font, style)

        familyName = style.get("prefFamily")
        if familyName == None:
            familyName = style.get("family")

        prefSubfamily = style.get("prefSubfamily")
        if prefSubfamily == None:
            prefSubfamily = style.get("subfamily")

        prefSubfamily = prefSubfamily.replace(" ", "")

        subfamilyName = style.get("subfamily")

        # Perform additional table fixups.
        font["head"].macStyle = getMacStyle(subfamilyName)
        font["OS/2"].fsSelection = makeSelection(font["OS/2"].fsSelection,
                                                 subfamilyName)

        weightOverride = style.get("weightOverride")
        if weightOverride != None:
            font["OS/2"].usWeightClass = weightOverride

        widthOverride = style.get("widthOverride")
        if widthOverride != None:
            font["OS/2"].usWidthClass = widthOverride

        ext = args.format if args.format is not None else "ttf"
        filename = f"{familyName}-{prefSubfamily}.{ext}"
        outputPath = os.path.join(args.outputPath, filename)

        if args.bless:
            outputPath += ".tmp"
            tempPaths.append(outputPath)

        font.flavor = args.format
        font.save(outputPath)

    # Bless the font files with FontForge if requested.
    if args.bless:
        for path in tempPaths:
            f = fontforge.open(path)
            f.generate(path.replace(".tmp", ""))

            os.unlink(path)
