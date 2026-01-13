from pydantic import Field
from talk_with_wiski.models.base import WiskiBaseModel


class GetCurrentTimeInput(WiskiBaseModel):
    """
    Input model for get_current_time tool.
    """

    


class GetCurrentTimeOutput(WiskiBaseModel):
    """
    Output model for get_current_time tool.
    """

    current_time: str = Field(..., description="Current time as a string")
    description: str = Field(..., description="Description of the current time data")