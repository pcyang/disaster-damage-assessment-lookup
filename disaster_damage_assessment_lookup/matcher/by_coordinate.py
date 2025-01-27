"""Helper for fetching damage assessment data for the given coordinate."""

import logging
import os
from pathlib import Path
from typing import Dict, Tuple

from geopandas import GeoDataFrame

from disaster_damage_assessment_lookup.matcher.schema.matcher import MatcherConfig

logger = logging.getLogger(__name__)


def match_by_coordinate(
    config: MatcherConfig,
    gdf_databases: Dict[str, GeoDataFrame],
    output_file_path: str,
) -> Tuple[GeoDataFrame, GeoDataFrame]:
    """Helper function for fetching damage assessment data for the given coordinate.

    Args:
        config: Matcher configurations.
        gdf_databases: Database to check.
        output_file_path: base path of the output file path, if saving the result.

    Returns:
        GeoDataFrame with matched data, GeoDataFrame with unmatched data
    """
    logger.info("Running match by coordinate")
    if "max_match_distance_meter" not in config.matcher_data_key_value:
        raise ValueError(
            "max_match_distance_meter must be added in matcher_data_key_value for "
            "matcher_type by_coordinate"
        )
    if "distance_column_name" not in config.matcher_data_key_value:
        raise ValueError(
            "distance_column_name must be added in matcher_data_key_value for "
            "matcher_type by_coordinate"
        )
    if "key_column_name" not in config.matcher_data_key_value:
        raise ValueError(
            "key_column_name must be added in matcher_data_key_value for "
            "matcher_type by_coordinate"
        )

    gdf = gdf_databases[config.source_data]
    gdf = gdf.to_crs(3857)

    postfire_master_data = gdf_databases[config.match_against_data]
    distance_column_name = config.matcher_data_key_value["distance_column_name"]
    max_match_distance_meter = int(
        config.matcher_data_key_value["max_match_distance_meter"]
    )
    key_column_name = config.matcher_data_key_value["key_column_name"]

    coordinate_matching_result = gdf.sjoin_nearest(
        postfire_master_data,
        max_distance=max_match_distance_meter,
        distance_col=distance_column_name,
        rsuffix=config.column_suffix.right,
        lsuffix=config.column_suffix.left,
    )

    coordinate_matching_unmatched_result = gdf[
        ~gdf[key_column_name].isin(coordinate_matching_result[key_column_name])
    ]

    logger.info(
        f"{len(coordinate_matching_result)} of {len(gdf)} records matched "
        f"by coordinate within {max_match_distance_meter} meter away."
    )
    if config.save_file is not None:
        Path(output_file_path).mkdir(parents=True, exist_ok=True)
        save_file_path = os.path.join(output_file_path, config.save_file.file_name)
        coordinate_matching_result.to_excel(
            save_file_path,
            sheet_name=config.save_file.sheet_name,
            index=config.save_file.include_index,
            columns=config.save_file.columns,
        )
    return coordinate_matching_result, coordinate_matching_unmatched_result
