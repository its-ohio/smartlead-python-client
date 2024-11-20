import csv
import json
from io import StringIO
from datetime import datetime, date
from typing import Optional, List

from ._utils import compact_list_to_str, JsonDict
from ._client_core import CoreClient
from ._fetcher import SmartleadFetcher
from ._enums import (
    TrackSetting,
    StopLeadSetting,
    EmailStatus,
    CampaignStatus,
    WebhookEventType,
    ClientPermission,
)


__all__ = ["SmartleadClient"]


class SmartleadClient(CoreClient):
    """
    Smartlead client.
    """

    def __init__(self, api_key: str) -> None:
        super().__init__(api_key=api_key)
        self.fetch = SmartleadFetcher(api_key=api_key)

    def create_campaign(self, name: str, client_id: Optional[int] = None) -> JsonDict:
        """
        Create a new campaign.

        :param name: Name of the new campaign
        :param client_id:
        :return:
        """
        return self._post(
            endpoint=f"campaigns/create",
            data={
                "name": name,
                "client_id": client_id,
            },
        )

    def update_campaign_schedule(
        self,
        campaign_id: int,
        timezone: str,
        days_of_the_week: List[int],
        start_hour: str,
        end_hour: str,
        min_time_between_emails: int,
        max_new_leads_per_day: int,
        schedule_start_time: datetime,
    ) -> JsonDict:
        """
        Update campaign schedule.

        :param campaign_id: ID of campaign to update.
        :param timezone: Name of the timezone, e.g., 'America/Los_Angeles'
        :param days_of_the_week: List of integers to represent weekdays, Monday -> 0, Tuesday -> 1, etc.
        :param start_hour: e.g., '01:15'
        :param end_hour: e.g., '13:18'
        :param min_time_between_emails: Minimum time between emails, in minutes.
        :param max_new_leads_per_day: Number of max new leads per day.
        :param schedule_start_time: Time at which the schedule starts.
        :return: Json indicating success, e.g., {'ok': True}
        """
        assert all(0 <= day <= 6 for day in days_of_the_week)
        return self._post(
            endpoint=f"campaigns/{campaign_id}/schedule",
            data={
                "timezone": timezone,
                "days_of_the_week": compact_list_to_str(obj=days_of_the_week),
                "start_hour": start_hour,
                "end_hour": end_hour,
                "min_time_between_emails": min_time_between_emails,
                "max_new_leads_per_day": max_new_leads_per_day,
                "schedule_start_time": schedule_start_time.isoformat(),
            },
        )

    def update_campaign_general_settings(
        self,
        campaign_id: int,
        track_settings: List[TrackSetting],
        stop_lead_settings: StopLeadSetting,
        unsubscribe_text: str,
        send_as_plain_text: bool,
        follow_up_percentage: int,
        client_id: int,
        enable_ai_esp_matching: bool = False,
    ) -> JsonDict:
        # TODO: confirm list/singular for settings
        return self._post(
            endpoint=f"campaigns/{campaign_id}/settings",
            data={
                "track_settings": compact_list_to_str(obj=track_settings),
                "stop_lead_settings": stop_lead_settings,
                "unsubscribe_text": unsubscribe_text,
                "send_as_plain_text": send_as_plain_text,
                "follow_up_percentage": follow_up_percentage,
                "client_id": client_id,
                "enable_ai_esp_matching": enable_ai_esp_matching,
            },
        )

    # TODO: implement this function
    def save_campaign_sequence(self):
        pass

    def delete_campaign(self, campaign_id: int) -> JsonDict:
        return self._delete(
            endpoint=f"campaigns/{campaign_id}",
        )

    def add_email_accounts_to_campaign(
        self, campaign_id: int, email_account_ids: List[int]
    ) -> JsonDict:
        return self._post(
            endpoint=f"campaigns/{campaign_id}/email-accounts",
            data={
                "email_account_ids": compact_list_to_str(obj=email_account_ids),
            },
        )

    def remove_email_account_from_campaign(
        self, campaign_id: int, email_account_ids: List[int]
    ) -> JsonDict:
        return self._delete(
            endpoint=f"campaigns/{campaign_id}/email-accounts",
            data={
                "email_account_ids": compact_list_to_str(obj=email_account_ids),
            },
        )

    def create_email_account(
        self,
        from_name: str,
        from_email: str,
        user_name: str,
        password: str,
        smtp_host: str,
        smtp_port: int,
        imap_host: str,
        imap_port: int,
        max_emails_per_day: int,
        account_id: Optional[int] = None,
        custom_tracking_url: str = "",
        bcc: str = "",
        signature: str = "",
        warmup_enabled: bool = False,
        total_warmup: Optional = None,
        daily_rampup: Optional = None,
        reply_rate_percentage: Optional[int] = None,
        client_id: Optional[int] = None,
    ) -> JsonDict:
        if reply_rate_percentage is not None:
            assert 0 <= reply_rate_percentage <= 100

        return self._post(
            endpoint="email-accounts/save",
            data={
                "id": account_id,
                "from_name": from_name,
                "from_email": from_email,
                "user_name": user_name,
                "password": password,
                "smtp_host": smtp_host,
                "smtp_port": smtp_port,
                "imap_host": imap_host,
                "imap_port": imap_port,
                "max_emails_per_day": max_emails_per_day,
                "custom_tracking_url": custom_tracking_url,
                "bcc": bcc,
                "signature": signature,
                "warmup_enabled": warmup_enabled,
                "total_warmup": total_warmup,
                "daily_rampup": daily_rampup,
                "reply_rate_percentage": reply_rate_percentage,
                "client_id": client_id,
            },
        )

    def update_email_account(
        self,
        email_account_id: int,
        max_emails_per_day: int,
        custom_tracking_url: str,
        bcc: str,
        signature: str,
        client_id: Optional[int] = None,
        time_to_wait_in_mins: Optional[int] = None,
    ) -> JsonDict:
        # TODO: check which of these parameters are required
        return self._post(
            endpoint=f"email-accounts/{email_account_id}",
            data={
                "max_emails_per_day": max_emails_per_day,
                "custom_tracking_url": custom_tracking_url,
                "bcc": bcc,
                "signature": signature,
                "client_id": client_id,
                "time_to_wait_in_mins": time_to_wait_in_mins,
            },
        )

    def update_email_account_warmup(
        self,
        email_account_id: int,
        warmup_enabled: bool,
        total_warmup_per_day: int,
        daily_rampup: int,
        reply_rate_percentage: int,
        warmup_key_id: str,
    ) -> JsonDict:
        assert 0 <= reply_rate_percentage <= 100
        return self._post(
            endpoint=f"email-accounts/{email_account_id}/warmup",
            data={
                "warmup_enabled": warmup_enabled,
                "total_warmup_per_day": total_warmup_per_day,
                "daily_rampup": daily_rampup,
                "reply_rate_percentage": reply_rate_percentage,
                "warmup_key_id": warmup_key_id,
            },
        )

    # TODO: implement this function
    def reply_to_lead_from_master_inbox(self) -> JsonDict:
        pass

    # TODO: implement this function
    def add_leads_to_campaign(self, campaign_id: int) -> JsonDict:
        pass

    def resume_lead_by_campaign_id(self, lead_id: int, campaign_id: int) -> JsonDict:
        return self._post(
            endpoint=f"campaigns/{campaign_id}/leads/{lead_id}/resume",
        )

    def pause_lead_by_campaign_id(self, lead_id: int, campaign_id: int) -> JsonDict:
        return self._post(
            endpoint=f"campaigns/{campaign_id}/leads/{lead_id}/pause",
        )

    def delete_lead_by_campaign_id(self, lead_id: int, campaign_id: int) -> JsonDict:
        return self._delete(
            endpoint=f"campaigns/{campaign_id}/leads/{lead_id}",
        )

    def unsubscribe_lead_from_campaign(
        self, lead_id: int, campaign_id: int
    ) -> JsonDict:
        return self._post(
            endpoint=f"campaigns/{campaign_id}/leads/{lead_id}/unsubscribe",
        )

    def add_leads_or_domains_to_global_block_list(
        self,
        removals: List[str],
        client_id: Optional[int] = None,
    ) -> JsonDict:
        return self._post(
            endpoint="leads/add-domain-block-list",
            data={
                "domain_block_list": removals,
                "client_id": client_id,
            },
        )

    # TODO: format lead-input
    def update_lead_using_lead_id(
        self,
    ) -> JsonDict:
        pass

    def update_lead_category_for_campaign(
        self,
        lead_id: str,
        campaign_id: int,
        category_id: int,
        pause_lead: bool,
    ) -> JsonDict:
        return self._post(
            endpoint=f"campaigns/{campaign_id}/leads/{lead_id}/category",
            data={
                "category_id": category_id,
                "pause_lead": pause_lead,
            },
        )

    def patch_campaign_status(
        self, campaign_id: int, status: CampaignStatus
    ) -> JsonDict:
        return self._post(
            endpoint=f"campaigns/{campaign_id}/status",
            data={
                "status": status,
            },
        )

    def update_campaign_webhook(
        self,
        campaign_id: int,
        webhook_name: str,
        webhook_url: str,
        event_types: List[WebhookEventType],
        categories: List[str],
        webhook_id: Optional[int] = None,
    ) -> JsonDict:
        return self._post(
            endpoint=f"campaigns/{campaign_id}/webhooks",
            data={
                "id": webhook_id,
                "name": webhook_name,
                "webhook_url": webhook_url,
                "event_types": event_types,
                "categories": categories,
            },
        )

    def delete_campaign_webhook(self, campaign_id: int, webhook_id: int) -> JsonDict:
        return self._delete(
            endpoint=f"campaigns/{campaign_id}/webhooks",
            data={
                "id": webhook_id,
            },
        )

    def add_client_to_system(
        self,
        name: str,
        email: str,
        permissions: List[ClientPermission],
        logo: str,
        password: str,
        logo_url: Optional[str] = None,
    ) -> JsonDict:
        return self._post(
            endpoint=f"client/save",
            data={
                "name": name,
                "email": email,
                "permission": permissions,
                "logo": logo,
                "logo_url": logo_url,
                "password": password,
            },
        )

    def reconnect_failed_email_accounts(self) -> JsonDict:
        return self._post(
            endpoint="email-accounts/reconnect-failed-email-accounts",
        )
