"""Executor package.

Manages Appium-driven test execution: queue consumption, device
allocation, Appium session lifecycle, and script running.
"""

from .executor_service import ExecutorService
from .queue import ExecutionQueue
from .device_allocator import DeviceAllocator
from .appium_driver import AppiumDriver
from .script_runner import ScriptRunner, ScriptResult

__all__ = [
    "ExecutorService",
    "ExecutionQueue",
    "DeviceAllocator",
    "AppiumDriver",
    "ScriptRunner",
    "ScriptResult",
]
