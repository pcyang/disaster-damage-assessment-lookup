"""Utility to load himl config."""

import os
from collections import OrderedDict
from typing import Any

import yaml
from himl import ConfigProcessor
from himl.config_merger import Loader


def load_himl_config(print_result: bool = False) -> Any:
    """Load configuration using himl.

    ---
    Parameters:
        print_result: Print the loaded configuration. Default is False.

    Returns: JSON object for the loaded configuration.

    """
    config_processor = ConfigProcessor()
    path = "config/"
    filters = ()  # can choose to output only specific keys
    exclude_keys = ()  # can choose to remove specific keys
    output_format = "yaml"  # yaml/json

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"""Configuration file default.yaml is missing, create a configuration file at {path}"""
        )

    # load the !include tag
    Loader.add_constructor("!include", Loader.include)

    # override the Yaml SafeLoader with our custom loader
    yaml.SafeLoader = Loader

    result = config_processor.process(
        path=path,
        filters=filters,
        exclude_keys=exclude_keys,
        output_format=output_format,
        print_data=False,
    )
    if print_result:
        yaml.add_representer(
            OrderedDict,
            lambda dumper, data: dumper.represent_mapping(
                "tag:yaml.org,2002:map", data.items()
            ),
        )
        yaml.add_representer(
            tuple,
            lambda dumper, data: dumper.represent_sequence(
                "tag:yaml.org,2002:seq", data
            ),
        )
    return result
