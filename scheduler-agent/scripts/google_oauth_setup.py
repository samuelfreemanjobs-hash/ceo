#!/usr/bin/env python3
"""
google_oauth_setup.py
=====================
Obtain a Google OAuth refresh token for Scheduler Agent Calendar access.

Usage:
    pip install google-auth-oauthlib google-api-python-client
    export GOOGLE_OAUTH_CLIENT_ID=...
    export GOOGLE_OAUTH_CLIENT_SECRET=...
    python scripts/google_oauth_setup.py

Opens a browser for consent (or prints URL in headless env).
Prints refresh token — store securely; set GOOGLE_REFRESH_TOKEN for dev.
"""

from __future__ import annotations

import os
import sys

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main() -> int:
    client_id = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    if not client_id or not client_secret:
        print(
            "Set GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET.",
            file=sys.stderr,
        )
        return 1

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        print(
            "pip install google-auth-oauthlib google-api-python-client",
            file=sys.stderr,
        )
        return 1

    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    }

    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    creds = flow.run_local_server(port=0)

    print("\n--- OAuth success ---")
    print(f"Refresh token (store securely):\n{creds.refresh_token}\n")
    print("Dev env:")
    print(f"  export GOOGLE_REFRESH_TOKEN='{creds.refresh_token}'")
    print("\nProduction: store per user_id in your secrets store.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
