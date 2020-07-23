import os

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont as instantiateFont
from tqdm import tqdm

from .util import updateMetadata, sanitize


# Generates and writes each defined instance.
def generateInstances(config, args):
    metadata = config["metadata"]
    familyName = sanitize(metadata["family"])

    outputDir = os.path.join(args.outputPath, familyName)

    # Create the output path if it doesn't exist.
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    for style in tqdm(config["styles"], ascii=True, leave=False):
        font = TTFont(args.source)

        instantiateFont(font, style["axes"], inplace=True, overlap=True)
        updateMetadata(font, metadata, style)

        styleName = sanitize(style["name"])
        subfamilyName = style.get("subfamily") if "subfamily" in style else ""

        filename = f"{familyName}{sanitize(subfamilyName)}-{styleName}.ttf"
        outputPath = os.path.join(outputDir, filename)

        font.save(outputPath)
