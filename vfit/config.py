import yaml

from .util import getUniqueStyleID


# Loads and validates the config from the given path.
def load(path):
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
