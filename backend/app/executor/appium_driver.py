"""AppiumDriver — context manager wrapping an Appium session.

Provides a clean lifecycle: create session on enter, quit session on
exit. Configuration is pulled from the Flask app config.
"""

from typing import Optional
from appium import webdriver
from appium.webdriver.appium_service import AppiumService


class AppiumDriver:
    """Context manager for an Appium WebDriver session.

    Usage::

        with AppiumDriver(udid="...", platform="android") as driver:
            driver.find_element(...)
    """

    def __init__(
        self,
        udid: str,
        platform: str,
        appium_host: str = "127.0.0.1",
        appium_port: int = 4723,
        **desired_caps,
    ):
        """Initialise AppiumDriver parameters.

        Args:
            udid: Device UDID / serial number.
            platform: "android" or "ios".
            appium_host: Appium server hostname.
            appium_port: Appium server port.
            **desired_caps: Additional desired capabilities.
        """
        # TODO: Store constructor args
        #   self.udid = udid
        #   self.platform = platform
        #   self.host = appium_host
        #   self.port = appium_port
        #   self.extra_caps = desired_caps
        #   self.driver: WebDriver | None = None
        self._service: Optional[AppiumService] = None

    def __enter__(self):
        """Create the Appium session and return the WebDriver instance.

        Returns:
            appium.webdriver.WebDriver (Remote instance).
        """
        # TODO: Implement __enter__
        #   - Build desired_caps dict
        #   - For Android: platformName, udid, automationName=UiAutomator2, ...
        #   - For iOS: platformName, udid, automationName=XCUITest, ...
        #   - self.driver = webdriver.Remote(f"http://{host}:{port}", caps)
        #   - Return self.driver
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Quit the Appium session gracefully.

        Ensures the WebDriver session is terminated even if an
        exception occurred during execution.
        """
        # TODO: Implement __exit__
        #   - If self.driver is not None: self.driver.quit()
        #   - self.driver = None
        pass
