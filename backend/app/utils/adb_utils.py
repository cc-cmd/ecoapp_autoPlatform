"""Device discovery utilities.

Provides functions to discover connected Android and iOS devices
via ADB and platform-specific iOS tools.
"""

import subprocess
import re
from dataclasses import dataclass, field


@dataclass
class DiscoveredDevice:
    """Information about a discovered test device.

    Attributes:
        udid: Unique device identifier (serial / UUID).
        device_name: Human-readable device name.
        platform: "android" or "ios".
        model: Device model (e.g. "Pixel 7", "iPhone 15 Pro").
        os_version: OS version string.
    """

    udid: str
    device_name: str
    platform: str
    model: str = ""
    os_version: str = ""


def list_android_devices() -> list[DiscoveredDevice]:
    """Discover Android devices connected via ADB.

    Runs ``adb devices -l`` and parses the output to extract device
    information. Returns both physical devices and emulators.

    Returns:
        List of DiscoveredDevice instances for connected Android devices.
    """
    # TODO: Implement Android device discovery
    #   - Run: adb devices -l
    #   - Parse lines matching: <udid> device <props>
    #   - For each device, optionally run:
    #       adb -s <udid> shell getprop ro.product.model
    #       adb -s <udid> shell getprop ro.build.version.release
    #   - Build DiscoveredDevice instances
    ...
    return []


def list_ios_devices() -> list[DiscoveredDevice]:
    """Discover iOS devices connected to the host.

    Uses ``idevice_id -l`` (libimobiledevice) to list connected iOS
    device UDIDs, then queries device info via ``ideviceinfo``.

    Falls back gracefully if the iOS tools are not installed.

    Returns:
        List of DiscoveredDevice instances for connected iOS devices.
    """
    # TODO: Implement iOS device discovery
    #   - Check if idevice_id is available
    #   - Run: idevice_id -l
    #   - For each UDID, run ideviceinfo to get name/version/model
    #   - Build DiscoveredDevice instances
    ...
    return []


def _run_adb_command(args: list[str], timeout: int = 10) -> str:
    """Run an ADB command and return stdout.

    Args:
        args: ADB arguments (e.g. ["devices", "-l"]).
        timeout: Command timeout in seconds.

    Returns:
        Command stdout as a string.

    Raises:
        RuntimeError: If the command fails or ADB is not found.
    """
    # TODO: Implement ADB command runner
    #   - cmd = ["adb"] + args
    #   - result = subprocess.run(cmd, capture_output=True, timeout=timeout)
    #   - if result.returncode != 0: raise RuntimeError(...)
    #   - return result.stdout.decode()
    raise NotImplementedError
