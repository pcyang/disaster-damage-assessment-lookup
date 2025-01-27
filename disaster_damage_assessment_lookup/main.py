"""Disaster Damage assessment lookup helper script."""

import logging

from dotenv import load_dotenv

from disaster_damage_assessment_lookup.data_loader.data_loader import DataLoader
from disaster_damage_assessment_lookup.data_loader.schema.data_loader import (
    DataLoaderConfig,
)
from disaster_damage_assessment_lookup.matcher.matcher import Matcher
from disaster_damage_assessment_lookup.matcher.schema.matcher import (
    MatcherConfigWrapper,
)
from disaster_damage_assessment_lookup.utils.config_loader import load_himl_config

logger = logging.getLogger(__name__)


def main():
    """Entry point for the disaster damage lookup helper script."""
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    logger.info("Running Disaster Damage Assessment Lookup")
    load_dotenv()
    config = load_himl_config(print_result=False)
    logger.info("Loaded configuration")

    # pylint: disable=E1101 # Suppress no member error for dynamic member
    data_loader = DataLoader(
        config=DataLoaderConfig.Schema().load(config["data_loader"])
    )
    logger.info("Initialized Data Loader")

    gdf_databases = data_loader.load()
    logger.info("Loaded databases")

    # pylint: disable=E1101 # Suppress no member error for dynamic member
    matcher = Matcher(
        config=MatcherConfigWrapper.Schema().load({"matcher": config["matcher"]})
    )

    logger.info("Running matchers")
    matcher.run(
        gdf_databases=gdf_databases,
        output_file_path=config["output_data_path"],
    )


main()
