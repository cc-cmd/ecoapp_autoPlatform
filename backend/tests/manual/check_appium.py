"""Manual Appium connectivity check script.

Run this script to verify that the Appium server is reachable and can
communicate with connected devices.

Usage:
    python tests/manual/check_appium.py

Environment variables (or edit defaults below):
    APPIUM_HOST  (default: 127.0.0.1)
    APPIUM_PORT  (default: 4723)

The script will:
  1. Ping the Appium server status endpoint.
  2. List available devices / sessions.
  3. Attempt to create a short-lived session on the first available
     device (optional, requires a device to be connected).
"""

import os
import sys
from urllib import request, error
import json


APPIUM_HOST = os.getenv("APPIUM_HOST", "127.0.0.1")
APPIUM_PORT = int(os.getenv("APPIUM_PORT", "4723"))
BASE_URL = f"http://{APPIUM_HOST}:{APPIUM_PORT}"


def check_server_status() -> bool:
    """Check if the Appium server is running.

    Returns:
        True if the server responds with a 200 status.
    """
    # TODO: Implement server status check
    #   url = f"{BASE_URL}/wd/hub/status"
    #   resp = request.urlopen(url, timeout=5)
    #   data = json.loads(resp.read())
    #   print(f"Server status: {data.get('value', {}).get('message', 'unknown')}")
    #   return True
    print("Checking Appium server status...")
    return False


def list_sessions() -> list[dict]:
    """List active Appium sessions.

    Returns:
        List of session info dicts.
    """
    # TODO: Implement session listing
    #   url = f"{BASE_URL}/wd/hub/sessions"
    #   resp = request.urlopen(url, timeout=5)
    #   data = json.loads(resp.read())
    #   return data.get("value", [])
    print("Listing active sessions...")
    return []


def check_device_connectivity(platform: str = "android") -> bool:
    """Attempt to create and quit a short-lived session.

    Args:
        platform: "android" or "ios".

    Returns:
        True if session was created and quit successfully.
    """
    # TODO: Implement connectivity test
    #   - Build desired capabilities for the given platform
    #   - Use appium.webdriver.Remote to create a session
    #   - Print device info
    #   - Quit the session
    #   - Return True on success
    print(f"Checking {platform} device connectivity...")
    return False


def main():
    """Run all connectivity checks."""
    print(f"Connecting to Appium at {BASE_URL}")
    print("=" * 50)

    # Check 1: Server status
    if not check_server_status():
        print("[FAIL] Appium server is not reachable.")
        print(f"  Make sure Appium is running: appium --address {APPIUM_HOST} --port {APPIUM_PORT}")
        sys.exit(1)
    print("[PASS] Appium server is running.")

    # Check 2: Active sessions
    sessions = list_sessions()
    print(f"  Active sessions: {len(sessions)}")

    # Check 3: Device connectivity (optional, uncomment to run)
    # check_device_connectivity("android")
    # check_device_connectivity("ios")

    print("=" * 50)
    print("All checks completed.")


if __name__ == "__main__":
    main()
