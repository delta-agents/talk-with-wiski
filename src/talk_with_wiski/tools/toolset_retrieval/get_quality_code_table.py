"""
tool call to get metadata.
"""

from talk_with_wiski.models.modelset_retrieval.get_quality_code_table import (
    GetQualityCodeTableInput,
    GetQualityCodeTableOutput,
)
from talk_with_wiski.utils.logging_utils import log_tool_call


@log_tool_call
async def get_quality_code_table(ctx, input: GetQualityCodeTableInput) -> GetQualityCodeTableOutput:
    """
    Get quality code table.
    """

    quality_codes = {
        40:  {"code": "Betrouwaar",       "description": "---"},
        60:  {"code": "Geschat",          "description": "---"},
        80:  {"code": "HandCorr (oud)",   "description": "handmatig gecorrigeerde data (HandCorr)"},
        100: {"code": "AutoValide (oud)", "description": "automatisch goedgekeurde data (AutoValide)"},
        110: {"code": "Twijfelachtig",    "description": "---"},
        150: {"code": "AutoGevuld (oud)", "description": "automatisch aangevulde data (AutoGevuld)"},
        180: {"code": "Onbetrouwbaar",    "description": "---"},
        190: {"code": "Gecensureerd",     "description": "---"},
        200: {"code": "Ongecontroleerd",  "description": "---"},
        254: {"code": "Afwezig (oud)",    "description": "afgekeurde of ontbrekende data (Afwezig)"},
}

    return GetQualityCodeTableOutput(
        data=quality_codes,
        description="Quality code table",
    )
