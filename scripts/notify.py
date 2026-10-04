"""Send a phone push (ntfy) and/or an email. Configure in .env or GitHub secrets.

  NTFY_TOPIC      a long, hard-to-guess topic name you subscribe to in the ntfy app
  SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD   the account that SENDS the email
  ALERT_EMAIL_TO  where alerts go

Test: python scripts/notify.py --test
"""
from __future__ import annotations

import os
import smtplib
import sys
from email.message import EmailMessage

import common  # noqa: F401  (loads .env)


def send(title: str, body: str, urgent: bool = False) -> list[str]:
    sent = []
    topic = os.getenv("NTFY_TOPIC")
    if topic:
        import requests

        server = os.getenv("NTFY_SERVER", "https://ntfy.sh")
        r = requests.post(
            f"{server}/{topic}",
            data=body.encode("utf-8"),
            headers={"Title": title.encode("ascii", "ignore").decode(), "Priority": "high" if urgent else "default"},
            timeout=20,
        )
        if r.ok:
            sent.append("push")
        else:
            print(f"Push failed: {r.status_code} {r.text[:200]}")

    host, to = os.getenv("SMTP_HOST"), os.getenv("ALERT_EMAIL_TO")
    if host and to:
        msg = EmailMessage()
        msg["Subject"], msg["From"], msg["To"] = title, os.getenv("SMTP_USER"), to
        msg.set_content(body)
        try:
            with smtplib.SMTP(host, int(os.getenv("SMTP_PORT", "587")), timeout=30) as s:
                s.starttls()
                s.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))
                s.send_message(msg)
            sent.append("email")
        except Exception as e:
            print(f"Email failed: {e}")

    if not sent:
        print(f"[no notification channel worked or none set up]\n{title}\n{body}")
    return sent


if __name__ == "__main__":
    if "--test" in sys.argv:
        print("Sent via:", send("Trading Agent test", "If you can read this, alerts work.") or "nothing")
