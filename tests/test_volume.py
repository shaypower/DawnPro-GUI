"""
Volume Control Tests for DawnPro-GUI

Tests FR-4: Volume Control Tests
- FR-4.1: Initial volume test
- FR-4.2: Valid range testing
- FR-4.3: Boundary testing
- FR-4.4: Invalid low test
- FR-4.5: Invalid high test
- FR-4.6: Persistence test
- FR-4.7: Command logging test
- FR-4.8: Disconnected behavior
"""

import pytest
from tests.mock_hardware import MockDawnProDevice
from tests.conftest import Defaults


class TestVolumeInitial:
    """Test initial volume state."""

    def test_volume_initial_value(
        self, device_with_default_settings: MockDawnProDevice
    ) -> None:
        """
        FR-4.1: Verify initial volume = 50 (default).

        Args:
            device_with_default_settings: Device with default settings.
        """
        volume = device_with_default_settings.get_volume()
        assert volume == 50


class TestVolumeValidRange:
    """Test volume setting with valid values."""

    def test_set_volume_zero(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-4.2: Test volume at minimum (0).

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_volume(0)
        assert result is True
        assert connected_device.get_volume() == 0

    def test_set_volume_middle(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-4.2: Test volume at middle range (30).

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_volume(30)
        assert result is True
        assert connected_device.get_volume() == 30

    def test_set_volume_max(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-4.2: Test volume at maximum (112).

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_volume(112)
        assert result is True
        assert connected_device.get_volume() == 112

    def test_set_volume_various_values(
        self, connected_device: MockDawnProDevice, volume_values: list
    ) -> None:
        """
        FR-4.2: Test multiple valid volume values.

        Args:
            connected_device: Mock device that is connected.
            volume_values: List of valid volume values from fixture.
        """
        for value in volume_values:
            result = connected_device.set_volume(value)
            assert result is True, f"Failed to set volume to {value}"
            assert connected_device.get_volume() == value


class TestVolumeBoundaries:
    """Test volume boundary conditions."""

    def test_volume_min_boundary(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-4.3: Test volume at minimum boundary (0).

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_volume(Defaults.VOLUME_MIN)
        assert result is True
        assert connected_device.get_volume() == Defaults.VOLUME_MIN

    def test_volume_max_boundary(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-4.3: Test volume at maximum boundary (112).

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_volume(Defaults.VOLUME_MAX)
        assert result is True
        assert connected_device.get_volume() == Defaults.VOLUME_MAX


class TestVolumeInvalid:
    """Test volume with invalid values."""

    def test_volume_below_min(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-4.4: Verify error on volume < 0.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_volume(-1)
        assert result is False

    def test_volume_above_max(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-4.5: Verify error on volume > 112.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_volume(113)
        assert result is False

    def test_volume_far_above_max(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-4.5: Verify error on volume far above max (200).

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_volume(200)
        assert result is False

    def test_invalid_volume_values(
        self, connected_device: MockDawnProDevice, invalid_volume_values: list
    ) -> None:
        """
        FR-4.4/FR-4.5: Test multiple invalid volume values.

        Args:
            connected_device: Mock device that is connected.
            invalid_volume_values: List of invalid volume values from fixture.
        """
        for value in invalid_volume_values:
            result = connected_device.set_volume(value)
            assert result is False, f"Should have failed for volume {value}"


class TestVolumePersistence:
    """Test volume persistence across operations."""

    def test_volume_persists_after_other_operations(
        self, connected_device: MockDawnProDevice
    ) -> None:
        """
        FR-4.6: Volume changes persist across other operations.

        Args:
            connected_device: Mock device that is connected.
        """
        # Set volume
        connected_device.set_volume(45)
        assert connected_device.get_volume() == 45

        # Change other settings
        connected_device.set_gain("High")
        connected_device.set_filter("Non-Oversampling")
        connected_device.set_led_status("Off")

        # Volume should still be 45
        assert connected_device.get_volume() == 45

    def test_volume_persists_multiple_sets(
        self, connected_device: MockDawnProDevice
    ) -> None:
        """
        FR-4.6: Multiple volume changes persist correctly.

        Args:
            connected_device: Mock device that is connected.
        """
        for value in [10, 20, 30, 40, 50]:
            connected_device.set_volume(value)
            assert connected_device.get_volume() == value


class TestVolumeCommandLogging:
    """Test volume command logging."""

    def test_volume_change_is_logged(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-4.7: Volume changes are recorded in command log.

        Args:
            connected_device: Mock device that is connected.
        """
        connected_device.clear_command_log()
        connected_device.set_volume(35)

        log = connected_device.get_command_log()
        assert len(log) > 0
        assert log[0]["command"] == "set_volume"
        assert log[0]["value"] == 35
        assert log[0]["success"] is True

    def test_failed_volume_change_is_logged(
        self, disconnected_device: MockDawnProDevice
    ) -> None:
        """
        FR-4.7: Failed volume changes are also logged.

        Args:
            disconnected_device: Mock device that is disconnected.
        """
        disconnected_device.clear_command_log()
        disconnected_device.set_volume(50)

        log = disconnected_device.get_command_log()
        assert len(log) > 0
        assert log[0]["command"] == "set_volume"
        assert log[0]["success"] is False


class TestVolumeDisconnected:
    """Test volume behavior when disconnected."""

    def test_set_volume_when_disconnected(
        self, disconnected_device: MockDawnProDevice
    ) -> None:
        """
        FR-4.8: set_volume returns false when disconnected.

        Args:
            disconnected_device: Mock device that is disconnected.
        """
        result = disconnected_device.set_volume(50)
        assert result is False

    def test_get_volume_when_disconnected(
        self, disconnected_device: MockDawnProDevice
    ) -> None:
        """
        FR-4.8: get_volume returns None when disconnected.

        Args:
            disconnected_device: Mock device that is disconnected.
        """
        volume = disconnected_device.get_volume()
        assert volume is None
