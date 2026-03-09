# Config
from talk_with_wiski.models.modelset_1.example1 import (
    AddIndexInput,
    AddIndexOutput,
)

from talk_with_wiski.models.modelset_2.example2 import (
    Example2Input,
    Example2Output,
)

from talk_with_wiski.models.modelset_retrieval.get_locations import (
    GetLocationsInput,
    GetLocationsOutput,
)

from talk_with_wiski.models.modelset_retrieval.get_sites import (
    GetSitesInput,
    GetSitesOutput,
)

from talk_with_wiski.models.modelset_retrieval.get_parameters import (
    GetParametersInput,
    GetParametersOutput,
)

from talk_with_wiski.models.modelset_retrieval.get_group_list import (
    GetGroupListInput,
    GetGroupListOutput,
    GroupItem,
)

from talk_with_wiski.models.modelset_retrieval.get_parametertype_list import (
    GetParametertypeListInput,
    GetParametertypeListOutput,
)

from talk_with_wiski.models.modelset_retrieval.get_timeseries_list import (
    GetTimeseriesListInput,
    GetTimeseriesListOutput,
)

from talk_with_wiski.models.modelset_retrieval.get_timeseries_values import (
    GetTimeseriesValuesInput,
    GetTimeseriesValuesOutput,
)

from talk_with_wiski.models.modelset_retrieval.get_timeseries_type import (
    GetTimeseriesTypeInput,
    GetTimeseriesTypeOutput,
    TimeseriesType,
)

from talk_with_wiski.models.modelset_retrieval.get_metadata import (
    GetMetadataInput,
    GetMetadataOutput,
)

from talk_with_wiski.models.modelset_retrieval.get_quality_code_table import (
    GetQualityCodeTableInput,
    GetQualityCodeTableOutput,
)

from talk_with_wiski.models.modelset_analysis.analyse_timeseries_trend import (
    AnalyseTimeseriesTrendInput,
    AnalyseTimeseriesTrendOutput,
    LinearTrendLine,
)

from talk_with_wiski.models.modelset_analysis.analyse_timeseries_statistics import (
    AnalyseTimeseriesStatsInput,
    AnalyseTimeseriesStatsOutput,
    TimeseriesStatistics,
)

from talk_with_wiski.models.modelset_analysis.analyse_timeseries_thresholds import (
    AnalyseTimeseriesThresholdsInput,
    AnalyseTimeseriesThresholdsOutput,
    TimeseriesThresholds,
)

from talk_with_wiski.models.modelset_analysis.analyse_timeseries_availability import (
    AnalyseTimeseriesAvailabilityInput,
    AnalyseTimeseriesAvailabilityOutput,
)

from talk_with_wiski.models.modelset_analysis.analyse_timeseries_quality_code import (
    AnalyseTimeseriesQualityCodeInput,
    AnalyseTimeseriesQualityCodeOutput,
)
from talk_with_wiski.models.modelset_retrieval.get_current_time import (
    GetCurrentTimeInput,
    GetCurrentTimeOutput,
)

__all__ = [
    "AddIndexInput",
    "AddIndexOutput",
    "Example2Input",
    "Example2Output",
    "GetLocationsInput",
    "GetLocationsOutput",
    "GetSitesInput",
    "GetSitesOutput",
    "GetParametersInput",
    "GetParametersOutput",
    "GetGroupListInput",
    "GetGroupListOutput",
    "GroupItem",
    "GetParametertypeListInput",
    "GetParametertypeListOutput",
    "GetTimeseriesListInput",
    "GetTimeseriesListOutput",
    "GetTimeseriesValuesInput",
    "GetTimeseriesValuesOutput",
    "GetTimeseriesTypeInput",
    "GetTimeseriesTypeOutput",
    "TimeseriesType",
    "GetMetadataInput",
    "GetMetadataOutput",
    "GetQualityCodeTableInput",
    "GetQualityCodeTableOutput",
    "AnalyseTimeseriesTrendInput",
    "AnalyseTimeseriesTrendOutput",
    "LinearTrendLine",
    "AnalyseTimeseriesStatsInput",
    "AnalyseTimeseriesStatsOutput",
    "TimeseriesStatistics",
    "AnalyseTimeseriesThresholdsInput",
    "AnalyseTimeseriesThresholdsOutput",
    "TimeseriesThresholds",
    "AnalyseTimeseriesAvailabilityInput",
    "AnalyseTimeseriesAvailabilityOutput",
    "AnalyseTimeseriesQualityCodeInput",
    "AnalyseTimeseriesQualityCodeOutput",
    "GetCurrentTimeInput",
    "GetCurrentTimeOutput",
]
