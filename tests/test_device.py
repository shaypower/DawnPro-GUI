"""
Device Detection Tests for DawnPro-GUI

Tests FR-3: Device Detection Tests
- FR-3.1: Connected detection
- FR-3.2: Disconnected detection
- FR-3.3: Reconnection handling
- FR-3.4: Vendor/product ID verification
"""

import pytest
from tests.mock_hardware import MockDawnProDevice


class TestDeviceDetection:
    """Test device connection and detection."""

    def test_device_detection_when_connected(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-3.1: Test passes when device is simulated as connected.

        Args:
            connected_device: Mock device that is connected.
        """
        assert connected_device.is_connected() is True

    def test_device_detection_when_disconnected(self, disconnected_device: MockDawnProDevice) -> None:
        """
        FR-3.2: Test passes when device is simulated as disconnected.

        Args:
            disconnected_device: Mock device that is disconnected.
        """
        assert disconnected_device.is_connected() is False

    def test_device_reconnection(self, mock_device: MockDawnProDevice) -> None:
        """
        FR-3.3: Verify device can be detected after reconnection.

        Args:
            mock_device: Base mock device.
        """
        # Start connected
        mock_device.connect()
        assert mock_device.is_connected() is True

        # Disconnect
        mock_device.disconnect()
        assert mock_device.is_connected() is False

        # Reconnect
        mock_device.connect()
        assert mock_device.is_connected() is True

    def test_device_vendor_id(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-3.4: Verify correct vendor ID (12230 / 0x2fc6).

        Args:
            connected_device: Mock device that is connected.
        """
        assert connected_device.state.vendor_id == 12230

    def test_device_product_id(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-3.4: Verify correct product ID (61546 / 0xf06a).

        Args:
            connected_device: Mock device that is connected.
        """
        assert connected_device.state.product_id == 61546

    def test_device_initial_state(self, mock_device: MockDawnProDevice) -> None:
        """
        Verify device initializes with correct default state.

        Args:
            mock_device: Base mock device.
        """
        # By default, device should be connected
        assert mock_device.is_connected() is True

    def test_disconnect_prevents_operations(self, disconnected_device: MockDawnProDevice) -> None:
        """
        Verify that operations fail when device is disconnected.

        Args:
            disconnected_device: Mock device that is disconnected.
        """
        # All set operations should return False when disconnected
        assert disconnected_device.set_volume(50) is False
        assert disconnected_device.set_gain("Low") is False
        assert disconnected_device.set_filter("Fast Roll-Off Low Latency") is False
        assert disconnected_device.set_led_status("On") is False

        # All get operations should return None when disconnected
        assert disconnected_device.get_volume() is None
        assert disconnected_device.get_gain() is None
        assert disconnected_device.get_filter() is None
        assert disconnected_device.get_led_status() is None


class TestDeviceState:
    """Test device state management."""

    def test_device_reset(self, mock_device: MockDawnProDevice) -> None:
        """
        Verify device can be reset to factory defaults.

        Args:
            mock_device: Base mock device.
        """
        # Change some settings
        mock_device.set_volume(30)
        mock_device.set_gain("High")
        mock_device.set_led_status("Off")
        mock_device.set_filter("Non-Oversampling")

        # Reset
        mock_device.reset()

        # Verify defaults
        assert mock_device.get_volume() == 50
        assert mock_device.get_gain() == "Low"
        assert mock_device.get_led_status() == "On"
        assert mock_device.get_filter() == "Fast Roll-Off Low Latency"

    def test_command_logging(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-2.4: Verify commands are logged.

        Args:
            connected_device: Mock device that is connected.
        """
        # Clear any initial commands
        connected_device.clear_command_log()

        # Execute some commands
        connected_device.set_volume(40)
        connected_device.set_gain("High")

        # Check log
        log = connected_device.get_command_log()
        assert len(log) >= 2

        # Verify log entries
        assert log[0]['command'] == 'set_volume'
        assert log[0]['value'] == 40
        assert log[0]['success'] is True

        assert log[1]['command'] == 'set_gain'
        assert log[1]['value'] == 'High'
        assert log[1]['success'] is True

    def test_command_log_clearing(self, connected_device: MockDawnProDevice) -> None:
        """
        Verify command log can be cleared.

        Args:
            connected_device: Mock device that is connected.
        """
        connected_device.set_volume(50)
        assert len(connected_device.get_command_log()) > 0

        connected_device.clear_command_log()
        assert len(connected_device.get_command_log()) == 0
