import json


# Loads and validates the config from the given path.
def load(path):
    config = {}

    # Attempt to read and parse the config file.
    with open(path, "r") as cfg_file:
        config = json.load(cfg_file)

    # Regular subfamily should be the default if subfamily is not specified.
    for style in config:
        if style.get("subfamily") is None:
            style["subfamily"] = "Regular"

    return config
