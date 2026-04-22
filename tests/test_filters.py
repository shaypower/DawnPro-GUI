"""
Filter Selection Tests for DawnPro-GUI

Tests FR-6: Filter Selection Tests
- FR-6.1: Initial filter test
- FR-6.2: All filter types
- FR-6.3 to FR-6.7: Individual filter tests
- FR-6.8: Filter cycle test
- FR-6.9: Command logging test
- FR-6.10: Disconnected behavior
"""

import pytest
from tests.mock_hardware import MockDawnProDevice


class TestFilterInitial:
    """Test initial filter state."""

    def test_filter_initial_value(self, device_with_default_settings: MockDawnProDevice) -> None:
        """
        FR-6.1: Verify initial filter = Fast Roll-Off Low Latency.

        Args:
            device_with_default_settings: Device with default settings.
        """
        filter_type = device_with_default_settings.get_filter()
        assert filter_type == "Fast Roll-Off Low Latency"


class TestFilterAllTypes:
    """Test all filter types can be set."""

    def test_all_filters(
        self,
        connected_device: MockDawnProDevice,
        all_filters: list
    ) -> None:
        """
        FR-6.2: Test all 5 filter types.

        Args:
            connected_device: Mock device that is connected.
            all_filters: List of all filter types from fixture.
        """
        for filter_type in all_filters:
            result = connected_device.set_filter(filter_type)
            assert result is True, f"Failed to set filter to {filter_type}"
            assert connected_device.get_filter() == filter_type


class TestFilterIndividual:
    """Test each filter type individually."""

    def test_fast_roll_off_low_latency(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-6.3: Set and verify Fast Roll-Off Low Latency.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_filter("Fast Roll-Off Low Latency")
        assert result is True
        assert connected_device.get_filter() == "Fast Roll-Off Low Latency"

    def test_fast_roll_off_phase_compensated(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-6.4: Set and verify Fast Roll-Off Phase Compensated.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_filter("Fast Roll-Off Phase Compensated")
        assert result is True
        assert connected_device.get_filter() == "Fast Roll-Off Phase Compensated"

    def test_slow_roll_off_low_latency(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-6.5: Set and verify Slow Roll-Off Low Latency.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_filter("Slow Roll-Off Low Latency")
        assert result is True
        assert connected_device.get_filter() == "Slow Roll-Off Low Latency"

    def test_slow_roll_off_phase_compensated(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-6.6: Set and verify Slow Roll-Off Phase Compensated.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_filter("Slow Roll-Off Phase Compensated")
        assert result is True
        assert connected_device.get_filter() == "Slow Roll-Off Phase Compensated"

    def test_non_oversampling(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-6.7: Set and verify Non-Oversampling.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_filter("Non-Oversampling")
        assert result is True
        assert connected_device.get_filter() == "Non-Oversampling"


class TestFilterCycle:
    """Test filter cycling behavior."""

    def test_filter_cycle_through_all(
        self,
        connected_device: MockDawnProDevice,
        all_filters: list
    ) -> None:
        """
        FR-6.8: Cycle through all filters successfully.

        Args:
            connected_device: Mock device that is connected.
            all_filters: List of all filter types from fixture.
        """
        for filter_type in all_filters:
            result = connected_device.set_filter(filter_type)
            assert result is True
            assert connected_device.get_filter() == filter_type

    def test_filter_rapid_switching(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-6.8: Rapid filter switching works correctly.

        Args:
            connected_device: Mock device that is connected.
        """
        filters = [
            "Fast Roll-Off Low Latency",
            "Non-Oversampling",
            "Fast Roll-Off Phase Compensated",
            "Slow Roll-Off Low Latency",
            "Slow Roll-Off Phase Compensated"
        ]
        for f in filters:
            connected_device.set_filter(f)
            assert connected_device.get_filter() == f


class TestFilterPersistence:
    """Test filter persistence across operations."""

    def test_filter_persists_after_other_operations(self, connected_device: MockDawnProDevice) -> None:
        """
        Filter setting persists across other changes.

        Args:
            connected_device: Mock device that is connected.
        """
        # Set filter
        connected_device.set_filter("Non-Oversampling")
        assert connected_device.get_filter() == "Non-Oversampling"

        # Change other settings
        connected_device.set_volume(45)
        connected_device.set_gain("High")
        connected_device.set_led_status("Off")

        # Filter should still be Non-Oversampling
        assert connected_device.get_filter() == "Non-Oversampling"


class TestFilterCommandLogging:
    """Test filter command logging."""

    def test_filter_change_is_logged(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-6.9: Filter changes recorded in log.

        Args:
            connected_device: Mock device that is connected.
        """
        connected_device.clear_command_log()
        connected_device.set_filter("Slow Roll-Off Phase Compensated")

        log = connected_device.get_command_log()
        assert len(log) > 0
        assert log[0]['command'] == 'set_filter'
        assert log[0]['value'] == "Slow Roll-Off Phase Compensated"
        assert log[0]['success'] is True

    def test_failed_filter_change_is_logged(self, disconnected_device: MockDawnProDevice) -> None:
        """
        FR-6.9: Failed filter changes are also logged.

        Args:
            disconnected_device: Mock device that is disconnected.
        """
        disconnected_device.clear_command_log()
        disconnected_device.set_filter("Non-Oversampling")

        log = disconnected_device.get_command_log()
        assert len(log) > 0
        assert log[0]['command'] == 'set_filter'
        assert log[0]['success'] is False


class TestFilterDisconnected:
    """Test filter behavior when disconnected."""

    def test_set_filter_when_disconnected(self, disconnected_device: MockDawnProDevice) -> None:
        """
        FR-6.10: set_filter returns false when disconnected.

        Args:
            disconnected_device: Mock device that is disconnected.
        """
        result = disconnected_device.set_filter("Fast Roll-Off Low Latency")
        assert result is False

    def test_get_filter_when_disconnected(self, disconnected_device: MockDawnProDevice) -> None:
        """
        FR-6.10: get_filter returns None when disconnected.

        Args:
            disconnected_device: Mock device that is disconnected.
        """
        filter_type = disconnected_device.get_filter()
        assert filter_type is None


class TestFilterInvalid:
    """Test filter with invalid values."""

    def test_set_invalid_filter(self, connected_device: MockDawnProDevice) -> None:
        """
        Verify invalid filter values are rejected.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_filter("Invalid Filter")
        assert result is False

    def test_set_empty_filter(self, connected_device: MockDawnProDevice) -> None:
        """
        Verify empty filter string is rejected.

        Args:
            connected_device: Mock device that is connected.
        """
        result = connected_device.set_filter("")
        assert result is False

    def test_set_similar_but_wrong_filter(self, connected_device: MockDawnProDevice) -> None:
        """
        Verify similar but incorrect filter names are rejected.

        Args:
            connected_device: Mock device that is connected.
        """
        # These should fail due to exact string matching
        result1 = connected_device.set_filter("fast roll-off low latency")  # lowercase
        assert result1 is False

        result2 = connected_device.set_filter("Fast Roll-Off")  # incomplete
        assert result2 is False
