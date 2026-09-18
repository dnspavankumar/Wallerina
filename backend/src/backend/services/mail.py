"""Transactional mail via SMTP.

Any provider works through this module; the default is Gmail, which needs no
domain verification and delivers to any recipient once the sending account
has an App Password — unlike Resend's, Mailgun's or SendGrid's sandbox
modes, which only deliver to a pre-authorized address until a domain is
verified. This is deliberately the only mail Wallerina sends today: a copy
of a draft-swaps plan to the address the user typed in.
"""

from __future__ import annotations

import asyncio
import re
import smtplib
from decimal import Decimal
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from backend.core.config import get_settings
from backend.models.execution import ExecutionLeg, ExecutionPlan

_RISK_PATTERN = re.compile(r"carries\s+([\d.]+)\s*%\s+of\s+portfolio\s+risk", re.IGNORECASE)


class MailUnavailable(RuntimeError):
    """No SMTP credentials are configured. The message is safe to show to the user."""


class MailSendError(RuntimeError):
    """The SMTP server rejected the message or the connection failed."""


def _risk_share(leg: ExecutionLeg) -> float:
    """The risk-contribution percentage embedded in a leg's reason text, or -1 if absent."""
    match = _RISK_PATTERN.search(leg.reason)
    return float(match.group(1)) if match else -1.0


def _token_amount(units: str, decimals: int) -> str:
    scale = Decimal(10) ** decimals
    value = Decimal(units) / scale
    return f"{value.normalize():f}" if value == value.to_integral_value() else f"{value:.6f}".rstrip("0").rstrip(".")


def _legs_by_risk(plan: ExecutionPlan) -> list[ExecutionLeg]:
    return sorted(plan.legs, key=_risk_share, reverse=True)


def _rows_html(legs: list[ExecutionLeg]) -> str:
    rows = []
    for leg in legs:
        amount = _token_amount(leg.sell_amount, leg.sell_decimals)
        rows.append(
            "<tr>"
            f"<td style='padding:8px;border-bottom:1px solid #333'>{leg.chain}</td>"
            f"<td style='padding:8px;border-bottom:1px solid #333'>{amount} {leg.sell_symbol}</td>"
            f"<td style='padding:8px;border-bottom:1px solid #333;text-align:right'>${leg.sell_value_usd:,.0f}</td>"
            f"<td style='padding:8px;border-bottom:1px solid #333'>{leg.buy_symbol}</td>"
            f"<td style='padding:8px;border-bottom:1px solid #333'>{leg.reason}</td>"
            "</tr>"
        )
    return "".join(rows)


def _rows_text(legs: list[ExecutionLeg]) -> str:
    lines = []
    for leg in legs:
        amount = _token_amount(leg.sell_amount, leg.sell_decimals)
        lines.append(
            f"- {leg.chain}: sell {amount} {leg.sell_symbol} (${leg.sell_value_usd:,.0f}) "
            f"into {leg.buy_symbol} — {leg.reason}"
        )
    return "\n".join(lines)


def _render(plan: ExecutionPlan) -> tuple[str, str]:
    legs = _legs_by_risk(plan)
    total = sum(leg.sell_value_usd for leg in plan.legs)

    html = f"""
    <div style="font-family:sans-serif;background:#0a0a0a;color:#eee;padding:24px">
      <p style="letter-spacing:0.1em;text-transform:uppercase;font-size:11px;color:#999">Draft swaps</p>
      <h2 style="font-weight:300">{plan.address}</h2>
      <p style="color:#aaa;font-size:13px">
        Goal: {plan.goal} &middot; {len(legs)} swap(s) drafted &middot; ${total:,.0f} total &middot;
        sorted by share of portfolio risk
      </p>
      <table style="width:100%;border-collapse:collapse;font-size:13px;margin-top:12px">
        <thead>
          <tr style="text-align:left;color:#999;font-size:11px;text-transform:uppercase">
            <th style="padding:8px">Network</th><th style="padding:8px">Sell</th>
            <th style="padding:8px;text-align:right">Value</th><th style="padding:8px">Swap into</th>
            <th style="padding:8px">Why</th>
          </tr>
        </thead>
        <tbody>{_rows_html(legs)}</tbody>
      </table>
      <p style="color:#666;font-size:11px;margin-top:20px">
        Drafts only. Wallerina never signs, sends or executes anything.
      </p>
    </div>
    """

    text = (
        f"Draft swaps for {plan.address}\n"
        f"Goal: {plan.goal} | {len(legs)} swap(s) | ${total:,.0f} total | sorted by share of portfolio risk\n\n"
        f"{_rows_text(legs)}\n\n"
        "Drafts only. Wallerina never signs, sends or executes anything."
    )

    return html, text


def _send_sync(*, host: str, port: int, username: str, password: str, sender: str, to: str, subject: str, html: str, text: str) -> None:
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = to
    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(html, "html"))

    with smtplib.SMTP(host, port, timeout=15) as server:
        server.starttls()
        server.login(username, password)
        server.sendmail(sender, [to], message.as_string())


async def send_draft_plan(to: str, plan: ExecutionPlan) -> None:
    settings = get_settings()
    if not settings.smtp_username or not settings.smtp_password:
        raise MailUnavailable(
            "Email needs SMTP_USERNAME and SMTP_PASSWORD on the backend "
            "(a Gmail address and an App Password from https://myaccount.google.com/apppasswords)."
        )

    html, text = _render(plan)
    subject = f"Wallerina draft swaps — {plan.address[:6]}…{plan.address[-4:]}"

    try:
        await asyncio.to_thread(
            _send_sync,
            host=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_username,
            password=settings.smtp_password,
            sender=settings.smtp_from_email or settings.smtp_username,
            to=to,
            subject=subject,
            html=html,
            text=text,
        )
    except smtplib.SMTPException as error:
        raise MailSendError(f"smtp: {error}") from error
    except OSError as error:
        raise MailSendError(f"smtp: could not reach {settings.smtp_host}:{settings.smtp_port} ({error})") from error
