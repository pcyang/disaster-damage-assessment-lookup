"""Helper for running matcher to look up the damage assessment data."""

import logging
from typing import Dict

from geopandas import GeoDataFrame

from disaster_damage_assessment_lookup.matcher.by_address import match_by_address
from disaster_damage_assessment_lookup.matcher.by_coordinate import match_by_coordinate
from disaster_damage_assessment_lookup.matcher.by_fire_perimeter import (
    match_by_fire_perimeters,
)
from disaster_damage_assessment_lookup.matcher.no_op import no_op_matcher
from disaster_damage_assessment_lookup.matcher.schema.matcher import (
    MatcherConfigWrapper,
)

logger = logging.getLogger(__name__)


class Matcher:
    """Helper class for running matcher to look up the damage assessment data."""

    def __init__(self, config: MatcherConfigWrapper):
        self.config = config

    def run(
        self,
        gdf_databases: Dict[str, GeoDataFrame],
        output_file_path: str,
    ) -> None:
        """Run the matchers and output the results to file."""

        for matcher in self.config.matcher.values():
            if matcher.matcher_type == "by_fire_perimeters":
                result = match_by_fire_perimeters(
                    config=matcher,
                    gdf_databases=gdf_databases,
                    output_file_path=output_file_path,
                )
                gdf_databases[matcher.label] = result
                gdf_databases[matcher.unmatched_label] = result
            elif matcher.matcher_type == "by_address":
                matched_result, unmatched_result = match_by_address(
                    config=matcher,
                    gdf_databases=gdf_databases,
                    output_file_path=output_file_path,
                )
                gdf_databases[matcher.label] = matched_result
                gdf_databases[matcher.unmatched_label] = unmatched_result
            elif matcher.matcher_type == "by_coordinate":
                matched_result, unmatched_result = match_by_coordinate(
                    config=matcher,
                    gdf_databases=gdf_databases,
                    output_file_path=output_file_path,
                )
                gdf_databases[matcher.label] = matched_result
                gdf_databases[matcher.unmatched_label] = unmatched_result
            elif matcher.matcher_type == "no_op":
                no_op_result = no_op_matcher(
                    config=matcher,
                    gdf_databases=gdf_databases,
                    output_file_path=output_file_path,
                )
                gdf_databases[matcher.label] = no_op_result
                gdf_databases[matcher.unmatched_label] = no_op_result
