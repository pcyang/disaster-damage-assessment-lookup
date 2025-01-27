"""Helper for checking if a given coordinate is within a fire perimeter."""

import logging
import os
from pathlib import Path
from typing import Dict

import geopandas as gpd
import numpy as np
from geopandas import GeoDataFrame

from disaster_damage_assessment_lookup.matcher.schema.matcher import MatcherConfig

logger = logging.getLogger(__name__)


def match_by_fire_perimeters(
    config: MatcherConfig,
    gdf_databases: Dict[str, GeoDataFrame],
    output_file_path: str,
) -> GeoDataFrame:
    """Helper function for checking if a given coordinate is within a fire perimeter

    Args:
        config: Matcher configurations.
        gdf_databases: Database to check.
        output_file_path: base path of the output file path, if saving the result.

    Returns:
        source_data with fire perimeter information columns appended.
    """
    logger.info("Running match by fire perimeters")
    perimeters = {}
    fire_perimeter_database = gdf_databases[config.match_against_data]
    fire_perimeter_database = fire_perimeter_database.to_crs(3857)

    if "incident_name" not in config.matcher_data_key_list:
        raise ValueError(
            "incident_name must be added in matcher_data_key_list "
            "with at least one incident_name for "
            "matcher_type by_fire_perimeters"
        )
    if "max_distance_from_perimeter_meter" not in config.matcher_data_key_value:
        raise ValueError(
            "max_distance_from_perimeter_meter must be added in matcher_data_key_value for "
            "matcher_type by_fire_perimeters"
        )

    for incident_name in config.matcher_data_key_list["incident_name"]:
        fire_perimeter = fire_perimeter_database.loc[
            (fire_perimeter_database["poly_IncidentName"] == incident_name)
        ]
        perimeters[incident_name] = fire_perimeter

    logger.info(
        f"Loaded fire perimeters: {config.matcher_data_key_list['incident_name']}"
    )

    # Check inside of perimeter
    # Assuming that no perimeters overlaps
    gdf = gdf_databases[config.source_data]
    gdf = gdf.to_crs(3857)
    within_fire_perimeter = {}
    total_data_count = len(gdf)
    distance_from_fire_perimeter_column_label = "Distance from Fire Perimeter"
    fire_perimeter_column_label = "Fire Perimeter"
    gdf[distance_from_fire_perimeter_column_label] = ""
    gdf[fire_perimeter_column_label] = ""
    for label, perimeter in perimeters.items():
        points_in_perimeter = gpd.sjoin(perimeter, gdf, predicate="contains")
        gdf[fire_perimeter_column_label] = np.where(
            gdf["Intake #"].isin(points_in_perimeter["Intake #"]),
            label,
            gdf[fire_perimeter_column_label],
        )
        gdf[distance_from_fire_perimeter_column_label] = np.where(
            gdf["Intake #"].isin(points_in_perimeter["Intake #"]),
            "Inside",
            gdf[distance_from_fire_perimeter_column_label],
        )

        logger.info(
            f"{len(points_in_perimeter)} of {total_data_count} entries "
            f"inside of fire perimeter {label}"
        )
        within_fire_perimeter[label] = points_in_perimeter

    # Check within n meter from the perimeter
    within_n_meter_from_fire_perimeter = {}
    n = config.matcher_data_key_value["max_distance_from_perimeter_meter"]
    for label, perimeter in perimeters.items():
        points_not_perimeters = gdf[
            ~gdf["Intake #"].isin(within_fire_perimeter[label]["Intake #"])
        ]

        points_close_to_perimeter = gpd.sjoin(
            perimeter,
            points_not_perimeters,
            predicate="dwithin",
            distance=n,
        )
        gdf[fire_perimeter_column_label] = np.where(
            gdf["Intake #"].isin(points_close_to_perimeter["Intake #"]),
            label,
            gdf[fire_perimeter_column_label],
        )
        gdf[distance_from_fire_perimeter_column_label] = np.where(
            gdf["Intake #"].isin(points_close_to_perimeter["Intake #"]),
            f"<{n} m",
            gdf[distance_from_fire_perimeter_column_label],
        )

        logger.info(
            f"{len(points_close_to_perimeter)} of {total_data_count} entries "
            f"within {n} meters "
            f"from the fire perimeter {label}"
        )
        within_n_meter_from_fire_perimeter[label] = points_close_to_perimeter

    # Remaining are outside of the perimeter
    logger.info(
        f"{len(gdf[gdf[fire_perimeter_column_label] == ''])} of {total_data_count} entries "
        f"more than {n} meters "
        f"from the fire perimeters"
    )

    gdf[distance_from_fire_perimeter_column_label] = np.where(
        gdf[fire_perimeter_column_label] == "",
        f">{n}m  ",
        gdf[distance_from_fire_perimeter_column_label],
    )
    if config.save_file is not None:
        Path(output_file_path).mkdir(parents=True, exist_ok=True)
        save_file_path = os.path.join(output_file_path, config.save_file.file_name)
        gdf.to_excel(
            save_file_path,
            sheet_name=config.save_file.sheet_name,
            index=config.save_file.include_index,
            columns=config.save_file.columns,
        )

    return gdf
