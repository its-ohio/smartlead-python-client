from enum import Enum
from typing import Any, TypeVar, Type, List


__all__ = [
    "TrackSetting",
    "StopLeadSetting",
    "EmailStatus",
    "CampaignStatus",
    "WebhookEventType",
    "ClientPermission",
]


class _BaseEnum(str, Enum):
    """
    Base class for enums
    """

    @classmethod
    def all(cls: Type["T"]) -> List["T"]:
        return [cls(item) for item in cls]

    @classmethod
    def contains(cls, obj: Any) -> bool:
        for item in cls:
            if str(obj) == str(item):
                return True

        return False

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, (_BaseEnum, str)) and str(self) == str(other)

    def __hash__(self) -> int:
        return hash(str(self))


T = TypeVar("T", bound=_BaseEnum)


class LeadStatus(_BaseEnum):
    """
    Smartlead lead status.
    """

    STARTED = "STARTED"
    """
    The lead is scheduled to start and is yet to receive the 1st email in the sequence.
    """
    COMPLETED = "COMPLETED"
    """
    The lead has received all the emails in the campaign.
    """
    BLOCKED = "BLOCKED"
    """
    A lead is blocked when the email sent is bounced or if added in the global block list.
    """
    INPROGRESS = "INPROGRESS"
    """
    The lead has last received at least one email in the sequence.
    """


x = LeadStatus.STARTED


class TrackSetting(_BaseEnum):
    """
    Smartlead track settings.
    """

    DONT_TRACK_EMAIL_OPEN = "DONT_TRACK_EMAIL_OPEN"
    DONT_TRACK_LINK_CLICK = "DONT_TRACK_LINK_CLICK"
    DONT_TRACK_REPLY_TO_AN_EMAIL = "DONT_TRACK_REPLY_TO_AN_EMAIL"


class StopLeadSetting(_BaseEnum):
    """
    Smartlead stop-lead settings.
    """

    CLICK_ON_A_LINK = "CLICK_ON_A_LINK"
    OPEN_AN_EMAIL = "OPEN_AN_EMAIL"
    # TODO: check whether or not this is a valid setting
    REPLY_TO_AN_EMAIL = "REPLY_TO_AN_EMAIL"


class EmailStatus(_BaseEnum):
    """
    Smartlead email statuses.
    """

    OPENED = "opened"
    CLICKED = "clicked"
    REPLIED = "replied"
    UNSUBSCRIBED = "unsubscribed"
    BOUNCED = "bounced"


class CampaignStatus(_BaseEnum):
    """
    Smartlead campaign statuses.
    """

    PAUSED = "PAUSED"
    STOPPED = "STOPPED"
    COMPLETED = "COMPLETED"
    ACTIVE = "ACTIVE"
    DRAFTED = "DRAFTED"
    START = "START"


class WebhookEventType(_BaseEnum):
    """
    Webhook event type
    """

    EMAIL_SENT = "EMAIL_SENT"
    EMAIL_OPEN = "EMAIL_OPEN"
    EMAIL_LINK_CLICK = "EMAIL_LINK_CLICK"
    EMAIL_REPLY = "EMAIL_REPLY"
    LEAD_UNSUBSCRIBED = "LEAD_UNSUBSCRIBED"
    LEAD_CATEGORY_UPDATED = "LEAD_CATEGORY_UPDATED"


class EmailType(_BaseEnum):
    """
    Smartlead email types
    """

    GMAIL = "GMAIL"
    SMTP = "SMTP"
    ZOHO = "ZOHO"
    OUTLOOK = "OUTLOOK"


class LeadStatus(_BaseEnum):
    """
    Smartlead lead status.
    """

    STARTED = "STARTED"
    COMPLETED = "COMPLETED"
    BLOCKED = "BLOCKED"
    INPROGRESS = "INPROGRESS"


class ClientPermission(_BaseEnum):
    """
    Smartlead client permission
    """

    # TODO: find all permissions
    REPLY_MASTER_INBOX = "reply_master_inbox"
    FULL_ACCESS = "full_access"
