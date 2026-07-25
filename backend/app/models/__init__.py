"""SQLAlchemy model imports.

Import all models here so that Alembic's env.py can do a single
``from app.models import *`` to auto-discover tables.
"""

from .user import User
from .category import Category
from .test_case import TestCase
from .device import Device
from .run_group import RunGroup
from .test_run import TestRun

__all__ = [
    "User",
    "Category",
    "TestCase",
    "Device",
    "RunGroup",
    "TestRun",
]
