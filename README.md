# Apple Silicon Coder

A Python project for managing teams and their billing information.

## Usage

1. Create a team: `coder.create_team(1)`
2. Upgrade a team to paid tier: `coder.upgrade_to_paid(1)`
3. Get team billing information: `coder.get_team_billing_info(1)`
4. Handle Stripe webhook: `coder.handle_stripe_webhook(event)`
5. Get paid tier price: `coder.get_paid_tier_price()`
