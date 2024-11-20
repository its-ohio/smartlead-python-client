import csv
import json
import math
from io import StringIO
from datetime import date
from typing import List, Optional

from ._enums import EmailStatus
from ._utils import JsonDict
from ._client_core import CoreClient
from ._formats import CampaignLeads


__all__ = ["SmartleadFetcher"]

_PAGINATION_LIMIT = 100


class SmartleadFetcher(CoreClient):
    """
    Smartlead fetcher.
    """

    def campaign_info(self, campaign_id: int) -> JsonDict:
        """
        Fetch information about a campaign.

        :param campaign_id: Integer ID of the campaign.
        :return: Campaign information.
        """
        return self._get(
            endpoint=f"campaigns/{campaign_id}",
        )

    def campaign_sequence(self, campaign_id: int) -> List[JsonDict]:
        return self._get(
            endpoint=f"campaigns/{campaign_id}/sequences",
        )

    def all_campaigns(self) -> List[JsonDict]:
        """
        Fetch all campaigns.

        :return: A list of all campaigns.
        """
        return self._get(
            endpoint="campaigns",
        )

    def campaign_email_accounts(self, campaign_id: int) -> List[JsonDict]:
        """
        Fetch info on all email accounts associated with a campaign.

        :param campaign_id: ID of the campaign.
        :return: A list of dictionaries, each containing info on an email account.
        """
        return self._get(
            endpoint=f"campaigns/{campaign_id}/email-accounts",
        )

    def all_campaigns_with_lead_id(self, lead_id: int) -> List[JsonDict]:
        return self._get(
            endpoint=f"leads/{lead_id}/campaigns",
        )

    def all_email_accounts(self, offset: int = 0, limit: int = 100) -> List[JsonDict]:
        """
        Fetch all email accounts.

        :param offset: Pagination offset.
        :param limit: Limit, max 100
        :return: A list of email accounts.
        """
        assert offset >= 0
        assert limit <= 100
        return self._get(
            endpoint="email-accounts",
            params={
                "offset": offset,
                "limit": limit,
            },
        )

    def email_account(self, email_account_id: int) -> JsonDict:
        """
        Fetch info for a single email account.

        :param email_account_id: ID of the email account to fetch.
        :return: JSON data describing the email account.
        """
        return self._get(
            endpoint=f"email-accounts/{email_account_id}/",
        )

    def email_account_warmup_stats(self, email_account_id: int) -> JsonDict:
        """
        Fetch warmup stats for the specified email account.

        :param email_account_id: ID of the email account to fetch warmup stats for.
        :return: JSON data containing the warmup stats.
        """
        return self._get(
            endpoint=f"email-accounts/{email_account_id}/warmup-stats",
        )

    def _campaign_leads(
        self,
        campaign_id: int,
        offset: int,
        limit: int,
    ) -> CampaignLeads:
        assert offset >= 0
        assert 0 <= limit <= _PAGINATION_LIMIT
        return self._get(
            endpoint=f"campaigns/{campaign_id}/leads",
            params={
                "offset": offset,
                "limit": limit,
            },
        )

    def all_campaign_leads(
        self,
        campaign_id: int,
    ) -> List[dict]:
        """
        Fetch all leads for a campaign.

        :param campaign_id: Integer ID of the campaign, e.g., '50318'.
        :return: JSON data containing all the leads.
        """
        first_leads = self._campaign_leads(
            campaign_id=campaign_id,
            offset=0,
            limit=_PAGINATION_LIMIT,
        )
        all_leads = first_leads["data"].copy()
        total_leads = int(first_leads["total_leads"])
        n_fetches_required = (total_leads - len(first_leads["data"])) / 100
        for i in range(math.ceil(n_fetches_required)):
            new_leads = self._campaign_leads(
                campaign_id=campaign_id,
                offset=len(all_leads),
                limit=_PAGINATION_LIMIT,
            )
            all_leads.extend(new_leads["data"])

        return all_leads

    def lead_categories(self) -> List[JsonDict]:
        """
        Fetch all possible lead categories.

        :return:
        """
        return self._get(
            endpoint="leads/fetch-categories",
        )

    def lead_by_email_address(self, email_address: str) -> JsonDict:
        return self._get(
            endpoint=f"leads/",
            params={
                "email": email_address,
            },
        )

    def campaign_data(self, campaign_id: int) -> List[JsonDict]:
        """
        Fetch campaign data for the specified campaign.

        :param campaign_id: Integer ID for the campaign.
        :return: A list of dictionaries containing campaign data.
        """
        csv_text = self._get(
            endpoint=f"campaigns/{campaign_id}/leads-export",
            allow_text_return=True,
        )
        file = StringIO(csv_text)
        data, headings = [], []
        for csv_row in csv.reader(file):
            # if we are in the first row, and 'headings' is still an empty list, save the headings and then move on
            if not headings:
                headings = csv_row
                continue

            row = {}
            for key, val in zip(headings, csv_row):
                if key in (
                    "id",
                    "campaign_lead_map_id",
                    "last_email_sequence_sent",
                    "open_count",
                    "click_count",
                    "reply_count",
                ):
                    if val == '':
                        row[key] = 0
                    else:
                        row[key] = int(val)

                elif key in (
                    "custom_fields",
                    "unsubscribed_client_id_map",
                ):
                    row[key] = json.loads(val)

                elif key in (
                    "is_interested",
                    "is_unsubscribed",
                ):
                    row[key] = str(val).lower() == "true"

                else:
                    row[key] = val

            data.append(row)

        return data

    def lead_message_history_for_campaign(
        self, lead_id: int, campaign_id: int
    ) -> JsonDict:
        return self._get(
            endpoint=f"campaigns/{campaign_id}/leads/{lead_id}/message-history",
        )

    def all_clients(self) -> List[JsonDict]:
        return self._get(
            endpoint="client",
        )

    def campaign_stats_by_campaign_id(
        self,
        campaign_id: int,
        offset: int = 0,
        limit: int = 100,
        email_sequence_number: Optional[int] = None,
        email_status: Optional[EmailStatus] = None,
    ) -> JsonDict:
        """
        Fetch stats for a campaign.

        :param campaign_id: Integer ID of the campaign to fetch stats for.
        :param offset: Pagination offset.
        :param limit: Pagination limit.
        :param email_sequence_number: ???
        :param email_status: ???
        :return: JSON dictionary containing stats for the specified campaign.
        """
        if email_sequence_number is not None:
            assert 0 <= email_sequence_number <= 4

        return self._get(
            endpoint=f"campaigns/{campaign_id}/statistics",
            params={
                "offset": offset,
                "limit": limit,
                "email_sequence_number": email_sequence_number,
                "email_status": email_status,
            },
        )

    def campaign_stats_by_id_and_date_range(
        self,
        campaign_id: int,
        start_date: date,
        end_date: date,
    ) -> List[JsonDict]:
        assert start_date <= end_date
        return self._get(
            endpoint=f"campaigns/{campaign_id}/analytics-by-date",
            params={
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
        )

    def campaign_top_level_analytics(self, campaign_id: int) -> JsonDict:
        """
        Fetch an analytical summary for the provided campaign.

        :param campaign_id: Integer ID of the campaign to fetch analytics for.
        :return: JSON dictionary containing campaign analytics.
        """
        return self._get(
            endpoint=f"campaigns/{campaign_id}/analytics",
        )

    def webhooks_by_campaign_id(self, campaign_id: int) -> JsonDict:
        return self._get(
            endpoint=f"campaigns/{campaign_id}/webhooks",
        )
