"""
Hardware Emulation Layer for DawnPro-GUI Testing

This module provides mock classes that emulate the Moondrop Dawn Pro hardware
and USB interface, allowing tests to run without physical hardware.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import IntEnum
import time


class Gain(IntEnum):
    """Gain settings for the device."""

    LOW = 0
    HIGH = 1


class LEDStatus(IntEnum):
    """LED status values."""

    ON = 0
    TEMP_OFF = 1
    OFF = 2


class Filter(IntEnum):
    """Filter types available."""

    FAST_ROLL_OFF_LOW_LATENCY = 0
    FAST_ROLL_OFF_PHASE_COMPENSATED = 1
    SLOW_ROLL_OFF_LOW_LATENCY = 2
    SLOW_ROLL_OFF_PHASE_COMPENSATED = 3
    NON_OVERSAMPLING = 4


@dataclass
class DeviceState:
    """Represents the state of the mock device."""

    volume: int = 50  # Range: 0-112
    gain: Gain = Gain.LOW
    led_status: LEDStatus = LEDStatus.ON
    filter: Filter = Filter.FAST_ROLL_OFF_LOW_LATENCY
    connected: bool = True
    vendor_id: int = 12230  # 0x2fc6
    product_id: int = 61546  # 0xf06a
    command_log: List[Dict[str, Any]] = field(default_factory=list)
    error_mode: bool = False

    def log_command(self, command: str, value: Any, success: bool) -> None:
        """Log a command execution."""
        self.command_log.append(
            {
                "command": command,
                "value": value,
                "timestamp": time.time(),
                "success": success,
            }
        )

    def reset_to_defaults(self) -> None:
        """Reset device state to factory defaults."""
        self.volume = 50
        self.gain = Gain.LOW
        self.led_status = LEDStatus.ON
        self.filter = Filter.FAST_ROLL_OFF_LOW_LATENCY
        self.connected = True
        self.error_mode = False
        self.command_log.clear()


class MockUSBDevice:
    """
    Mock USB device that emulates pyusb behavior.

    This class simulates the USB communication layer, allowing tests
    to verify USB command handling without actual hardware.
    """

    def __init__(self, state: DeviceState) -> None:
        """Initialize the mock USB device.

        Args:
            state: The device state to emulate.
        """
        self.state = state
        self._last_response: Optional[List[int]] = None

    def ctrl_transfer(
        self,
        bmRequestType: int,
        bRequest: int,
        wValue: int,
        wIndex: int,
        data_or_length: Any,
    ) -> Optional[List[int]]:
        """
        Mock control transfer that emulates USB communication.

        Args:
            bmRequestType: Request type (IN/OUT).
            bRequest: Request number.
            wValue: Value field.
            wIndex: Index field.
            data_or_length: Data to send or length to receive.

        Returns:
            Response data as list of integers, or None.

        Raises:
            IOError: If device is disconnected or in error mode.
        """
        if not self.state.connected:
            raise IOError("Device disconnected")

        if self.state.error_mode:
            raise IOError("Simulated USB error")

        # Simulate processing time
        time.sleep(0.01)

        # Handle IN transfers (reading data from device)
        if bmRequestType == 0xC3:  # IN request
            return self._handle_in_transfer(bRequest, data_or_length)

        # Handle OUT transfers (writing data to device)
        if bmRequestType == 0x43 and isinstance(data_or_length, list):
            return self._handle_out_transfer(bRequest, data_or_length)

        return None

    def _handle_in_transfer(self, bRequest: int, data_or_length: Any) -> List[int]:
        """Handle IN transfer (reading from device).

        Returns a 7-byte response with current device state.
        """
        length = data_or_length if isinstance(data_or_length, int) else 7

        # Response format: [0xC0, 0xA5, 0x00, filter, gain, led, volume]
        response = [
            0xC0,
            0xA5,
            0x00,
            int(self.state.filter),  # index 3: filter
            int(self.state.gain),  # index 4: gain
            int(self.state.led_status),  # index 5: LED
            self.state.volume,  # index 6: volume (percentage)
        ]

        self._last_response = response
        return response[:length]

    def _handle_out_transfer(self, bRequest: int, data: List[int]) -> List[int]:
        """Handle OUT transfer (writing to device)."""
        # Acknowledge the command
        return [0x00]


class MockDawnProDevice:
    """
    High-level mock for the Moondrop Dawn Pro device.

    This class emulates the actual device behavior, including:
    - Volume control (0-112 percentage)
    - Gain switching (Low/High)
    - Filter selection (5 types)
    - LED status (On/Temp-Off/Off)
    - Connection state simulation
    - Error simulation
    """

    # Valid ranges
    VOLUME_MIN = 0
    VOLUME_MAX = 112

    def __init__(self) -> None:
        """Initialize the mock device with default state."""
        self.state = DeviceState()
        self.usb = MockUSBDevice(self.state)

    # ==================== Connection Methods ====================

    def connect(self) -> None:
        """Simulate device connection."""
        self.state.connected = True
        self.state.log_command("connect", None, True)

    def disconnect(self) -> None:
        """Simulate device disconnection."""
        self.state.connected = False
        self.state.log_command("disconnect", None, True)

    def is_connected(self) -> bool:
        """Check if device is connected."""
        return self.state.connected

    # ==================== Volume Methods ====================

    def set_volume(self, volume: int) -> bool:
        """
        Set the device volume.

        Args:
            volume: Volume percentage (0-112).

        Returns:
            True if successful, False otherwise.
        """
        if not self.state.connected:
            self.state.log_command("set_volume", volume, False)
            return False

        if self.state.error_mode:
            self.state.log_command("set_volume", volume, False)
            return False

        if volume < self.VOLUME_MIN or volume > self.VOLUME_MAX:
            self.state.log_command("set_volume", volume, False)
            return False

        self.state.volume = volume
        self.state.log_command("set_volume", volume, True)
        return True

    def get_volume(self) -> Optional[int]:
        """
        Get the current volume.

        Returns:
            Current volume percentage, or None if disconnected.
        """
        if not self.state.connected:
            return None
        return self.state.volume

    # ==================== Gain Methods ====================

    def set_gain(self, gain: str) -> bool:
        """
        Set the device gain.

        Args:
            gain: "Low" or "High".

        Returns:
            True if successful, False otherwise.
        """
        if not self.state.connected:
            self.state.log_command("set_gain", gain, False)
            return False

        if self.state.error_mode:
            self.state.log_command("set_gain", gain, False)
            return False

        gain_map = {"Low": Gain.LOW, "High": Gain.HIGH}
        if gain not in gain_map:
            self.state.log_command("set_gain", gain, False)
            return False

        self.state.gain = gain_map[gain]
        self.state.log_command("set_gain", gain, True)
        return True

    def get_gain(self) -> Optional[str]:
        """
        Get the current gain setting.

        Returns:
            "Low" or "High", or None if disconnected.
        """
        if not self.state.connected:
            return None
        return "Low" if self.state.gain == Gain.LOW else "High"

    # ==================== Filter Methods ====================

    def set_filter(self, filter_type: str) -> bool:
        """
        Set the filter type.

        Args:
            filter_type: One of the 5 filter types.

        Returns:
            True if successful, False otherwise.
        """
        if not self.state.connected:
            self.state.log_command("set_filter", filter_type, False)
            return False

        if self.state.error_mode:
            self.state.log_command("set_filter", filter_type, False)
            return False

        filter_map = {
            "Fast Roll-Off Low Latency": Filter.FAST_ROLL_OFF_LOW_LATENCY,
            "Fast Roll-Off Phase Compensated": Filter.FAST_ROLL_OFF_PHASE_COMPENSATED,
            "Slow Roll-Off Low Latency": Filter.SLOW_ROLL_OFF_LOW_LATENCY,
            "Slow Roll-Off Phase Compensated": Filter.SLOW_ROLL_OFF_PHASE_COMPENSATED,
            "Non-Oversampling": Filter.NON_OVERSAMPLING,
        }

        if filter_type not in filter_map:
            self.state.log_command("set_filter", filter_type, False)
            return False

        self.state.filter = filter_map[filter_type]
        self.state.log_command("set_filter", filter_type, True)
        return True

    def get_filter(self) -> Optional[str]:
        """
        Get the current filter type.

        Returns:
            Filter type string, or None if disconnected.
        """
        if not self.state.connected:
            return None

        filter_names = {
            Filter.FAST_ROLL_OFF_LOW_LATENCY: "Fast Roll-Off Low Latency",
            Filter.FAST_ROLL_OFF_PHASE_COMPENSATED: "Fast Roll-Off Phase Compensated",
            Filter.SLOW_ROLL_OFF_LOW_LATENCY: "Slow Roll-Off Low Latency",
            Filter.SLOW_ROLL_OFF_PHASE_COMPENSATED: "Slow Roll-Off Phase Compensated",
            Filter.NON_OVERSAMPLING: "Non-Oversampling",
        }
        return filter_names.get(self.state.filter)

    # ==================== LED Methods ====================

    def set_led_status(self, status: str) -> bool:
        """
        Set the LED status.

        Args:
            status: "On", "Temporarily Off", or "Off".

        Returns:
            True if successful, False otherwise.
        """
        if not self.state.connected:
            self.state.log_command("set_led_status", status, False)
            return False

        if self.state.error_mode:
            self.state.log_command("set_led_status", status, False)
            return False

        led_map = {
            "On": LEDStatus.ON,
            "Temporarily Off": LEDStatus.TEMP_OFF,
            "Off": LEDStatus.OFF,
        }
        if status not in led_map:
            self.state.log_command("set_led_status", status, False)
            return False

        self.state.led_status = led_map[status]
        self.state.log_command("set_led_status", status, True)
        return True

    def get_led_status(self) -> Optional[str]:
        """
        Get the current LED status.

        Returns:
            LED status string, or None if disconnected.
        """
        if not self.state.connected:
            return None

        led_names = {
            LEDStatus.ON: "On",
            LEDStatus.TEMP_OFF: "Temporarily Off",
            LEDStatus.OFF: "Off",
        }
        return led_names.get(self.state.led_status)

    # ==================== Error Simulation ====================

    def enable_error_mode(self) -> None:
        """Enable error simulation mode."""
        self.state.error_mode = True

    def disable_error_mode(self) -> None:
        """Disable error simulation mode."""
        self.state.error_mode = False

    # ==================== Command Logging ====================

    def get_command_log(self) -> List[Dict[str, Any]]:
        """Get the log of all executed commands."""
        return self.state.command_log.copy()

    def clear_command_log(self) -> None:
        """Clear the command log."""
        self.state.command_log.clear()

    def reset(self) -> None:
        """Reset device to factory defaults."""
        self.state.reset_to_defaults()
