"""
Error Handling Tests for DawnPro-GUI

Tests FR-2.5: Error simulation
Tests error handling scenarios including:
- USB communication errors
- Invalid parameter handling
- Edge cases
"""

import pytest
from tests.mock_hardware import MockDawnProDevice


class TestErrorSimulation:
    """Test error simulation capabilities."""

    def test_error_mode_enabled(self, mock_device: MockDawnProDevice) -> None:
        """
        FR-2.5: Verify error mode can be enabled.

        Args:
            mock_device: Base mock device.
        """
        mock_device.connect()
        mock_device.enable_error_mode()
        # Device should still report connected
        assert mock_device.is_connected() is True

    def test_error_mode_disabled(self, mock_device: MockDawnProDevice) -> None:
        """
        FR-2.5: Verify error mode can be disabled.

        Args:
            mock_device: Base mock device.
        """
        mock_device.connect()
        mock_device.enable_error_mode()
        mock_device.disable_error_mode()
        # Device should work normally
        assert mock_device.set_volume(50) is True

    def test_operations_fail_in_error_mode(
        self, mock_device: MockDawnProDevice
    ) -> None:
        """
        FR-2.5: Operations fail when error mode is enabled.

        Args:
            mock_device: Base mock device.
        """
        mock_device.connect()
        mock_device.enable_error_mode()

        # All operations should fail in error mode
        assert mock_device.set_volume(50) is False
        assert mock_device.set_gain("High") is False
        assert mock_device.set_filter("Non-Oversampling") is False
        assert mock_device.set_led_status("Off") is False


class TestBoundaryConditions:
    """Test boundary condition handling."""

    def test_volume_at_exact_min(self, connected_device: MockDawnProDevice) -> None:
        """
        Volume at exact minimum (0) works.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_volume(0)
        assert result is True
        assert connected_device.get_volume() == 0

    def test_volume_at_exact_max(self, connected_device: MockDawnProDevice) -> None:
        """
        Volume at exact maximum (112) works.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_volume(112)
        assert result is True
        assert connected_device.get_volume() == 112

    def test_volume_just_inside_bounds(
        self, connected_device: MockDawnProDevice
    ) -> None:
        """
        Volume just inside bounds works.

        Args:
            connected_device: Mock device that is connected.
        """
        result1 = connected_device.set_volume(1)
        assert result1 is True
        assert connected_device.get_volume() == 1

        result2 = connected_device.set_volume(111)
        assert result2 is True
        assert connected_device.get_volume() == 111

    def test_volume_just_outside_bounds(
        self, connected_device: MockDawnProDevice
    ) -> None:
        """
        Volume just outside bounds fails.

        Args:
            connected_device: Mock device that is connected.
        """
        result1 = connected_device.set_volume(-1)
        assert result1 is False

        result2 = connected_device.set_volume(113)
        assert result2 is False


class TestNoneAndEmptyHandling:
    """Test handling of None and empty values."""

    def test_set_none_gain(self, connected_device: MockDawnProDevice) -> None:
        """
        None gain value is handled gracefully.

        Args:
            connected_device: Mock device that is connected.
        """
        # This should not crash
        result = connected_device.set_gain(None)  # type: ignore
        assert result is False

    def test_set_none_filter(self, connected_device: MockDawnProDevice) -> None:
        """
        None filter value is handled gracefully.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_filter(None)  # type: ignore
        assert result is False

    def test_set_none_led(self, connected_device: MockDawnProDevice) -> None:
        """
        None LED value is handled gracefully.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_led_status(None)  # type: ignore
        assert result is False


class TestRepeatedOperations:
    """Test repeated operations."""

    def test_same_volume_set_repeatedly(
        self, connected_device: MockDawnProDevice
    ) -> None:
        """
        Setting the same volume repeatedly works.

        Args:
            connected_device: Mock device that is connected.
        """
        for _ in range(10):
            result = connected_device.set_volume(42)
            assert result is True
        assert connected_device.get_volume() == 42

    def test_same_gain_set_repeatedly(
        self, connected_device: MockDawnProDevice
    ) -> None:
        """
        Setting the same gain repeatedly works.

        Args:
            connected_device: Mock device that is connected.
        """
        for _ in range(10):
            result = connected_device.set_gain("High")
            assert result is True
        assert connected_device.get_gain() == "High"

    def test_same_filter_set_repeatedly(
        self, connected_device: MockDawnProDevice
    ) -> None:
        """
        Setting the same filter repeatedly works.

        Args:
            connected_device: Mock device that is connected.
        """
        for _ in range(10):
            result = connected_device.set_filter("Non-Oversampling")
            assert result is True
        assert connected_device.get_filter() == "Non-Oversampling"

    def test_same_led_set_repeatedly(self, connected_device: MockDawnProDevice) -> None:
        """
        Setting the same LED status repeatedly works.

        Args:
            connected_device: Mock device that is connected.
        """
        for _ in range(10):
            result = connected_device.set_led_status("Off")
            assert result is True
        assert connected_device.get_led_status() == "Off"


class TestCommandLogIntegrity:
    """Test command log integrity."""

    def test_command_log_has_timestamps(
        self, connected_device: MockDawnProDevice
    ) -> None:
        """
        Command log entries have timestamps.

        Args:
            connected_device: Mock device that is connected.
        """
        connected_device.clear_command_log()
        connected_device.set_volume(50)

        log = connected_device.get_command_log()
        assert len(log) > 0
        assert "timestamp" in log[0]
        assert log[0]["timestamp"] > 0

    def test_command_log_has_success_field(
        self, connected_device: MockDawnProDevice
    ) -> None:
        """
        Command log entries have success field.

        Args:
            connected_device: Mock device that is connected.
        """
        connected_device.clear_command_log()
        connected_device.set_volume(50)

        log = connected_device.get_command_log()
        assert len(log) > 0
        assert "success" in log[0]
        assert log[0]["success"] is True

    def test_command_log_order(self, connected_device: MockDawnProDevice) -> None:
        """
        Command log maintains correct order.

        Args:
            connected_device: Mock device that is connected.
        """
        connected_device.clear_command_log()

        connected_device.set_volume(30)
        connected_device.set_gain("High")
        connected_device.set_filter("Non-Oversampling")

        log = connected_device.get_command_log()
        assert len(log) >= 3
        assert log[0]["command"] == "set_volume"
        assert log[1]["command"] == "set_gain"
        assert log[2]["command"] == "set_filter"
