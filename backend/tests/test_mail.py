"""Mail: risk-based ordering and the guard when SMTP is unconfigured."""

from __future__ import annotations

import pytest

from backend.models.execution import ExecutionLeg, ExecutionPlan
from backend.services import mail

ADDRESS = "0x8ba1f109551bd432803012645ac136ddd64dba7"
TOKEN = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"


def leg(symbol, reason, leg_id):
    return ExecutionLeg(
        id=leg_id,
        network="eth-mainnet",
        chain="Ethereum",
        chain_id=1,
        sell_symbol=symbol,
        sell_token=TOKEN,
        sell_decimals=18,
        sell_amount="1000000000000000000",
        sell_value_usd=100.0,
        buy_symbol="USDC",
        buy_token=TOKEN,
        buy_decimals=6,
        reason=reason,
    )


def plan(legs):
    return ExecutionPlan(
        address=ADDRESS,
        generated_at="2026-09-18T12:34:00Z",
        goal="balanced",
        target_stablecoin_ratio=0.5,
        current_stablecoin_ratio=0.1,
        rebalance_required=True,
        legs=legs,
        skipped=[],
        slippage_bps=100,
        swaps_configured=True,
    )


class TestRiskOrdering:
    def test_sorts_highest_risk_share_first(self):
        legs = [
            leg("ETH", "Carries 20% of portfolio risk at 41% weight", "a"),
            leg("TRUE", "Carries 80% of portfolio risk at 38% weight", "b"),
        ]
        ordered = mail._legs_by_risk(plan(legs))
        assert [item.sell_symbol for item in ordered] == ["TRUE", "ETH"]

    def test_legs_without_a_risk_share_sort_last(self):
        legs = [
            leg("XYZ", "New position, no risk history yet", "a"),
            leg("ETH", "Carries 20% of portfolio risk at 41% weight", "b"),
        ]
        ordered = mail._legs_by_risk(plan(legs))
        assert [item.sell_symbol for item in ordered] == ["ETH", "XYZ"]


class TestSendDraftPlan:
    async def test_raises_when_unconfigured(self, monkeypatch):
        monkeypatch.setenv("SMTP_USERNAME", "")
        monkeypatch.setenv("SMTP_PASSWORD", "")
        mail.get_settings.cache_clear()
        with pytest.raises(mail.MailUnavailable):
            await mail.send_draft_plan("user@example.com", plan([]))
        mail.get_settings.cache_clear()
