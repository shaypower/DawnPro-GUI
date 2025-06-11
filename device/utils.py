from typing import Dict, Union


def convert_volume_to_percent(value: int) -> int:
    """Convert a raw volume value to a percentage.

    Args:
        value: The raw volume value (0x00-0x70).

    Returns:
        The volume as a percentage (0-100).
    """
    clamped_value = max(0x00, min(0x70, value))
    return (0x70 - clamped_value) * 100 // 0x70


def convert_volume_to_payload(value: int) -> int:
    """Convert a percentage volume to a raw payload value.

    Args:
        value: The volume percentage (0-100).

    Returns:
        The raw volume value (0x00-0x70).
    """
    payload_value = (0x70 - (value * 0x70 // 100)) - 1
    return max(0x00, min(0x70, payload_value))


def convert_led_status_to_string(value: int) -> str:
    """Convert a raw LED status value to a string.

    Args:
        value: The raw LED status value (0-2).

    Returns:
        The LED status as a string ("On", "Temporarily Off", or "Off").
    """
    led_map: Dict[int, str] = {0: "On", 1: "Temporarily Off", 2: "Off"}
    return led_map.get(value, "Invalid LED Status")


def convert_gain_to_string(value: int) -> str:
    """Convert a raw gain value to a string.

    Args:
        value: The raw gain value (0-1).

    Returns:
        The gain as a string ("Low" or "High").
    """
    gain_map: Dict[int, str] = {0: "Low", 1: "High"}
    return gain_map.get(value, "Invalid Gain Value")


def convert_gain_to_payload(value: str) -> int:
    """Convert a gain string to a raw payload value.

    Args:
        value: The gain string ("Low" or "High").

    Returns:
        The raw gain value (0 or 1).
    """
    gain_map: Dict[str, int] = {"Low": 0, "High": 1}
    return gain_map.get(value, 0)


def convert_led_status_to_payload(value: str) -> int:
    """Convert an LED status string to a raw payload value.

    Args:
        value: The LED status string ("On", "Temporarily Off", or "Off").

    Returns:
        The raw LED status value (0-2).
    """
    led_map: Dict[str, int] = {"On": 0, "Temporarily Off": 1, "Off": 2}
    return led_map.get(value, 0)


def convert_filter_to_payload(value: str) -> int:
    """Convert a filter type string to a raw payload value.

    Args:
        value: The filter type string.

    Returns:
        The raw filter value (0-4).
    """
    filter_map: Dict[str, int] = {
        "Fast Roll-Off Low Latency": 0,
        "Fast Roll-Off Phase Compensated": 1,
        "Slow Roll-Off Low Latency": 2,
        "Slow Roll-Off Phase Compensated": 3,
        "Non-Oversampling": 4
    }
    return filter_map.get(value, 0)


def convert_filter_payload_to_string(value: int) -> str:
    """Convert a raw filter value to a string.

    Args:
        value: The raw filter value (0-4).

    Returns:
        The filter type as a string.
    """
    filter_map: Dict[int, str] = {
        0: "Fast Roll-Off Low Latency",
        1: "Fast Roll-Off Phase Compensated",
        2: "Slow Roll-Off Low Latency",
        3: "Slow Roll-Off Phase Compensated",
        4: "Non-Oversampling"
    }
    return filter_map.get(value, "Invalid Filter Value")