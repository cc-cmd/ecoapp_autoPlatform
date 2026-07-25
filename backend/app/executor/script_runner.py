"""ScriptRunner — loads and executes individual test scripts.

Each test script is a Python file expected to define a ``run``
function that accepts a driver instance and a log callback.

Example script structure::

    def run(driver, log):
        log("Starting test step 1")
        driver.find_element(...)
        log("Step 1 complete")
        # Return True for pass, False for fail
        return True
"""

from dataclasses import dataclass, field
from typing import Callable, Optional
from types import ModuleType


@dataclass
class ScriptResult:
    """Result of executing a single test script.

    Attributes:
        passed: Whether the script indicated success.
        error_message: Error message if an exception occurred.
        log_lines: Collected log lines during execution.
    """

    passed: bool = False
    error_message: Optional[str] = None
    log_lines: list[str] = field(default_factory=list)


class ScriptRunner:
    """Loads and runs an individual test script.

    The script is loaded as a Python module, and its ``run`` function
    is called with the Appium driver and a logger callback.
    """

    def __init__(self):
        pass

    def run(
        self,
        script_path: str,
        driver,
        log_callback: Callable[[str], None],
    ) -> ScriptResult:
        """Execute a test script.

        Args:
            script_path: Absolute filesystem path to the Python script.
            driver: Appium WebDriver instance for the allocated device.
            log_callback: Function to call with each log line.

        Returns:
            ScriptResult summarising the execution outcome.
        """
        # TODO: Implement script execution
        #   - Read script content from disk
        #   - Compile and exec in an isolated namespace
        #   - Extract `run` function
        #   - Call run(driver, log_callback)
        #   - Catch all exceptions and return ScriptResult(passed=False, ...)
        #   - Return ScriptResult based on run() return value
        raise NotImplementedError

    def _load_script(self, script_path: str) -> ModuleType:
        """Load a Python script as a module.

        Uses ``importlib`` machinery to load the script from a file
        path into a fresh module object, avoiding sys.path pollution.

        Args:
            script_path: Absolute path to the .py file.

        Returns:
            ModuleType instance with the script's code.

        Raises:
            ScriptLoadError: If the file cannot be read or compiled.
        """
        # TODO: Implement script loading
        #   - Read file, compile, exec in new module
        #   - Return module
        raise NotImplementedError
