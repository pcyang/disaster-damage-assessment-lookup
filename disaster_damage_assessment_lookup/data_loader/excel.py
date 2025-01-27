"""Helper for loading Excel file into GeoDataFrame using GoogleV3 API"""

import json
import logging
import os
from pathlib import Path
from typing import List

import geopandas as gpd
import numpy
import pandas as pd
from geopandas import GeoDataFrame
from geopy.exc import GeopyError
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import GoogleV3
from pandas import DataFrame
from unidecode import unidecode

from disaster_damage_assessment_lookup.data_loader.schema.excel import (
    AddressFormattingConfig,
    ExcelGeoDataFrameConfig,
    ExcelGeoDataFrameLoaderConfig,
    PostProcessingConfig,
    PreProcessingStepConfig,
)

logger = logging.getLogger(__name__)

# column for caching result from the geocode request
GEOCODE_COLUMN_NAME = "_geocode"

# columns to reference for converting pandas dataframe to geopandas dataframe
LATITUDE_COLUMN_NAME = "_latitude"
LONGITUDE_COLUMN_NAME = "_longitude"

# Normalized address to match against the DINS database
SITEADDRESS_COLUMN_NAME = "SITEADDRESS"


def get_cache_name(file_label: str):
    """Returns the name of the file for the given file_label."""
    return f"{file_label}_cache.xlsx"


def label_location(row, geocode, address_column_name):
    """Dataframe apply function for making request to GoogleV3 API using Geopy
    and fetch the geocode information for the given address.
    """
    if pd.isnull(row[GEOCODE_COLUMN_NAME]) and row[address_column_name] != "Na ":
        try:
            logger.debug(f"Running geocode for address '{row[address_column_name]}'")
            code = geocode(row[address_column_name])
        except GeopyError as e:
            logger.error(
                "Exception occurred while querying geocode for address: "
                f"{row[address_column_name]}, e: {e}"
            )
        if code:
            return json.dumps(code.raw)
    return row[GEOCODE_COLUMN_NAME]


def label_latitude(row):
    """Dataframe apply function for labeling latitude column with geocode data
    loaded from geocoding API request made to GoogleV3 API.
    """
    if not pd.isnull(row[GEOCODE_COLUMN_NAME]) and pd.isnull(row[LATITUDE_COLUMN_NAME]):
        return json.loads(row[GEOCODE_COLUMN_NAME])["geometry"]["location"]["lat"]
    return row[LATITUDE_COLUMN_NAME]


def label_longitude(row):
    """Dataframe apply function for labeling longitude column with geocode data
    loaded from geocoding API request made to GoogleV3 API.
    """
    if not pd.isnull(row[GEOCODE_COLUMN_NAME]) and pd.isnull(
        row[LONGITUDE_COLUMN_NAME]
    ):
        return json.loads(row[GEOCODE_COLUMN_NAME])["geometry"]["location"]["lng"]
    return row[LONGITUDE_COLUMN_NAME]


def label_siteaddress(row, config: AddressFormattingConfig):
    """Dataframe apply function for labeling SITEADDRESS column with address
    loaded from geocoding API request made to GoogleV3 API.
    """
    if not pd.isnull(row[GEOCODE_COLUMN_NAME]) and pd.isnull(
        row[SITEADDRESS_COLUMN_NAME]
    ):
        # GoogleV3's address look like
        # VÍA DE LA PAZ, PACIFIC PALISADES, CA 90272, USA
        # and needs to be converted to parcel address in DINS database that looks like
        # VIA DE LA PAZ, PACIFIC PALISADES, CA 90272
        formatted_address: str = json.loads(row[GEOCODE_COLUMN_NAME])[
            "formatted_address"
        ]
        site_address = formatted_address
        if config.to_upper:
            site_address = site_address.upper()
        for replacement_config in config.replace:
            site_address = site_address.replace(
                replacement_config.old_value,
                replacement_config.new_value,
            )
        if config.apply_unidecode:
            # Fix replace special character like VÍA with English character VIA
            site_address = unidecode(site_address)

        return site_address
    return row[SITEADDRESS_COLUMN_NAME]


class ExcelGeoDataFrameLoader:
    """Helper class for loading Excel file into GeoDataFrame using GoogleV3 API"""

    def __init__(self, config: ExcelGeoDataFrameLoaderConfig):
        self.geolocator = GoogleV3(config.google_server_api_key)
        self.geocode = RateLimiter(
            self.geolocator.geocode,
            min_delay_seconds=config.min_delay_between_requests_in_seconds,
        )

    def add_geolocation_data(self, df: DataFrame, geocode_search_column_name: str):
        """Add geolocation information inplace to the given df by looking up
        geocode_search_column_name using geocode call to GoogleV3 API using Geopy.

        Args:
            df: DataFrame to add geolocation information to.
            geocode_search_column_name: columns to run geocode search on.
        """
        df[GEOCODE_COLUMN_NAME] = df.apply(
            label_location,
            geocode=self.geocode,
            address_column_name=geocode_search_column_name,
            axis=1,
        )

    def do_preprocessing(
        self, df: DataFrame, preprocessing_steps_config: List[PreProcessingStepConfig]
    ):
        """Run preprocessing steps on the dataframe, such as dropping null
        entires and selecting columns to keep.

        Args:
            df: DataFrame to preform preprocessing on
            preprocessing_steps: List of Dictionary of type to data containing
            instruction on what preprocessing to do on df.

        Returns:
            Processed DataFrame.
        """
        logger.debug("Running preprocessing step")
        for config in preprocessing_steps_config:
            if config.processing_type == "dropna":
                for entry in config.data:
                    df.dropna(subset=[entry], inplace=True)
                    logger.debug(f"Dropped column {entry}")
            elif config.processing_type == "select_column":
                df = df[config.data]
                logger.debug(f"Selected columns {config.data}")
            elif config.processing_type == "head":
                df = df.head(int(config.data[0]))
                logger.debug(f"Selected the first {config.data[0]} rows")

        return df

    def do_post_processing(
        self, df: DataFrame, post_processing_config: PostProcessingConfig
    ):
        """Run post-processing step on the dataframe, such as formatting the address
        and adding Latitude and Longitude so it can be converted to GeoDataFrame."""
        df[LATITUDE_COLUMN_NAME] = df.apply(label_latitude, axis=1)
        df[LONGITUDE_COLUMN_NAME] = df.apply(label_longitude, axis=1)
        df[SITEADDRESS_COLUMN_NAME] = df.apply(
            label_siteaddress, config=post_processing_config.address_formatting, axis=1
        )

    def load(
        self,
        config: ExcelGeoDataFrameConfig,
        input_file_path: str,
        output_file_path: str,
    ) -> GeoDataFrame:
        """Convert the provided excel file to GeoDataFrame by making request
        to GoogleV3 API with Geopy using the provided column to look up the
        geocode of the given entry.

        Args:
            config: Configuration for the Excel File to load into GeoDataFrame
            input_file_path: Base file path to look for all input files.
            output_file_path: Base file path to save all output files.

        Returns:
            GeoDataFrame of the provided excel sheet, including Global Coordinate System data for
            the address.
        """
        excel_file_to_load = os.path.join(input_file_path, config.file_name)
        if not os.path.exists(excel_file_to_load):
            logger.error(
                f"excel_to_geodataframe failed to load excel file: {excel_file_to_load}, "
                f"sheet_name: {config.sheet_name}, "
                f"file_label: {config.label}"
            )
            raise ValueError(f"Excel file '{excel_file_to_load}' is missing!")

        cache_file_path = os.path.join(output_file_path, get_cache_name(config.label))
        if os.path.exists(cache_file_path):
            logger.debug(
                f"Loading excel file {excel_file_to_load} from cache {cache_file_path}"
            )

            excel_file = pd.ExcelFile(cache_file_path)
            df = pd.read_excel(excel_file, config.sheet_name)
        else:
            logger.debug(f"Loaded excel file '{excel_file_to_load}'")
            excel_file = pd.ExcelFile(excel_file_to_load)
            df = pd.read_excel(excel_file, config.sheet_name)

            df = self.do_preprocessing(df, config.preprocessing)

            df[GEOCODE_COLUMN_NAME] = numpy.nan
            df[LATITUDE_COLUMN_NAME] = numpy.nan
            df[LONGITUDE_COLUMN_NAME] = numpy.nan
            df[SITEADDRESS_COLUMN_NAME] = numpy.nan

            self.add_geolocation_data(df, config.geocode_column_name)
            self.do_post_processing(df, config.post_processing)

        gdf = gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(
                df[LONGITUDE_COLUMN_NAME],
                df[LATITUDE_COLUMN_NAME],
            ),
            crs=config.post_processing.output_crs,
        )

        logger.debug(
            f"Saving GeoDataFrame for excel file {excel_file_to_load} to cache {cache_file_path}"
        )
        Path(output_file_path).mkdir(parents=True, exist_ok=True)
        gdf.to_excel(cache_file_path, sheet_name=config.sheet_name, index=False)
        return gdf
