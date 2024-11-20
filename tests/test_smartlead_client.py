import os
import random
from typing import List

from dotenv import load_dotenv

from smartlead import SmartleadClient


# try both locations (such that the tests work, regardless of whether the tests are run from):
load_dotenv(".env.local")
load_dotenv("../.env.local")

# setup client:
client = SmartleadClient(api_key=os.getenv("SMARTLEAD_API_KEY"))


def _random_id(obj: List[dict]) -> int:
    index = random.randint(0, len(obj) - 1)
    return obj[index]["id"]


def _test_email_account(account: dict) -> None:
    assert isinstance(account, dict)
    assert "id" in account
    assert isinstance(account["id"], int)
    assert "from_email" in account
    assert "@" in account["from_email"]
    assert "warmup_details" in account


def _test_lead(lead: dict) -> None:
    assert isinstance(lead, dict)
    assert "id" in lead
    assert isinstance(lead["id"], int)
    assert "first_name" in lead
    assert "email" in lead
    assert "company_name" in lead


def test_fetch_all_campaigns() -> None:
    campaigns = client.fetch.all_campaigns()
    assert isinstance(campaigns, list)
    for campaign in campaigns:
        assert isinstance(campaign, dict)
        assert "id" in campaign


# now that we've tested fetch_all_campaigns, lets get the campaigns for easy use in future tests
all_campaigns = client.fetch.all_campaigns()


def test_fetch_campaign_info() -> None:
    campaign_id = _random_id(obj=all_campaigns)
    campaign = client.fetch.campaign_info(campaign_id=campaign_id)
    # run some sense checks:
    assert isinstance(campaign, dict)
    assert "id" in campaign
    assert campaign["id"] == campaign_id


def test_fetch_campaign_sequence() -> None:
    campaign_id = _random_id(obj=all_campaigns)
    sequence = client.fetch.campaign_sequence(campaign_id=campaign_id)
    assert isinstance(sequence, list)
    for item in sequence:
        assert isinstance(item, dict)
        assert "email_campaign_id" in item
        assert item["email_campaign_id"] == campaign_id


def test_fetch_lead_categories() -> None:
    categories = client.fetch.lead_categories()
    assert isinstance(categories, list)
    for category in categories:
        assert isinstance(category, dict)


def test_fetch_all_email_accounts() -> None:
    limit = random.randint(1, 100)
    all_accounts = client.fetch.all_email_accounts(limit=limit)
    assert isinstance(all_accounts, list)
    assert len(all_accounts) <= limit
    for account in all_accounts:
        _test_email_account(account=account)


# now that we've tested fetch_all_email_accounts, let's get the accounts for easy use in future tests
all_email_accounts = client.fetch.all_email_accounts()


def test_fetch_email_account() -> None:
    account_id = _random_id(obj=all_email_accounts)
    account = client.fetch.email_account(email_account_id=account_id)
    _test_email_account(account=account)


def test_fetch_campaign_email_accounts() -> None:
    campaign_id = _random_id(obj=all_campaigns)
    email_accounts = client.fetch.campaign_email_accounts(campaign_id=campaign_id)
    assert isinstance(email_accounts, list)
    for account in email_accounts:
        _test_email_account(account=account)


def test_fetch_email_account_warmup_stats() -> None:
    warmup_accounts = [
        account
        for account in all_email_accounts
        if account["warmup_details"] is not None
    ]
    account_id = _random_id(obj=warmup_accounts)
    warmup_stats = client.fetch.email_account_warmup_stats(email_account_id=account_id)
    assert isinstance(warmup_stats, dict)
    assert "id" in warmup_stats
    assert warmup_stats["id"] == account_id


def test_fetch_all_campaign_leads() -> None:
    campaign_id = _random_id(obj=all_campaigns)
    limit = random.randint(1, 100)
    campaign_leads = client.fetch.all_campaign_leads(
        campaign_id=campaign_id,
        limit=limit,
    )
    assert isinstance(campaign_leads, dict)
    assert "total_leads" in campaign_leads
    # test actual data:
    assert "data" in campaign_leads
    data = campaign_leads["data"]
    assert isinstance(data, list)
    assert len(data) <= limit and len(data) <= int(campaign_leads["total_leads"])
    for lead_info in data:
        assert isinstance(lead_info, dict)
        assert "campaign_lead_map_id" in lead_info
        assert "lead" in lead_info
        _test_lead(lead=lead_info["lead"])


def test_fetch_all_lead_categories() -> None:
    lead_categories = client.fetch.lead_categories()
    assert isinstance(lead_categories, list)
    for lead_category in lead_categories:
        assert isinstance(lead_category, dict)
        assert "id" in lead_category
        assert "name" in lead_category


def test_fetch_campaign_stats_by_campaign_id() -> None:
    campaign_id = _random_id(obj=all_campaigns)
    limit = random.randint(1, 100)
    campaign_stats = client.fetch.campaign_stats_by_campaign_id(
        campaign_id=campaign_id,
        limit=limit,
    )
    assert isinstance(campaign_stats, dict)
    assert "total_stats" in campaign_stats
    # test actual data:
    assert "data" in campaign_stats
    data = campaign_stats["data"]
    assert isinstance(data, list)
    assert len(data) <= limit and len(data) <= int(campaign_stats["total_stats"])
    for stat in data:
        assert isinstance(stat, dict)


def test_fetch_campaign_top_level_analytics() -> None:
    campaign_id = _random_id(obj=all_campaigns)
    analytics = client.fetch.campaign_top_level_analytics(
        campaign_id=campaign_id,
    )
    assert isinstance(analytics, dict)
    assert analytics["id"] == campaign_id
    assert "campaign_lead_stats" in analytics


def test_fetch_all_clients() -> None:
    clients = client.fetch.all_clients()
    assert isinstance(clients, list)
    for clt in clients:
        assert isinstance(clt, dict)
        assert "id" in clt
        assert "name" in clt
