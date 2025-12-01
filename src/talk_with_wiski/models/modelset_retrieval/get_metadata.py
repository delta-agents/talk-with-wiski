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
        description="List of metadata for ts_id, site_no, or station_no, depending on input provided."
        ""
        "Example for site_no: "
        "'site_id': '11346', "
        "'site_name': 'De Moer H Loon op Zand',"
        "'site_no': '2161', "
        "'site_type_name': 'Stuw',"
        "'ATT_EIGENAAR': 'Brabantse Delta Watersysteem',"
        "'ATT_DAMOCODE': 'KST00798',"
        "'ATT_SITE_NO_OUD': '2161',"
        "'ATT_SITE_REMARKS': Some random field containing user-defined text' "
        ""
        "Example for station_no: "
        "'GAUGE_DATUM': '7.658'"
        "'GWREF_DATUM': '1.946'"
        "'MEETWIJZEBRON': 'Stand-alone'"
        "'Meetdoel_BMV': 'no'"
        "'Meetdoel_BOS_hoog_water': 'no'"
        "'Meetdoel_Bedienen': 'no'"
        "'Meetdoel_KRW': 'no'"
        "'Meetdoel_Mark-Vliet_boezem': 'no'"
        "'Meetdoel_Waterketen': 'no'"
        "'Meetdoel_Waterkwaliteit': 'no'"
        "'Meetdoel_Waterveiligheid_primair': 'no'"
        "'Meetdoel_Waterveiligheid_projecten': 'no'"
        "'Meetdoel_Waterveiligheid_regionaal': 'no'"
        "'Meetdoel_basismeetnet_N': 'no'"
        "'Meetdoel_basismeetnet_Q': 'no'"
        "'Meetdoel_basismeetnet_freatisch_G': 'no'"
        "'Meetdoel_calamiteitenzorg': 'no'"
        "'Meetdoel_controlemetingen': 'no'"
        "'Meetdoel_extern': 'no'"
        "'Meetdoel_ondergrens_N2000': 'no'"
        "'Meetdoel_peilbeheer': 'no'"
        "'Meetdoel_project_onderzoek': 'no'"
        "'Meetdoel_waterakkoorden': 'no'"
        "'Meetfrequentie_Handmeting': ''"
        "'PeilvakNummer': ''"
        "'STATION_NUMMER_OUD': '2161_WTH_BOV'"
        "'STATUS': 'Out of work'"
        "'admin_level': 'District'"
        "'admin_name': '---'"
        "'area_id': ''"
        "'area_name': ''"
        "'ngr_letter': '-'"
        "'object_type': 'Oppervlaktewaterhoogte;Oppervlaktewater Diver;General'"
        "'object_type_shortname': 'WSBD_OPPERVLAKTEW_STATION;WSBD_OPPERVLAKTEW_DIVER;GN_STATION'"
        "'region_district': '---'"
        "'river_id': ''"
        "'river_name': ''"
        "'station_diary': ''"
        "'station_diary_status': ''"
        "'station_gauge_datum': '7.658'"
        "'station_gauge_datum_from': '-2208988800000'"
        "'station_gauge_datum_unit': 'Normaal Amsterdams Peil'"
        ""
        "'ts_id has the same fields/keys as station_no, but does not contains fields: ''"
        "'area_id','area_name','object_type','object_type_shortname','river_id''river_name'"
        "",
    )
    description: str = Field(
        ...,
        description="List of metadata for ts_id, site_no, or station_no, depending on input provided",
    )
