# Removes spaces from a string.
def sanitize(string):
    return string.replace(" ", "")


# Produces a unique ID for a style.
def getUniqueStyleID(style):
    id = style["name"]
    if "subfamily" in style:
        id = f"{style['subfamily']}-{id}"

    return sanitize(id)


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
