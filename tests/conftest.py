"""
Pytest Configuration and Fixtures for DawnPro-GUI Tests

This module provides shared fixtures and configuration for all tests.
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import the mock hardware
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.mock_hardware import MockDawnProDevice, DeviceState, Gain, LEDStatus, Filter


@pytest.fixture
def mock_device() -> MockDawnProDevice:
    """
    Create a fresh mock device for each test.

    Returns:
        MockDawnProDevice: A new mock device with default state.
    """
    device = MockDawnProDevice()
    yield device
    # Cleanup: reset device state after each test
    device.reset()


@pytest.fixture
def connected_device(mock_device: MockDawnProDevice) -> MockDawnProDevice:
    """
    Provide a device that is guaranteed to be connected.

    Args:
        mock_device: The base mock device fixture.

    Returns:
        MockDawnProDevice: A connected mock device.
    """
    mock_device.connect()
    return mock_device


@pytest.fixture
def disconnected_device(mock_device: MockDawnProDevice) -> MockDawnProDevice:
    """
    Provide a device that is guaranteed to be disconnected.

    Args:
        mock_device: The base mock device fixture.

    Returns:
        MockDawnProDevice: A disconnected mock device.
    """
    mock_device.disconnect()
    return mock_device


@pytest.fixture
def device_with_default_settings(mock_device: MockDawnProDevice) -> MockDawnProDevice:
    """
    Provide a device with default settings (volume=50, gain=Low, LED=On, filter=Fast Low Latency).

    Args:
        mock_device: The base mock device fixture.

    Returns:
        MockDawnProDevice: A device with default settings.
    """
    mock_device.connect()
    mock_device.reset()
    return mock_device


@pytest.fixture
def error_mode_device(mock_device: MockDawnProDevice) -> MockDawnProDevice:
    """
    Provide a device in error mode for testing error handling.

    Args:
        mock_device: The base mock device fixture.

    Returns:
        MockDawnProDevice: A device with error mode enabled.
    """
    mock_device.connect()
    mock_device.enable_error_mode()
    return mock_device


@pytest.fixture
def volume_values() -> list:
    """
    Provide standard volume test values.

    Returns:
        list: Volume values [0, 25, 50, 75, 112] mapped to 0-112 range.
    """
    return [0, 28, 56, 84, 112]


@pytest.fixture
def invalid_volume_values() -> list:
    """
    Provide invalid volume values for negative testing.

    Returns:
        list: Invalid volume values [-1, 113, 200].
    """
    return [-1, 113, 200]


@pytest.fixture
def all_filters() -> list:
    """
    Provide all valid filter types.

    Returns:
        list: All 5 filter type strings.
    """
    return [
        "Fast Roll-Off Low Latency",
        "Fast Roll-Off Phase Compensated",
        "Slow Roll-Off Low Latency",
        "Slow Roll-Off Phase Compensated",
        "Non-Oversampling",
    ]


@pytest.fixture
def gain_values() -> list:
    """
    Provide valid gain values.

    Returns:
        list: ["Low", "High"].
    """
    return ["Low", "High"]


@pytest.fixture
def led_values() -> list:
    """
    Provide valid LED status values.

    Returns:
        list: ["On", "Temporarily Off", "Off"].
    """
    return ["On", "Temporarily Off", "Off"]


# ==================== Default Value Constants ====================


class Defaults:
    """Default values for the device."""

    VOLUME = 50
    GAIN = "Low"
    LED_STATUS = "On"
    FILTER = "Fast Roll-Off Low Latency"
    VOLUME_MIN = 0
    VOLUME_MAX = 112


@pytest.fixture
def defaults() -> Defaults:
    """
    Provide default value constants.

    Returns:
        Defaults: Object containing default values.
    """
    return Defaults()
