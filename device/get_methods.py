import logging
import device.utils as utils

class GetMethods:
    def __init__(self, device, constants):
        self.device = device
        self.constants = constants

    def get_data(self):
        """Retrieve data from the device."""
        try:
            self.device.send_control_transfer(self.constants['BM_REQUEST_TYPE_OUT'], self.constants['B_REQUEST'], self.constants['W_VALUE'], self.constants['W_INDEX'], [0xC0, 0xA5, 0xA3])
            response = self.device.send_control_transfer(self.constants['BM_REQUEST_TYPE_IN'], self.constants['B_REQUEST_GET'], self.constants['W_VALUE'], self.constants['W_INDEX'], self.constants['DATA_LENGTH'])
            logging.info("Data retrieved from device.")
            print(response)
            return response
        except IOError:
            logging.error("Failed to retrieve data from the device.")
            return []

    def get_current_volume(self):
        """Get the current volume from the device."""
        try:
            self.device.refresh_volume()
            response = self.device.send_control_transfer(self.constants['BM_REQUEST_TYPE_IN'], self.constants['B_REQUEST_GET'], self.constants['W_VALUE'], self.constants['W_INDEX'], self.constants['DATA_LENGTH'])
            volume_value = response[4]
            self.device.volume = volume_value
            percent_volume = utils.convert_volume_to_percent(volume_value)
            logging.info(f"Current volume is {percent_volume}%.")
            return percent_volume
        except IOError:
            logging.error("Failed to get current volume.")
            return None

    def get_current_led_status(self):
        """Get the current LED status."""
        data = self.get_data()
        if data:
            led_status = utils.convert_led_status_to_string(data[5])
            self.device.led_status = led_status
            logging.info(f"Current LED status: {led_status}.")
            return led_status
        return None

    def get_gain(self):
        """Get the current gain."""
        data = self.get_data()
        if data:
            gain = utils.convert_gain_to_string(int(data[4]))
            self.device.current_gain = gain
            logging.info(f"Current gain: {gain}.")
            return gain
        return None

    def get_filter(self):
        """Get the current filter type."""
        data = self.get_data()
        if data:
            filter_type = utils.convert_filter_payload_to_string(data[3])
            logging.info(f"Current filter type: {filter_type}.")
            return filter_type
        return None
