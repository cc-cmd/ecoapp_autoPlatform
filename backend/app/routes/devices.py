"""Device management routes.

All endpoints require JWT authentication (``@jwt_required()``).

Endpoints:
  - GET  /api/devices          - List all discovered devices.
  - POST /api/devices/discover - Trigger device discovery (ADB / iOS tools).
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

devices_bp = Blueprint("devices", __name__)


@devices_bp.route("/", methods=["GET"])
@devices_bp.route("", methods=["GET"])
@jwt_required()
def list_devices():
    """List all known devices.

    Query parameters:
        platform (str, optional) — filter by platform ("android" / "ios")
        status (str, optional)   — filter by status ("online" / "busy" / "offline")

    Responses:
        200 → { devices: [...] }
    """
    # TODO: Implement device listing
    #   - Read optional query filters
    #   - Call device_service.list_devices(...)
    #   - Return device list
    return jsonify({"error": "Not implemented"}), 501


@devices_bp.route("/discover", methods=["POST"])
@jwt_required()
def discover_devices():
    """Trigger device discovery.

    Scans connected devices via ADB (Android) and iOS device tools.
    New devices are created, existing ones are updated with fresh
    metadata and their heartbeat is refreshed.

    Responses:
        200 → { message: "Discovery complete", devices: [...] }
    """
    # TODO: Implement device discovery
    #   - Call device_service.discover()
    #   - Return discovered/updated devices
    return jsonify({"error": "Not implemented"}), 501
