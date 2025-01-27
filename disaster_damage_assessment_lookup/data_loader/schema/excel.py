"""Schema definition for the excel data loader components."""

from dataclasses import field
from typing import List, Optional

from marshmallow_dataclass import dataclass


@dataclass
class StringReplacementConfig:
    """Configuration for the string replacement operation"""

    old_value: str
    """Old value to find for the string replacement."""

    new_value: str
    """New value to replace the old_value with for string replacement."""


@dataclass
class AddressFormattingConfig:
    """Configuration for address formatting."""

    to_upper: bool = False
    """Whether or not the address should be converted to upper case. Default to False"""

    replace: Optional[List[StringReplacementConfig]] = field(default_factory=list)
    """List of string replacement to apply to the address."""

    apply_unidecode: bool = True
    """Whether or not to apply unidecode to convert non-English character to English character.
    Default to True."""


@dataclass
class PostProcessingConfig:
    """Configuration for post processing steps to run after getting the geocode."""

    address_formatting: Optional[AddressFormattingConfig] = field(
        default=AddressFormattingConfig
    )
    """Configuration for formatting changes to be made to address returned by geocoding function."""

    output_crs: Optional[str] = "EPSG:4326"
    """Output Coordinate Reference System format for the GeoDataFrame. Default to EPSG:4236."""


@dataclass
class PreProcessingStepConfig:
    """Configuration for the preprocessing steps to run before getting the geocode."""

    processing_type: str
    """Type or preprocessing type to run."""

    data: List[str]
    """Data to pass to the preprocessing operation."""


@dataclass
class ExcelGeoDataFrameConfig:
    """Excel GeoDataFrame data loader configuration."""

    file_name: str
    """File name for the Excel file to load and convert to GeoDataFrame."""

    sheet_name: str
    """Sheet name inside of the Excel file to load and convert to GeoDataFrame."""

    label: str
    """Label for the output GeoDataFrame. Will be use as a reference from other parts of the Himl
    configuration, as well as for creating cache file for this GeoDataFrame."""

    geocode_column_name: str
    """Name of the column in the Excel spreadsheet to use for the geocode lookup for coordinate 
    and normalized address, e.g. the raw input address column."""

    preprocessing: Optional[List[PreProcessingStepConfig]] = field(default_factory=list)
    """Preprocessing operations to run before running the geocoding operation.
    List of Dictionaries with key for the type of operation to run and value 
    as the list of data to pass to the operation."""

    post_processing: Optional[PostProcessingConfig] = field(
        default=PostProcessingConfig
    )
    """Configuration for post processing steps to run after getting the geocode."""


@dataclass
class ExcelGeoDataFrameLoaderConfig:
    """ExcelGeoDataFrameLoader class configuration."""

    google_server_api_key: str
    """API Key used for making request to GoogleV3 API for geocoding information."""

    min_delay_between_requests_in_seconds: float = 0.5
    """Minimum delay in seconds between Geocode request operation to prevent 
    throttling by the provider service. Default to 0.5 seconds."""
