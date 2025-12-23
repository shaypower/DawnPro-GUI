import usb.core
import time
import logging
from typing import Dict, Any, Optional, List
from device.get_methods import GetMethods
from device.set_methods import SetMethods
from device.config import AppConfig


class Moondrop:
    """Main class for interacting with the Moondrop Dawn Pro device."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize the Moondrop device connection and settings.

        Args:
            config: Application configuration instance.
        """
        self.volume = 0
        self.led_status = config.device_constants.LED_STATUS_OFF
        self.current_filter = 'low'
        self.current_gain = 'low'
        self.device = usb.core.find(
            idVendor=config.device_identifiers.MOONDROP_VID,
            idProduct=config.device_identifiers.DAWN_PRO_PID
        )

        if self.device is None:
            raise ValueError("Device not found")
        logging.info("Device found and initialized.")

        self.constants = config.get_constants_dict()
        self.getter = GetMethods(self, self.constants)
        self.setter = SetMethods(self, self.constants)

    def send_control_transfer(
        self,
        bmRequestType: int,
        bRequest: int,
        wValue: int,
        wIndex: int,
        data_or_length: List[int]
    ) -> List[int]:
        """Send a control transfer to the USB device.

        Args:
            bmRequestType: The request type.
            bRequest: The request number.
            wValue: The value field.
            wIndex: The index field.
            data_or_length: The data to send or length to receive.

        Returns:
            The response data from the device.

        Raises:
            IOError: If the USB control transfer fails.
        """
        try:
            time.sleep(0.1)
            return self.device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, data_or_length)
        except usb.core.USBError as error:
            logging.error(f"USB control transfer failed: {error}")
            raise IOError(f"USB control transfer failed: {error}") from error

    def refresh_volume(self) -> Optional[List[int]]:
        """Refresh the volume settings.

        Returns:
            The response from the device, or None if failed.
        """
        return self.setter.refresh_volume()

    def set_volume(self, volume: int) -> bool:
        """Set the device volume.

        Args:
            volume: The volume level to set (0-60).

        Returns:
            True if successful, False otherwise.
        """
        return self.setter.set_volume(volume)

    def get_current_volume(self) -> Optional[int]:
        """Get the current volume level.

        Returns:
            The current volume level (0-60) or None if failed.
        """
        return self.getter.get_current_volume()

    def get_current_led_status(self) -> Optional[str]:
        """Get the current LED status.

        Returns:
            The current LED status or None if failed.
        """
        return self.getter.get_current_led_status()

    def get_gain(self) -> Optional[str]:
        """Get the current gain setting.

        Returns:
            The current gain setting or None if failed.
        """
        return self.getter.get_gain()

    def get_filter(self) -> Optional[str]:
        """Get the current filter setting.

        Returns:
            The current filter setting or None if failed.
        """
        return self.getter.get_filter()

    def set_led_status(self, status: str) -> bool:
        """Set the LED status.

        Args:
            status: The LED status to set.

        Returns:
            True if successful, False otherwise.
        """
        return self.setter.set_led_status(status)

    def set_filter(self, filter_type: str) -> bool:
        """Set the filter type.

        Args:
            filter_type: The filter type to set.

        Returns:
            True if successful, False otherwise.
        """
        return self.setter.set_filter(filter_type)

    def set_gain(self, status: str) -> bool:
        """Set the gain setting.

        Args:
            status: The gain setting to set.

        Returns:
            True if successful, False otherwise.
        """
        return self.setter.set_gain(status)

