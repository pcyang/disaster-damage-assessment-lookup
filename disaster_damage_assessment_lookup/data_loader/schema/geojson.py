"""Schema definition for the geojson data loader components."""

from typing import List, Optional

from marshmallow_dataclass import dataclass


@dataclass
class GeoJSONGeoDataFrameConfig:
    """GeoJSON data loader configuration."""

    file_name: str
    """File name for the geojson to load and convert to GeoDataFrame."""

    label: str
    """Label for the output GeoDataFrame. Will be use as a reference from other parts of the Himl
    configuration, as well as for creating cache file for this GeoDataFrame."""

    columns: Optional[List[str]] = None
    """Columns to select from the GeoJSON to output to GeoDataFrame."""
