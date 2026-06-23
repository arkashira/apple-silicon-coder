import json
from dataclasses import dataclass
from enum import Enum
from typing import Dict

class Tier(Enum):
    FREE = 1
    PAID = 2

@dataclass
class Team:
    id: int
    tier: Tier
    billing_info: Dict[str, str]

class AppleSiliconCoder:
    def __init__(self):
        self.teams = {}
        self.stripe_webhooks = {}

    def create_team(self, team_id: int, tier: Tier = Tier.FREE):
        self.teams[team_id] = Team(id=team_id, tier=tier, billing_info={})

    def upgrade_to_paid(self, team_id: int):
        if team_id not in self.teams:
            raise ValueError("Team not found")
        self.teams[team_id].tier = Tier.PAID
        self.teams[team_id].billing_info = {"stripe_customer_id": "example_customer_id"}

    def get_team_billing_info(self, team_id: int) -> Dict[str, str]:
        if team_id not in self.teams:
            raise ValueError("Team not found")
        return self.teams[team_id].billing_info

    def handle_stripe_webhook(self, event: Dict[str, str]):
        if event["type"] == "invoice.payment_succeeded":
            team_id = int(event["metadata"]["team_id"])
            self.teams[team_id].billing_info["payment_status"] = "paid"

    def get_paid_tier_price(self) -> int:
        return 49
