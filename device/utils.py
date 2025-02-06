def convert_volume_to_percent(value):
    clamped_value = max(0x00, min(0x70, value))
    return (0x70 - clamped_value) * 100 // 0x70

def convert_volume_to_payload(value):
    payload_value = (0x70 - (value * 0x70 // 100)) - 1
    return max(0x00, min(0x70, payload_value))

def convert_led_status_to_string(value):
    led_map = {0: "On", 1: "Temporarily Off", 2: "Off"}
    return led_map.get(value, "Invalid LED Status")

def convert_gain_to_string(value):
    gain_map = {0: "Low", 1: "High"}
    return gain_map.get(value, "Invalid Gain Value")

def convert_gain_to_payload(value):
    gain_map = {"Low": 0, "High": 1}
    return gain_map.get(value, 0)

def convert_led_status_to_payload(value):
    led_map = {"On": 0, "Temporarily Off": 1, "Off": 2}
    return led_map.get(value, 0)

def convert_filter_to_payload(value):
    filter_map = {
        "Fast Roll-Off Low Latency": 0,
        "Fast Roll-Off Phase Compensated": 1,
        "Slow Roll-Off Low Latency": 2,
        "Slow Roll-Off Phase Compensated": 3,
        "Non-Oversampling": 4
    }
    return filter_map.get(value, 0)

def convert_filter_payload_to_string(value):
    filter_map = {
        0: "Fast Roll-Off Low Latency",
        1: "Fast Roll-Off Phase Compensated",
        2: "Slow Roll-Off Low Latency",
        3: "Slow Roll-Off Phase Compensated",
        4: "Non-Oversampling"
    }
    return filter_map.get(value, "Invalid Filter Value")