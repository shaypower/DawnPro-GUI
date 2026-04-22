"""
Integration Tests for DawnPro-GUI

Tests FR-8: Integration Tests
- FR-8.1: Complete workflow test
- FR-8.2: Disconnect/reconnect workflow
- FR-8.3: State persistence across ops
- FR-8.4: Rapid succession commands
- FR-8.5: Multi-parameter integration
"""

import pytest
from tests.mock_hardware import MockDawnProDevice


class TestCompleteWorkflow:
    """Test complete user workflows."""

    def test_complete_workflow(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-8.1: Test volume+gain+filter+led sequence.

        Args:
            connected_device: Mock device that is connected.
        """
        # Start with defaults
        assert connected_device.get_volume() == 50
        assert connected_device.get_gain() == "Low"
        assert connected_device.get_filter() == "Fast Roll-Off Low Latency"
        assert connected_device.get_led_status() == "On"

        # Change all settings
        assert connected_device.set_volume(75) is True
        assert connected_device.set_gain("High") is True
        assert connected_device.set_filter("Non-Oversampling") is True
        assert connected_device.set_led_status("Off") is True

        # Verify all changes
        assert connected_device.get_volume() == 75
        assert connected_device.get_gain() == "High"
        assert connected_device.get_filter() == "Non-Oversampling"
        assert connected_device.get_led_status() == "Off"

    def test_typical_user_session(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-8.1: Simulate a typical user session.

        Args:
            connected_device: Mock device that is connected.
        """
        # User increases volume
        connected_device.set_volume(75)
        assert connected_device.get_volume() == 75

        # User switches to high gain for better sound
        connected_device.set_gain("High")
        assert connected_device.get_gain() == "High"

        # User tries different filters
        connected_device.set_filter("Slow Roll-Off Phase Compensated")
        assert connected_device.get_filter() == "Slow Roll-Off Phase Compensated"

        # User turns off LED for night listening
        connected_device.set_led_status("Off")
        assert connected_device.get_led_status() == "Off"

        # User settles on medium volume
        connected_device.set_volume(45)
        assert connected_device.get_volume() == 45


class TestDisconnectReconnect:
    """Test disconnect and reconnect scenarios."""

    def test_disconnect_reconnect_workflow(
        self, mock_device: MockDawnProDevice
    ) -> None:
        """
        FR-8.2: Test operations during disconnection and after reconnection.

        Args:
            mock_device: Base mock device.
        """
        # Start connected
        mock_device.connect()
        mock_device.set_volume(50)
        assert mock_device.get_volume() == 50

        # Disconnect
        mock_device.disconnect()
        assert mock_device.is_connected() is False

        # Operations should fail
        assert mock_device.set_volume(75) is False
        assert mock_device.get_volume() is None

        # Reconnect
        mock_device.connect()
        assert mock_device.is_connected() is True

        # Operations should work again (state may be reset)
        assert mock_device.set_volume(40) is True
        assert mock_device.get_volume() == 40

    def test_state_after_reconnect(self, mock_device: MockDawnProDevice) -> None:
        """
        FR-8.2: Verify device state after reconnection.

        Args:
            mock_device: Base mock device.
        """
        # Set some values
        mock_device.set_volume(55)
        mock_device.set_gain("High")

        # Disconnect and reconnect
        mock_device.disconnect()
        mock_device.connect()

        # Device should work after reconnection
        assert mock_device.is_connected() is True
        assert mock_device.set_volume(30) is True


class TestStatePersistence:
    """Test state persistence across operations."""

    def test_unrelated_settings_persist(
        self, connected_device: MockDawnProDevice
    ) -> None:
        """
        FR-8.3: Verify unrelated settings persist during changes.

        Args:
            connected_device: Mock device that is connected.
        """
        # Set initial state
        connected_device.set_volume(40)
        connected_device.set_gain("High")
        connected_device.set_filter("Fast Roll-Off Phase Compensated")
        connected_device.set_led_status("Temporarily Off")

        # Change only volume
        connected_device.set_volume(50)

        # Other settings should persist
        assert connected_device.get_gain() == "High"
        assert connected_device.get_filter() == "Fast Roll-Off Phase Compensated"
        assert connected_device.get_led_status() == "Temporarily Off"

        # Change only gain
        connected_device.set_gain("Low")

        # Other settings should persist
        assert connected_device.get_volume() == 50
        assert connected_device.get_filter() == "Fast Roll-Off Phase Compensated"
        assert connected_device.get_led_status() == "Temporarily Off"

    def test_multiple_changes_preserve_state(
        self, connected_device: MockDawnProDevice
    ) -> None:
        """
        FR-8.3: Multiple changes preserve unrelated state.

        Args:
            connected_device: Mock device that is connected.
        """
        # Set filter and LED
        connected_device.set_filter("Non-Oversampling")
        connected_device.set_led_status("Off")

        # Make multiple volume changes
        for v in [30, 50, 80, 112]:
            connected_device.set_volume(v)
            assert connected_device.get_volume() == v

        # Filter and LED should persist
        assert connected_device.get_filter() == "Non-Oversampling"
        assert connected_device.get_led_status() == "Off"


class TestRapidSuccession:
    """Test rapid command execution."""

    def test_rapid_succession_commands(
        self, connected_device: MockDawnProDevice
    ) -> None:
        """
        FR-8.4: 10+ commands in sequence work correctly.

        Args:
            connected_device: Mock device that is connected.
        """
        commands = [
            ("volume", 30),
            ("gain", "High"),
            ("filter", "Slow Roll-Off Low Latency"),
            ("volume", 40),
            ("led", "Off"),
            ("gain", "Low"),
            ("filter", "Fast Roll-Off Phase Compensated"),
            ("volume", 50),
            ("led", "On"),
            ("filter", "Non-Oversampling"),
            ("gain", "High"),
            ("volume", 80),
        ]

        for cmd, value in commands:
            if cmd == "volume":
                result = connected_device.set_volume(value)
                assert result is True
            elif cmd == "gain":
                result = connected_device.set_gain(value)
                assert result is True
            elif cmd == "filter":
                result = connected_device.set_filter(value)
                assert result is True
            elif cmd == "led":
                result = connected_device.set_led_status(value)
                assert result is True

        # Verify final state
        assert connected_device.get_volume() == 80
        assert connected_device.get_gain() == "High"
        assert connected_device.get_filter() == "Non-Oversampling"
        assert connected_device.get_led_status() == "On"

    def test_rapid_volume_changes(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-8.4: Rapid volume changes work correctly.

        Args:
            connected_device: Mock device that is connected.
        """
        for v in range(0, 61, 5):
            connected_device.set_volume(v)
            assert connected_device.get_volume() == v


class TestMultiParameter:
    """Test multi-parameter interactions."""

    def test_all_parameters_together(self, connected_device: MockDawnProDevice) -> None:
        """
        FR-8.5: Test interactions between all settings.

        Args:
            connected_device: Mock device that is connected.
        """
        # Set all parameters
        connected_device.set_volume(35)
        connected_device.set_gain("High")
        connected_device.set_filter("Slow Roll-Off Phase Compensated")
        connected_device.set_led_status("Temporarily Off")

        # Verify all are set correctly
        assert connected_device.get_volume() == 35
        assert connected_device.get_gain() == "High"
        assert connected_device.get_filter() == "Slow Roll-Off Phase Compensated"
        assert connected_device.get_led_status() == "Temporarily Off"

    def test_interleaved_get_set_operations(
        self, connected_device: MockDawnProDevice
    ) -> None:
        """
        FR-8.5: Interleaved get/set operations work correctly.

        Args:
            connected_device: Mock device that is connected.
        """
        # Set and get in interleaved fashion
        connected_device.set_volume(25)
        assert connected_device.get_volume() == 25

        connected_device.set_gain("High")
        assert connected_device.get_gain() == "High"

        connected_device.set_filter("Non-Oversampling")
        assert connected_device.get_filter() == "Non-Oversampling"

        connected_device.set_led_status("Off")
        assert connected_device.get_led_status() == "Off"

        # Verify all persist
        assert connected_device.get_volume() == 25
        assert connected_device.get_gain() == "High"
        assert connected_device.get_filter() == "Non-Oversampling"
        assert connected_device.get_led_status() == "Off"


class TestErrorHandling:
    """Test error handling scenarios."""

    def test_operations_fail_gracefully_when_disconnected(
        self, disconnected_device: MockDawnProDevice
    ) -> None:
        """
        All operations fail gracefully when disconnected.

        Args:
            disconnected_device: Mock device that is disconnected.
        """
        # All set operations return False
        assert disconnected_device.set_volume(50) is False
        assert disconnected_device.set_gain("High") is False
        assert disconnected_device.set_filter("Non-Oversampling") is False
        assert disconnected_device.set_led_status("Off") is False

        # All get operations return None
        assert disconnected_device.get_volume() is None
        assert disconnected_device.get_gain() is None
        assert disconnected_device.get_filter() is None
        assert disconnected_device.get_led_status() is None

    def test_invalid_values_handled_gracefully(
        self, connected_device: MockDawnProDevice
    ) -> None:
        """
        Invalid values are handled gracefully.

        Args:
            connected_device: Mock device that is connected.
        """
        # Invalid values return False but don't crash
        assert connected_device.set_volume(-1) is False
        assert connected_device.set_volume(113) is False
        assert connected_device.set_gain("Medium") is False
        assert connected_device.set_filter("Unknown") is False
        assert connected_device.set_led_status("Blinking") is False
