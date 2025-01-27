"""Helper for loading all of the data needed to fetch the damage assessment information."""

import logging
import os
from typing import Dict

import geopandas as gpd
from geopandas import GeoDataFrame

from disaster_damage_assessment_lookup.data_loader.excel import ExcelGeoDataFrameLoader
from disaster_damage_assessment_lookup.data_loader.schema.data_loader import (
    DataLoaderConfig,
)

logger = logging.getLogger(__name__)


class DataLoader:
    """Helper class for loading all of the data needed to fetch the
    damage assessment information."""

    def __init__(self, config: DataLoaderConfig):
        self.config = config

    def load(self) -> Dict[str, GeoDataFrame]:
        """Load all of the data needed to fetch the damage assessment information.

        Returns:
            Dictionary of a string label as key and GeoDataFrame as value.
        """
        result = {}
        excel_geodataframe_loader = None
        if self.config.geodataframe_loader:
            excel_geodataframe_loader = ExcelGeoDataFrameLoader(
                self.config.geodataframe_loader
            )
            logger.info("Initialized ExcelGeoDataFrameLoader")

        if not excel_geodataframe_loader and self.config.excel:
            raise ValueError(
                "geodataframe_loader must be configured in default.yaml in "
                "order to import excel file into GeoDataFrame!"
            )

        if self.config.excel:
            for label, gdf_config in self.config.excel.items():
                logger.info(
                    f"Loading Excel Files {gdf_config.file_name} into GeoDataFrame"
                )
                if label in result:
                    raise ValueError(
                        f"Conflicting label '{label}' "
                        "found when trying to load GeoDataFrame during the DataLoader step"
                    )

                gdf = excel_geodataframe_loader.load(
                    config=gdf_config,
                    input_file_path=self.config.input_file_path,
                    output_file_path=self.config.output_file_path,
                )
                if gdf is not None:
                    logger.info(
                        f"Successfully loaded Excel Files {gdf_config.file_name} into GeoDataFrame"
                    )
                    result[label] = gdf
        if self.config.geojson:
            for label, gdf_config in self.config.geojson.items():
                file_name = os.path.join(
                    self.config.input_file_path, gdf_config.file_name
                )
                logger.info(f"Loading geojson Files {file_name} into GeoDataFrame")
                if label in result:
                    raise ValueError(
                        f"Conflicting label '{label}' "
                        "found when trying to load GeoDataFrame during the DataLoader step"
                    )
                gdf = gpd.read_file(filename=file_name, columns=gdf_config.columns)
                if gdf is not None:
                    logger.info(
                        f"Successfully loaded geojson Files {file_name} into GeoDataFrame"
                    )
                    result[label] = gdf

        return result
