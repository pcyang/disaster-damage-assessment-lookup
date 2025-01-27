"""Schema definition for the data loader components."""

from dataclasses import field
from typing import Dict, Optional

from marshmallow_dataclass import dataclass

from disaster_damage_assessment_lookup.data_loader.schema.excel import (
    ExcelGeoDataFrameConfig,
    ExcelGeoDataFrameLoaderConfig,
)
from disaster_damage_assessment_lookup.data_loader.schema.geojson import (
    GeoJSONGeoDataFrameConfig,
)


@dataclass
class DataLoaderConfig:
    """Configuration for the Data Loader component."""

    input_file_path: Optional[str] = "input_data"
    """Base file path to look for all input files."""

    output_file_path: Optional[str] = "output_data"
    """Base file path to save all output files."""

    geodataframe_loader: Optional[ExcelGeoDataFrameLoaderConfig] = None
    """Configuration for the GeoDataFrame Loader."""

    excel: Optional[Dict[str, ExcelGeoDataFrameConfig]] = field(default_factory=dict)
    """Dictionary of configuration for creating GeoDataFrame from Excel File. 
    Key is the label for the given Excel File, value is the configuration."""

    geojson: Optional[Dict[str, GeoJSONGeoDataFrameConfig]] = field(
        default_factory=dict
    )
    """Dictionary of configuration for creating GeoDataFrame from geojson File. 
    Key is the label for the given geojson File, value is the configuration."""
