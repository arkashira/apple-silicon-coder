from apple_silicon_coder import AppleSiliconCoder, Tier
import pytest

def test_create_team():
    coder = AppleSiliconCoder()
    coder.create_team(1)
    assert coder.teams[1].tier == Tier.FREE

def test_upgrade_to_paid():
    coder = AppleSiliconCoder()
    coder.create_team(1)
    coder.upgrade_to_paid(1)
    assert coder.teams[1].tier == Tier.PAID

def test_get_team_billing_info():
    coder = AppleSiliconCoder()
    coder.create_team(1)
    coder.upgrade_to_paid(1)
    billing_info = coder.get_team_billing_info(1)
    assert billing_info["stripe_customer_id"] == "example_customer_id"

def test_handle_stripe_webhook():
    coder = AppleSiliconCoder()
    coder.create_team(1)
    coder.upgrade_to_paid(1)
    event = {
        "type": "invoice.payment_succeeded",
        "metadata": {"team_id": "1"}
    }
    coder.handle_stripe_webhook(event)
    assert coder.teams[1].billing_info["payment_status"] == "paid"

def test_get_paid_tier_price():
    coder = AppleSiliconCoder()
    assert coder.get_paid_tier_price() == 49

def test_team_not_found():
    coder = AppleSiliconCoder()
    with pytest.raises(ValueError):
        coder.get_team_billing_info(1)
