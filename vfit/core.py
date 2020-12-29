import os

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont as instantiateFont
from tqdm import tqdm

from .util import updateMetadata, makeSelection, getMacStyle, sanitize


# Generates and writes each defined instance.
def generateInstances(config, args):

    # Create the output path if it doesn't exist.
    if not os.path.exists(args.outputPath):
        os.makedirs(args.outputPath)

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

        subfamilyName = style.get("subfamily")

        font["OS/2"].fsSelection = makeSelection(font["OS/2"].fsSelection,
                                                 subfamilyName)

        font["head"].macStyle = getMacStyle(subfamilyName)

        ext = args.format if args.format is not None else "ttf"
        filename = f"{familyName}-{prefSubfamily}.{ext}"
        outputPath = os.path.join(args.outputPath, filename)

        font.flavor = args.format
        font.save(outputPath)
