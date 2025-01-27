"""Schema configuration for the Matcher."""

from dataclasses import field
from typing import Dict, List, Optional

from marshmallow_dataclass import dataclass


@dataclass
class SaveFileConfig:
    """Save file configuration for the result from the matcher."""

    file_name: str
    """Name of the file to save the matcher result to."""

    sheet_name: str
    """Name of the excel sheet to save the result to."""

    include_index: Optional[bool] = False
    """Whether or not to include the generated index column from the matcher result."""

    columns: Optional[List[str]] = None
    """Columns to select for the save file"""


@dataclass
class ColumnSuffixConfig:
    """Configuration for the column suffix on merge operation."""

    left: str
    """Suffix for the left column."""

    right: str
    """Suffix for the right column."""


@dataclass
class MatcherConfig:
    """Excel GeoDataFrame data loader configuration."""

    label: str
    """Label for the matched result. Will be use as a reference from other parts of the Himl
    configuration."""

    unmatched_label: str
    """Label for the unmatched result. Will be use as a reference from other parts of the Himl
    configuration."""

    matcher_type: str
    """Name of the type of the matcher to use for the matching."""

    source_data: str
    """Source data to match against."""

    match_against_data: str
    """Data to match against the source data."""

    matcher_data_key_list: Optional[Dict[str, List[str]]] = field(default_factory=list)
    """Key List pair for the data needed for the specific matcher."""

    matcher_data_key_value: Optional[Dict[str, str]] = field(default_factory=list)
    """Key Value pair for the data needed for the specific matcher."""

    save_file: Optional[SaveFileConfig] = field(default=SaveFileConfig)
    """Configuration for saving the matcher result to excel file. Optional and will 
    not save if omitted."""

    column_suffix: Optional[ColumnSuffixConfig] = None
    """Configuration for the column suffix on merge operation."""


@dataclass
class MatcherConfigWrapper:
    """Wrapper class for the Matchers definitions"""

    matcher: Optional[Dict[str, MatcherConfig]] = field(default_factory=dict)
    """Dictionary list of matchers to execute in order."""
