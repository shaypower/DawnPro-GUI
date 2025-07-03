from typing import Dict, Union


def convert_volume_to_percent(value: int) -> int:
    """Convert a raw volume value to a percentage.

    Args:
        value: The raw volume value (0x00-0xFF).

    Returns:
        The volume as a percentage (0-60).
    """
    volume_table = [
      0xFF, 0xC8, 0xB4, 0xAA, 0xA0, 0x96, 0x8C, 0x82, 0x7A, 0x74,
      0x6E, 0x6A, 0x66, 0x62, 0x5E, 0x5A, 0x58, 0x56, 0x54, 0x52,
      0x50, 0x4E, 0x4C, 0x4A, 0x48, 0x46, 0x44, 0x42, 0x40, 0x3E,
      0x3C, 0x3A, 0x38, 0x36, 0x34, 0x32, 0x30, 0x2E, 0x2C, 0x2A,
      0x28, 0x26, 0x24, 0x22, 0x20, 0x1E, 0x1C, 0x1A, 0x18, 0x16,
      0x14, 0x12, 0x10, 0x0E, 0x0C, 0x0A, 0x08, 0x06, 0x04, 0x02,
      0x00
    ]
    try:
        return volume_table.index(value)
    except ValueError:
        return 0


def convert_volume_to_payload(value: int) -> int:
    """Convert a percentage volume to a raw payload value.

    Args:
        value: The volume percentage (0-60).

    Returns:
        The raw volume value (0x00-0xFF).
    """
    volume_table = [
      0xFF, 0xC8, 0xB4, 0xAA, 0xA0, 0x96, 0x8C, 0x82, 0x7A, 0x74,
      0x6E, 0x6A, 0x66, 0x62, 0x5E, 0x5A, 0x58, 0x56, 0x54, 0x52,
      0x50, 0x4E, 0x4C, 0x4A, 0x48, 0x46, 0x44, 0x42, 0x40, 0x3E,
      0x3C, 0x3A, 0x38, 0x36, 0x34, 0x32, 0x30, 0x2E, 0x2C, 0x2A,
      0x28, 0x26, 0x24, 0x22, 0x20, 0x1E, 0x1C, 0x1A, 0x18, 0x16,
      0x14, 0x12, 0x10, 0x0E, 0x0C, 0x0A, 0x08, 0x06, 0x04, 0x02,
      0x00
    ]
    try:
      return volume_table[value]
    except ValueError:
      return 0


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
