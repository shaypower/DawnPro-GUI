"""
Gain Control Tests for DawnPro-GUI

Tests FR-5: Gain Control Tests (AMP High/Low Switching)
- FR-5.1: Initial gain test
- FR-5.2: Low gain setting
- FR-5.3: High gain setting
- FR-5.4: Gain toggle test
- FR-5.5: Persistence test
- FR-5.6: Command logging test
- FR-5.7: Disconnected behavior
"""

import pytest
from tests.mock_hardware import MockDawnProDevice


class TestGainInitial:
    """Test initial gain state."""

    def test_gain_initial_value(self, device_with_default_settings: MockDawnProDevice) -> None:
        """
        FR-5.1: Verify initial gain = Low.

        Args:
            device_with_default_settings: Device with default settings.
        """
        gain = device_with_default_settings.get_gain()
        assert gain == "Low"


class TestGainValidSettings:
    """Test gain setting with valid values."""

    def test_set_gain_low(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-5.2: Set gain to Low, verify success.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_gain("Low")
        assert result is True
        assert connected_device.get_gain() == "Low"

    def test_set_gain_high(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-5.3: Set gain to High, verify success.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_gain("High")
        assert result is True
        assert connected_device.get_gain() == "High"

    def test_set_gain_all_valid_values(
        self,
        connected_device: MockDawnProDevice,
        gain_values: list
    ) -> None:
        """
        FR-5.2/FR-5.3: Test all valid gain values.

        Args:
            connected_device: Mock device that is connected.
            gain_values: List of valid gain values from fixture.
        """
        for gain in gain_values:
            result = connected_device.set_gain(gain)
            assert result is True, f"Failed to set gain to {gain}"
            assert connected_device.get_gain() == gain


class TestGainToggle:
    """Test gain toggling behavior."""

    def test_gain_toggle_low_high(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-5.4: Toggle between Low/High multiple times.

        Args:
            connected_device: Mock device that is connected.
        """
        # Toggle multiple times
        for expected in ["High", "Low", "High", "Low", "High"]:
            result = connected_device.set_gain(expected)
            assert result is True
            assert connected_device.get_gain() == expected

    def test_gain_rapid_switching(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-5.4: Rapid gain switching works correctly.

        Args:
            connected_device: Mock device that is connected.
        """
        for _ in range(10):
            connected_device.set_gain("High")
            assert connected_device.get_gain() == "High"
            connected_device.set_gain("Low")
            assert connected_device.get_gain() == "Low"


class TestGainPersistence:
    """Test gain persistence across operations."""

    def test_gain_persists_after_other_operations(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-5.5: Gain setting persists across other changes.

        Args:
            connected_device: Mock device that is connected.
        """
        # Set gain
        connected_device.set_gain("High")
        assert connected_device.get_gain() == "High"

        # Change other settings
        connected_device.set_volume(45)
        connected_device.set_filter("Non-Oversampling")
        connected_device.set_led_status("Off")

        # Gain should still be High
        assert connected_device.get_gain() == "High"

    def test_gain_persists_multiple_sets(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-5.5: Multiple gain changes persist correctly.

        Args:
            connected_device: Mock device that is connected.
        """
        for gain in ["High", "Low", "High", "High", "Low"]:
            connected_device.set_gain(gain)
            assert connected_device.get_gain() == gain


class TestGainCommandLogging:
    """Test gain command logging."""

    def test_gain_change_is_logged(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-5.6: Gain changes recorded in log.

        Args:
            connected_device: Mock device that is connected.
        """
        connected_device.clear_command_log()
        connected_device.set_gain("High")

        log = connected_device.get_command_log()
        assert len(log) > 0
        assert log[0]['command'] == 'set_gain'
        assert log[0]['value'] == 'High'
        assert log[0]['success'] is True

    def test_failed_gain_change_is_logged(self, disconnected_device: MockDawnProDevice) -> None:
        """
        FR-5.6: Failed gain changes are also logged.

        Args:
            disconnected_device: Mock device that is disconnected.
        """
        disconnected_device.clear_command_log()
        disconnected_device.set_gain("High")

        log = disconnected_device.get_command_log()
        assert len(log) > 0
        assert log[0]['command'] == 'set_gain'
        assert log[0]['success'] is False


class TestGainDisconnected:
    """Test gain behavior when disconnected."""

    def test_set_gain_when_disconnected(self, disconnected_device: MockDawnProDevice) -> None:
        """
        FR-5.7: set_gain returns false when disconnected.

        Args:
            disconnected_device: Mock device that is disconnected.
        """
        result = disconnected_device.set_gain("High")
        assert result is False

    def test_get_gain_when_disconnected(self, disconnected_device: MockDawnProDevice) -> None:
        """
        FR-5.7: get_gain returns None when disconnected.

        Args:
            disconnected_device: Mock device that is disconnected.
        """
        gain = disconnected_device.get_gain()
        assert gain is None


class TestGainInvalid:
    """Test gain with invalid values."""

    def test_set_invalid_gain(self, connected_device: MockDawnProDevice) -> None:
        """
        Verify invalid gain values are rejected.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_gain("Medium")
        assert result is False

    def test_set_empty_gain(self, connected_device: MockDawnProDevice) -> None:
        """
        Verify empty gain string is rejected.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_gain("")
        assert result is False
