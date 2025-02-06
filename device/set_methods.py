import logging
import device.utils as utils

class SetMethods:
    def __init__(self, device, constants):
        self.device = device
        self.constants = constants

    def refresh_volume(self):
        """Refresh the volume."""
        try:
            response = self.device.send_control_transfer(self.constants['BM_REQUEST_TYPE_OUT'], self.constants['B_REQUEST'], self.constants['W_VALUE'], self.constants['W_INDEX'], self.constants['VOLUME_REFRESH_DATA'])
            logging.info("Volume refreshed.")
            return response
        except IOError:
            logging.error("Failed to refresh volume.")
            return None

    def set_volume(self, volume):
        """Set the device volume."""
        data = [192, 165, 4, utils.convert_volume_to_payload(volume)]
        try:
            self.device.send_control_transfer(self.constants['BM_REQUEST_TYPE_OUT'], self.constants['B_REQUEST'], self.constants['W_VALUE'], self.constants['W_INDEX'], data)
            self.device.volume = volume
            self.refresh_volume()
            logging.info(f"Volume set to {volume}.")
            return True
        except IOError:
            logging.error("Failed to set volume.")
            return False

    def set_gain(self, gain):
        """Set the device gain."""
        gain = utils.convert_gain_to_payload(gain)
        data = [192, 165, 2, gain]
        try:
            self.device.send_control_transfer(self.constants['BM_REQUEST_TYPE_OUT'], self.constants['B_REQUEST'], self.constants['W_VALUE'], self.constants['W_INDEX'], data)
            self.device.current_gain = gain
            self.refresh_volume()
            logging.info(f"Gain set to {gain}.")
            return True
        except IOError:
            logging.error("Failed to set gain.")
            return False

    def set_led_status(self, status):
        """Set the LED status."""
        status = utils.convert_led_status_to_payload(status)
        data = [192, 165, 6, status]
        try:
            self.device.send_control_transfer(self.constants['BM_REQUEST_TYPE_OUT'], self.constants['B_REQUEST'], self.constants['W_VALUE'], self.constants['W_INDEX'], data)
            self.device.led_status = status
            logging.info(f"LED status set to {status}.")
            return True
        except IOError:
            logging.error("Failed to set LED status.")
            return False

    def set_filter(self, filter_type):
        filter_type = utils.convert_filter_to_payload(filter_type)
        data = [192, 165, 1, filter_type]
        try:
            self.device.send_control_transfer(self.constants['BM_REQUEST_TYPE_OUT'], self.constants['B_REQUEST'], self.constants['W_VALUE'], self.constants['W_INDEX'], data)
            self.device.current_filter = filter_type
            logging.info(f"Filter set to {filter_type}.")
            return True
        except IOError:
            logging.error("Failed to set filter.")
            return False
