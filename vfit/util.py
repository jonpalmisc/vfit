PLAT_MAC = 1
PLAT_WINDOWS = 3

ENC_ROMAN = 0
ENC_UNICODE_11 = 1

LANG_ENGLISH = 1033

MACSTYLE = {'Regular': 0, 'Bold': 1, 'Italic': 2, 'Bold Italic': 3}

OVERLAP_SIMPLE = 0x40
OVERLAP_COMPOUND = 0x0400


# Removes spaces from a string.
def sanitize(string):
    return string.replace(" ", "")


# Produces a unique ID for a style.
def getUniqueStyleID(style):
    id = style["name"]
    if "subfamily" in style:
        id = f"{style['subfamily']}-{id}"

    return sanitize(id)


def getFullName(style):
    familyName = style.get("prefFamily")
    if familyName == None:
        familyName = style.get("family")

    subfamilyName = style.get("prefSubfamily")
    if subfamilyName == None:
        subfamilyName = style.get("subfamily")

    return f"{familyName} {subfamilyName}"


def getPostscriptName(style):
    familyName = style.get("prefFamily")
    if familyName == None:
        familyName = style.get("family")

    subfamilyName = style.get("prefSubfamily")
    if subfamilyName == None:
        subfamilyName = style.get("subfamily")

    familyName = familyName.replace(" ", "")
    subfamilyName = subfamilyName.replace(" ", "")

    return f"{familyName}-{subfamilyName}"


# Rewrites the name table with new metadata.
def updateNames(font, style):
    nameTable = font["name"]

    nameTable.names = []

    family = style.get("family")
    subfamily = style.get("subfamily")
    prefFamily = style.get("prefFamily")
    prefSubfamily = style.get("prefSubfamily")

    fullName = getFullName(style)
    postscriptName = getPostscriptName(style)

    nameTable.setName(family, 1, PLAT_MAC, ENC_ROMAN, 0)
    nameTable.setName(family, 1, PLAT_WINDOWS, ENC_UNICODE_11, LANG_ENGLISH)

    nameTable.setName(subfamily, 2, PLAT_MAC, ENC_ROMAN, 0)
    nameTable.setName(subfamily, 2, PLAT_WINDOWS, ENC_UNICODE_11, LANG_ENGLISH)

    nameTable.setName(fullName, 3, PLAT_MAC, ENC_ROMAN, 0)
    nameTable.setName(fullName, 3, PLAT_WINDOWS, ENC_UNICODE_11, LANG_ENGLISH)

    nameTable.setName(fullName, 4, PLAT_MAC, ENC_ROMAN, 0)
    nameTable.setName(fullName, 4, PLAT_WINDOWS, ENC_UNICODE_11, LANG_ENGLISH)

    nameTable.setName("Version 1.000", 5, PLAT_MAC, ENC_ROMAN, 0)
    nameTable.setName("Version 1.000", 5, PLAT_WINDOWS, ENC_UNICODE_11,
                      LANG_ENGLISH)

    nameTable.setName(postscriptName, 6, PLAT_MAC, ENC_ROMAN, 0)
    nameTable.setName(postscriptName, 6, PLAT_WINDOWS, ENC_UNICODE_11,
                      LANG_ENGLISH)

    if prefFamily is not None:
        nameTable.setName(prefFamily, 16, PLAT_WINDOWS, ENC_UNICODE_11,
                          LANG_ENGLISH)

    if prefSubfamily is not None:
        nameTable.setName(prefSubfamily, 17, PLAT_WINDOWS, ENC_UNICODE_11,
                          LANG_ENGLISH)


def makeSelection(bits, style):
    bits = bits ^ bits

    if style == 'Regular':
        bits |= 0b1000000
    else:
        bits &= ~0b1000000

    if style == 'Bold' or style == 'BoldItalic':
        bits |= 0b100000
    else:
        bits &= ~0b100000

    if style == 'Italic':
        bits |= 0b1
    else:
        bits &= ~0b1

    if not bits:
        bits = 0b1000000

    return bits


def getMacStyle(style):
    return MACSTYLE[style]


def dropVariationTables(font):
    for tag in 'STAT cvar fvar gvar'.split():
        if tag in font.keys():
            del font[tag]


def setOverlapFlags(font):
    glyf = font["glyf"]
    for glyph_name in glyf.keys():
        glyph = glyf[glyph_name]

        if glyph.isComposite():
            glyph.components[0].flags |= OVERLAP_COMPOUND
        elif glyph.numberOfContours > 0:
            glyph.flags[0] |= OVERLAP_SIMPLE
