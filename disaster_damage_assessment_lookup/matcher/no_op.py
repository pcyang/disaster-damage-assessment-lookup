"""No-op matcher that can use to save the same DataFrame in a different column view."""

import os
from pathlib import Path
from typing import Dict

from geopandas import GeoDataFrame

from disaster_damage_assessment_lookup.matcher.schema.matcher import MatcherConfig


def no_op_matcher(
    config: MatcherConfig,
    gdf_databases: Dict[str, GeoDataFrame],
    output_file_path: str,
) -> GeoDataFrame:
    """No-op matcher that can use to save the same DataFrame in a different column view.

    Args:
        config: Matcher configurations.
        gdf_databases: Database to check.
        output_file_path: base path of the output file path, if saving the result.

    Returns:
        source_data with fire perimeter information columns appended.
    """
    gdf = gdf_databases[config.source_data]
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
