from pydantic import Field, model_validator
from pydantic_ai import ModelRetry
from typing import Dict, List, Optional

from talk_with_wiski.models.base import WiskiBaseModel


class GetMetadataInput(WiskiBaseModel):
    """
    Input model for get_timeseries_metadata tool.
    ts_id is required (string or list of strings).
    """

    ts_id: Optional[str | List[str]] = Field(
        default=None,
        description="ts_id or list of ts_ids",
    )
    site_no: Optional[str | List[str]] = Field(
        default=None,
        description="site_no or list of site_nos",
    )
    station_no: Optional[str | List[str]] = Field(
        default=None,
        description="station_no or list of station_nos",
    )

    @model_validator(mode="after")
    def validate_exclusive_fields(self):
        ts_id, site_no, station_no = (
            self.ts_id,
            self.site_no,
            self.station_no,
        )
        if not (ts_id or site_no or station_no):
            raise ModelRetry(
                "At least one ts_id (str or list of strings) or site_no (str or list of strings) or station_no (str or list of strings) must be provided."
            )
        return self


class GetMetadataOutput(WiskiBaseModel):
    data: List[Dict[str, str]] = Field(
        ...,
        description="List of metadata for ts_id, site_no, or station_no, depending on input provided.",
    )
    description: str = Field(
        ...,
        description="List of metadata for ts_id, site_no, or station_no, depending on input provided",
    )
