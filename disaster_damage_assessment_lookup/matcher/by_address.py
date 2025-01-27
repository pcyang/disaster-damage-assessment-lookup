"""Helper for fetching damage assessment data for the given address."""

import logging
import os
from pathlib import Path
from typing import Dict, Tuple

from geopandas import GeoDataFrame

from disaster_damage_assessment_lookup.matcher.schema.matcher import MatcherConfig

logger = logging.getLogger(__name__)


def match_by_address(
    config: MatcherConfig,
    gdf_databases: Dict[str, GeoDataFrame],
    output_file_path: str,
) -> Tuple[GeoDataFrame, GeoDataFrame]:
    """Helper function for fetching damage assessment data for the given address.

    Args:
        config: Matcher configurations.
        gdf_databases: Database to check.
        output_file_path: base path of the output file path, if saving the result.

    Returns:
        GeoDataFrame with matched data, GeoDataFrame with unmatched data
    """
    logger.info("Running match by address")
    if "on_column_name" not in config.matcher_data_key_value:
        raise ValueError(
            "on_column_name must be added in matcher_data_key_value for "
            "matcher_type by_address"
        )

    on_column_name = config.matcher_data_key_value["on_column_name"]
    gdf = gdf_databases[config.source_data]
    gdf = gdf.to_crs(3857)
    gdf.dropna(subset=["geometry"], inplace=True)
    gdf.dropna(subset=[on_column_name], inplace=True)

    postfire_master_data = gdf_databases[config.match_against_data]
    address_matching_result = gdf.merge(
        postfire_master_data,
        on=on_column_name,
        how="inner",
        suffixes=(config.column_suffix.left, config.column_suffix.right),
    )
    unique_address_matched = address_matching_result.drop_duplicates(
        subset=[on_column_name]
    )
    address_matching_unmatched_result = gdf[
        ~gdf[on_column_name].isin(unique_address_matched[on_column_name])
    ]

    logger.info(
        f"{len(unique_address_matched)} of {len(gdf)} records matched by address. "
        f"Total of {len(address_matching_result)} including duplicates."
    )

    if config.save_file is not None:
        Path(output_file_path).mkdir(parents=True, exist_ok=True)
        save_file_path = os.path.join(output_file_path, config.save_file.file_name)
        address_matching_result.to_excel(
            save_file_path,
            sheet_name=config.save_file.sheet_name,
            index=config.save_file.include_index,
            columns=config.save_file.columns,
        )
    return address_matching_result, address_matching_unmatched_result
