"""
LED Status Tests for DawnPro-GUI

Tests FR-7: LED Status Tests
- FR-7.1: Initial LED test
- FR-7.2: LED On setting
- FR-7.3: LED Temp-off setting
- FR-7.4: LED Off setting
- FR-7.5: LED state persistence
"""

import pytest
from tests.mock_hardware import MockDawnProDevice


class TestLEDInitial:
    """Test initial LED state."""

    def test_led_initial_value(self, device_with_default_settings: MockDawnProDevice) -> None:
        """
        FR-7.1: Verify initial LED = On.

        Args:
            device_with_default_settings: Device with default settings.
        """
        led_status = device_with_default_settings.get_led_status()
        assert led_status == "On"


class TestLEDValidSettings:
    """Test LED setting with valid values."""

    def test_set_led_on(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-7.2: Set LED to On, verify success.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_led_status("On")
        assert result is True
        assert connected_device.get_led_status() == "On"

    def test_set_led_temp_off(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-7.3: Set LED to Temporarily Off, verify success.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_led_status("Temporarily Off")
        assert result is True
        assert connected_device.get_led_status() == "Temporarily Off"

    def test_set_led_off(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-7.4: Set LED to Off, verify success.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_led_status("Off")
        assert result is True
        assert connected_device.get_led_status() == "Off"

    def test_set_led_all_valid_values(
        self,
        connected_device: MockDawnProDevice,
        led_values: list
    ) -> None:
        """
        FR-7.2/FR-7.3/FR-7.4: Test all valid LED values.

        Args:
            connected_device: Mock device that is connected.
            led_values: List of valid LED values from fixture.
        """
        for status in led_values:
            result = connected_device.set_led_status(status)
            assert result is True, f"Failed to set LED status to {status}"
            assert connected_device.get_led_status() == status


class TestLEDPersistence:
    """Test LED persistence across operations."""

    def test_led_state_unaffected_by_other_changes(
        self,
        connected_device: MockDawnProDevice
    ) -> None:
        """
        FR-7.5: LED state unaffected by volume/gain changes.

        Args:
            connected_device: Mock device that is connected.
        """
        # Set LED
        connected_device.set_led_status("Off")
        assert connected_device.get_led_status() == "Off"

        # Change other settings
        connected_device.set_volume(45)
        connected_device.set_gain("High")
        connected_device.set_filter("Non-Oversampling")

        # LED should still be Off
        assert connected_device.get_led_status() == "Off"

    def test_led_persists_multiple_sets(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-7.5: Multiple LED changes persist correctly.

        Args:
            connected_device: Mock device that is connected.
        """
        for status in ["Off", "On", "Temporarily Off", "On", "Off"]:
            connected_device.set_led_status(status)
            assert connected_device.get_led_status() == status


class TestLEDCommandLogging:
    """Test LED command logging."""

    def test_led_change_is_logged(self, connected_device: MockDawnProDevice) -> None:
        """
        LED changes are recorded in command log.

        Args:
            connected_device: Mock device that is connected.
        """
        connected_device.clear_command_log()
        connected_device.set_led_status("Temporarily Off")

        log = connected_device.get_command_log()
        assert len(log) > 0
        assert log[0]['command'] == 'set_led_status'
        assert log[0]['value'] == "Temporarily Off"
        assert log[0]['success'] is True

    def test_failed_led_change_is_logged(self, disconnected_device: MockDawnProDevice) -> None:
        """
        Failed LED changes are also logged.

        Args:
            disconnected_device: Mock device that is disconnected.
        """
        disconnected_device.clear_command_log()
        disconnected_device.set_led_status("On")

        log = disconnected_device.get_command_log()
        assert len(log) > 0
        assert log[0]['command'] == 'set_led_status'
        assert log[0]['success'] is False


class TestLEDDisconnected:
    """Test LED behavior when disconnected."""

    def test_set_led_when_disconnected(self, disconnected_device: MockDawnProDevice) -> None:
        """
        set_led_status returns false when disconnected.

        Args:
            disconnected_device: Mock device that is disconnected.
        """
        result = disconnected_device.set_led_status("On")
        assert result is False

    def test_get_led_when_disconnected(self, disconnected_device: MockDawnProDevice) -> None:
        """
        get_led_status returns None when disconnected.

        Args:
            disconnected_device: Mock device that is disconnected.
        """
        led_status = disconnected_device.get_led_status()
        assert led_status is None


class TestLEDInvalid:
    """Test LED with invalid values."""

    def test_set_invalid_led_status(self, connected_device: MockDawnProDevice) -> None:
        """
        Verify invalid LED status values are rejected.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_led_status("Blinking")
        assert result is False

    def test_set_empty_led_status(self, connected_device: MockDawnProDevice) -> None:
        """
        Verify empty LED status string is rejected.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_led_status("")
        assert result is False

    def test_set_similar_but_wrong_led_status(self, connected_device: MockDawnProDevice) -> None:
        """
        Verify similar but incorrect LED status names are rejected.

        Args:
            connected_device: Mock device that is connected.
        """
        result1 = connected_device.set_led_status("on")  # lowercase
        assert result1 is False

        result2 = connected_device.set_led_status("Temp Off")  # incomplete
        assert result2 is False
