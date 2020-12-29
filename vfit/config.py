import json

from .util import getUniqueStyleID


# Loads and validates the config from the given path.
def load(path):
    config = {}

    # Attempt to read and parse the config file.
    with open(path, "r") as cfg_file:
        config = json.load(cfg_file)

    for style in config:
        if style.get("subfamily") is None:
            style["subfamily"] = "Regular"

    return config
