import usb.core
import time
import logging
from device.get_methods import GetMethods
from device.set_methods import SetMethods


BM_REQUEST_TYPE_OUT = 0x43
BM_REQUEST_TYPE_IN = 0xc3
B_REQUEST = 160
B_REQUEST_GET = 161
W_VALUE = 0x0000
W_INDEX = 0x09a0
VOLUME_REFRESH_DATA = [0xC0, 0xA5, 0xA2]
DATA_LENGTH = 7
LED_STATUS_ENABLED = 0
LED_STATUS_TEMP_OFF = 1
LED_STATUS_OFF = 2


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Moondrop:
    MOONDROP_VID = 0x2fc6
    DAWN_PRO_PID = 0xf06a
    VOLUME_MAX = 0x00
    VOLUME_MIN = 0x70

    def __init__(self):
        self.volume = 0
        self.led_status = LED_STATUS_OFF
        self.current_filter = 'low'
        self.current_gain = 'low'
        self.device = usb.core.find(idVendor=self.MOONDROP_VID, idProduct=self.DAWN_PRO_PID)

        if self.device is None:
            raise ValueError("Device not found")
        logging.info("Device found and initialized.")

        self.constants = {
            'BM_REQUEST_TYPE_OUT': BM_REQUEST_TYPE_OUT,
            'BM_REQUEST_TYPE_IN': BM_REQUEST_TYPE_IN,
            'B_REQUEST': B_REQUEST,
            'B_REQUEST_GET': B_REQUEST_GET,
            'W_VALUE': W_VALUE,
            'W_INDEX': W_INDEX,
            'VOLUME_REFRESH_DATA': VOLUME_REFRESH_DATA,
            'DATA_LENGTH': DATA_LENGTH,
            'LED_STATUS_ENABLED': LED_STATUS_ENABLED,
            'LED_STATUS_TEMP_OFF': LED_STATUS_TEMP_OFF,
            'LED_STATUS_OFF': LED_STATUS_OFF
        }

        self.getter = GetMethods(self, self.constants)
        self.setter = SetMethods(self, self.constants)

    def send_control_transfer(self, bmRequestType, bRequest, wValue, wIndex, data_or_length):
        """Send a control transfer to the USB device."""
        try:
            time.sleep(0.1)
            return self.device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, data_or_length)
        except usb.core.USBError as error:
            logging.error(f"USB control transfer failed: {error}")
            raise IOError(f"USB control transfer failed: {error}") from error

    def refresh_volume(self):
        return self.setter.refresh_volume()

    def set_volume(self, volume):
        return self.setter.set_volume(volume)

    def get_current_volume(self):
        return self.getter.get_current_volume()

    def get_current_led_status(self):
        return self.getter.get_current_led_status()

    def get_gain(self):
        return self.getter.get_gain()
    
    def get_filter(self):
        return self.getter.get_filter()

    def set_led_status(self, status):
        return self.setter.set_led_status(status)

    def set_filter(self, filter_type):
        return self.setter.set_filter(filter_type)

    def set_gain(self, status):
        return self.setter.set_gain(status)
    
