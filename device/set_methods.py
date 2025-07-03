import logging
from typing import List, Optional, Any, Dict
import device.utils as utils


class SetMethods:
    """Class for handling set operations on the Moondrop device."""

    def __init__(self, device: Any, constants: Dict[str, Any]) -> None:
        """Initialize the SetMethods class.

        Args:
            device: The Moondrop device instance.
            constants: Dictionary of constant values used for device communication.
        """
        self.device = device
        self.constants = constants

    def refresh_volume(self) -> Optional[List[int]]:
        """Refresh the volume settings.

        Returns:
            The response from the device, or None if failed.
        """
        try:
            response = self.device.send_control_transfer(
                self.constants['BM_REQUEST_TYPE_OUT'],
                self.constants['B_REQUEST'],
                self.constants['W_VALUE'],
                self.constants['W_INDEX'],
                self.constants['VOLUME_REFRESH_DATA']
            )
            logging.info("Volume refreshed.")
            return response
        except IOError:
            logging.error("Failed to refresh volume.")
            return None

    def set_volume(self, volume: int) -> bool:
        """Set the device volume.

        Args:
            volume: The volume level to set (0-60).

        Returns:
            True if successful, False otherwise.
        """
        data = [192, 165, 4, utils.convert_volume_to_payload(volume)]
        try:
            self.device.send_control_transfer(
                self.constants['BM_REQUEST_TYPE_OUT'],
                self.constants['B_REQUEST'],
                self.constants['W_VALUE'],
                self.constants['W_INDEX'],
                data
            )
            self.device.volume = volume
            self.refresh_volume()
            logging.info(f"Volume set to {volume}.")
            return True
        except IOError:
            logging.error("Failed to set volume.")
            return False

    def set_gain(self, gain: str) -> bool:
        """Set the device gain.

        Args:
            gain: The gain setting to set ("Low" or "High").

        Returns:
            True if successful, False otherwise.
        """
        gain = utils.convert_gain_to_payload(gain)
        data = [192, 165, 2, gain]
        try:
            self.device.send_control_transfer(
                self.constants['BM_REQUEST_TYPE_OUT'],
                self.constants['B_REQUEST'],
                self.constants['W_VALUE'],
                self.constants['W_INDEX'],
                data
            )
            self.device.current_gain = gain
            self.refresh_volume()
            logging.info(f"Gain set to {gain}.")
            return True
        except IOError:
            logging.error("Failed to set gain.")
            return False

    def set_led_status(self, status: str) -> bool:
        """Set the LED status.

        Args:
            status: The LED status to set ("On", "Temporarily Off", or "Off").

        Returns:
            True if successful, False otherwise.
        """
        status = utils.convert_led_status_to_payload(status)
        data = [192, 165, 6, status]
        try:
            self.device.send_control_transfer(
                self.constants['BM_REQUEST_TYPE_OUT'],
                self.constants['B_REQUEST'],
                self.constants['W_VALUE'],
                self.constants['W_INDEX'],
                data
            )
            self.device.led_status = status
            logging.info(f"LED status set to {status}.")
            return True
        except IOError:
            logging.error("Failed to set LED status.")
            return False

    def set_filter(self, filter_type: str) -> bool:
        """Set the filter type.

        Args:
            filter_type: The filter type to set.

        Returns:
            True if successful, False otherwise.
        """
        filter_type = utils.convert_filter_to_payload(filter_type)
        data = [192, 165, 1, filter_type]
        try:
            self.device.send_control_transfer(
                self.constants['BM_REQUEST_TYPE_OUT'],
                self.constants['B_REQUEST'],
                self.constants['W_VALUE'],
                self.constants['W_INDEX'],
                data
            )
            self.device.current_filter = filter_type
            logging.info(f"Filter set to {filter_type}.")
            return True
        except IOError:
            logging.error("Failed to set filter.")
            return False
