import logging
from typing import List, Optional, Any, Dict
import device.utils as utils


class GetMethods:
    """Class for handling get operations on the Moondrop device."""

    def __init__(self, device: Any, constants: Dict[str, Any]) -> None:
        """Initialize the GetMethods class.

        Args:
            device: The Moondrop device instance.
            constants: Dictionary of constant values used for device communication.
        """
        self.device = device
        self.constants = constants

    def get_data(self) -> List[int]:
        """Retrieve data from the device.
        
        Sends command [0xC0, 0xA5, 0xA3] to request device settings.
        Returns a 7-byte response where:
        - data[3] = filter type
        - data[4] = gain setting
        - data[5] = LED status

        Returns:
            List of integers containing the device data, or empty list if failed.
        """
        try:
            self.device.send_control_transfer(
                self.constants['BM_REQUEST_TYPE_OUT'],
                self.constants['B_REQUEST'],
                self.constants['W_VALUE'],
                self.constants['W_INDEX'],
                [0xC0, 0xA5, 0xA3]
            )
            response = self.device.send_control_transfer(
                self.constants['BM_REQUEST_TYPE_IN'],
                self.constants['B_REQUEST_GET'],
                self.constants['W_VALUE'],
                self.constants['W_INDEX'],
                self.constants['DATA_LENGTH']
            )
            logging.info(f"Data retrieved from device: {response}")
            return response
        except IOError:
            logging.error("Failed to retrieve data from the device.")
            return []

    def get_current_volume(self) -> Optional[int]:
        """Get the current volume from the device.
        
        Sends volume refresh command [0xC0, 0xA5, 0xA2] then reads response.
        Note: This uses a different command than get_data(), so the response
        structure may differ. Volume is read from response[4].

        Returns:
            The current volume as a percentage (0-60), or None if failed.
        """
        try:
            self.device.refresh_volume()
            response = self.device.send_control_transfer(
                self.constants['BM_REQUEST_TYPE_IN'],
                self.constants['B_REQUEST_GET'],
                self.constants['W_VALUE'],
                self.constants['W_INDEX'],
                self.constants['DATA_LENGTH']
            )
            volume_value = response[4]
            self.device.volume = volume_value
            percent_volume = utils.convert_volume_to_percent(volume_value)
            logging.info(f"Current volume is {percent_volume}%.")
            return percent_volume
        except IOError:
            logging.error("Failed to get current volume.")
            return None

    def get_current_led_status(self) -> Optional[str]:
        """Get the current LED status.

        Returns:
            The current LED status as a string, or None if failed.
        """
        data = self.get_data()
        if data:
            led_status = utils.convert_led_status_to_string(data[5])
            self.device.led_status = led_status
            logging.info(f"Current LED status: {led_status}.")
            return led_status
        return None

    def get_gain(self) -> Optional[str]:
        """Get the current gain setting.

        Returns:
            The current gain setting as a string, or None if failed.
        """
        data = self.get_data()
        if data:
            gain = utils.convert_gain_to_string(int(data[4]))
            self.device.current_gain = gain
            logging.info(f"Current gain: {gain}.")
            return gain
        return None

    def get_filter(self) -> Optional[str]:
        """Get the current filter type.

        Returns:
            The current filter type as a string, or None if failed.
        """
        data = self.get_data()
        if data:
            filter_type = utils.convert_filter_payload_to_string(data[3])
            logging.info(f"Current filter type: {filter_type}.")
            return filter_type
        return None
