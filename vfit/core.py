import os

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont as instantiateFont
from tqdm import tqdm

from .util import updateNames, makeSelection, getPostscriptName, getMacStyle, sanitize, dropVariationTables, setOverlapFlags


# Generates and writes each defined instance.
def generateInstances(config, args):

    # Create the output path if it doesn't exist.
    if not os.path.exists(args.outputPath):
        os.makedirs(args.outputPath)

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

        dropVariationTables(font)

        # Fix contour overlap issues on macOS.
        if args.fixContour == True:
            setOverlapFlags(font)

        ext = args.format if args.format is not None else "ttf"
        filename = getPostscriptName(style) + f".{ext}"
        outputPath = os.path.join(args.outputPath, filename)

        font.flavor = args.format
        font.save(outputPath)
