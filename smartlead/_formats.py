from datetime import datetime
from typing import TypedDict, List, Optional, Type, Any, TypeVar

from ._enums import CampaignStatus, TrackSetting, StopLeadSetting
from ._utils import Json


T = TypeVar("T")


def _parse_json_to_desired_type(
    obj: Json,
    desired_type: Type[T],
) -> T:
    if desired_type == Any:
        return obj

    type_name = str(desired_type)
    # check for nested typing, i.e., str(List[Any]) == "typing.List[typing.Any]"
    if "[" in type_name:
        # find the name of the class: 'typing.List[typing.Any]' -> 'List'
        outer_type_name = type_name.split("[")[0].split(".")[-1].lower()
        inner_types = desired_type.__args__
        # check optional
        if outer_type_name == "optional":
            if obj is None:
                return None

            else:
                return _parse_json_to_desired_type(
                    obj=obj,
                    desired_type=inner_types[0],
                )

        # check list:
        if outer_type_name == "list":
            if not isinstance(obj, list):
                raise TypeError(
                    f"Unexpected argument type. Can't convert obj of type {type(obj).__name__} to list."
                )

            return [
                _parse_json_to_desired_type(
                    obj=item,
                    desired_type=inner_types[0],
                )
                for item in obj
            ]

        # check dictionary:
        if outer_type_name == "dict":
            if not isinstance(obj, dict):
                raise TypeError(
                    f"Unexpected argument type. Can't convert obj of type {type(obj).__name__} to dict."
                )

            return {
                _parse_json_to_desired_type(
                    obj=key,
                    desired_type=inner_types[0],
                ): _parse_json_to_desired_type(
                    obj=val,
                    desired_type=inner_types[1],
                )
                for key, val in obj.items()
            }

        raise TypeError(f"Unimplemented nested type: {type_name}")

    # now that nested types are handled, we can run an isinstance check:
    if isinstance(obj, desired_type):
        return obj

    # as optional was already handled, if we get None now, it should break:
    if obj is None:
        raise TypeError(f"Expected type {desired_type} but got None.")

    # check for Container:
    if issubclass(desired_type, Container):
        return Container.from_json(json_data=obj)

    raise TypeError(
        f"Can't convert {obj} of type {type(obj).__name__} to {desired_type.__name__}."
    )


class Container:
    """
    Base class for objects that can be easily created from json.
    """

    @classmethod
    def from_json(cls: Type["C"], json_data: Json) -> "C":
        pass


C = TypeVar("C", bound=Container)


class CampaignSchedulerCron(TypedDict):
    tz: str
    days: List[int]
    end_hour: str
    start_hour: str


class CampaignInfo(TypedDict):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    status: CampaignStatus
    name: str
    track_settings: List[TrackSetting]
    scheduler_cron_value: CampaignSchedulerCron
    min_time_btwn_emails: int
    max_leads_per_day: int
    stop_lead_settings: StopLeadSetting
    enable_ai_esp_matching: bool
    send_as_plain_text: bool
    follow_up_percentage: bool
    unsubscribe_text: str
    parent_campaign_id: int
    client_id: int


class CampaignSequenceDelayDetails(TypedDict):
    delay_in_days: int


class CampaignSequenceVariant(TypedDict):
    id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    subject: str
    email_body: str
    email_campaign_seq_id: int
    variant_label: str
    optional_email_body_1: Optional[str]
    variant_distribution_percentage: Optional[str]


class CampaignSequence(TypedDict):
    id: int
    created_at: datetime
    updated_at: datetime
    email_campaign_id: int
    seq_number: int
    seq_delay_details: CampaignSequenceDelayDetails
    subject: str
    email_body: str
    sequence_variants: Optional[List[CampaignSequenceVariant]]


class LeadCategoryInfo(TypedDict):
    id: int
    created_at: datetime
    name: str


class CampaignLeads(TypedDict):
    total_leads: int
    data: List[dict]
    offset: int
    limit: int
