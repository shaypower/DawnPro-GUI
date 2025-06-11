from dataclasses import dataclass, field
from typing import Dict, List, Optional
import json
import os
from pathlib import Path


@dataclass
class DeviceConstants:
    """Constants for device communication."""
    BM_REQUEST_TYPE_OUT: int = 0x43
    BM_REQUEST_TYPE_IN: int = 0xc3
    B_REQUEST: int = 160
    B_REQUEST_GET: int = 161
    W_VALUE: int = 0x0000
    W_INDEX: int = 0x09a0
    VOLUME_REFRESH_DATA: List[int] = field(default_factory=lambda: [0xC0, 0xA5, 0xA2])
    DATA_LENGTH: int = 7
    LED_STATUS_ENABLED: int = 0
    LED_STATUS_TEMP_OFF: int = 1
    LED_STATUS_OFF: int = 2


@dataclass
class DeviceIdentifiers:
    """Device identification constants."""
    MOONDROP_VID: int = 0x2fc6
    DAWN_PRO_PID: int = 0xf06a
    VOLUME_MAX: int = 0x00
    VOLUME_MIN: int = 0x70


@dataclass
class DefaultSettings:
    """Default settings for the device."""
    DEFAULT_VOLUME: int = 50
    DEFAULT_LED_STATUS: str = "On"
    DEFAULT_GAIN: str = "Low"
    DEFAULT_FILTER: str = "Fast Roll-Off Low Latency"


@dataclass
class UIMetrics:
    """UI-related metrics and settings."""
    WINDOW_WIDTH: int = 400
    WINDOW_HEIGHT: int = 300
    MARGIN_TOP: int = 10
    MARGIN_BOTTOM: int = 20
    MARGIN_START: int = 10
    MARGIN_END: int = 10
    SPACING: int = 10


@dataclass
class LoggingConfig:
    """Logging configuration."""
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(levelname)s - %(message)s"
    LOG_FILE: Optional[str] = None


@dataclass
class AppConfig:
    """Main application configuration."""
    device_constants: DeviceConstants = field(default_factory=DeviceConstants)
    device_identifiers: DeviceIdentifiers = field(default_factory=DeviceIdentifiers)
    default_settings: DefaultSettings = field(default_factory=DefaultSettings)
    ui_metrics: UIMetrics = field(default_factory=UIMetrics)
    logging: LoggingConfig = field(default_factory=LoggingConfig)

    @classmethod
    def load_from_file(cls, config_path: str) -> 'AppConfig':
        """Load configuration from a JSON file.

        Args:
            config_path: Path to the configuration file.

        Returns:
            AppConfig instance with loaded settings.

        Raises:
            FileNotFoundError: If the config file doesn't exist.
            json.JSONDecodeError: If the config file is invalid JSON.
        """
        if not os.path.exists(config_path):
            return cls()

        with open(config_path, 'r') as f:
            config_data = json.load(f)

        return cls(
            device_constants=DeviceConstants(**config_data.get('device_constants', {})),
            device_identifiers=DeviceIdentifiers(**config_data.get('device_identifiers', {})),
            default_settings=DefaultSettings(**config_data.get('default_settings', {})),
            ui_metrics=UIMetrics(**config_data.get('ui_metrics', {})),
            logging=LoggingConfig(**config_data.get('logging', {}))
        )

    def save_to_file(self, config_path: str) -> None:
        """Save current configuration to a JSON file.

        Args:
            config_path: Path where to save the configuration file.

        Raises:
            IOError: If the file cannot be written.
        """
        config_dir = os.path.dirname(config_path)
        if config_dir:
            Path(config_dir).mkdir(parents=True, exist_ok=True)

        config_data = {
            'device_constants': self.device_constants.__dict__,
            'device_identifiers': self.device_identifiers.__dict__,
            'default_settings': self.default_settings.__dict__,
            'ui_metrics': self.ui_metrics.__dict__,
            'logging': self.logging.__dict__
        }

        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=4)

    def get_constants_dict(self) -> Dict[str, any]:
        """Get all constants as a dictionary for device communication.

        Returns:
            Dictionary containing all constants.
        """
        return {
            'BM_REQUEST_TYPE_OUT': self.device_constants.BM_REQUEST_TYPE_OUT,
            'BM_REQUEST_TYPE_IN': self.device_constants.BM_REQUEST_TYPE_IN,
            'B_REQUEST': self.device_constants.B_REQUEST,
            'B_REQUEST_GET': self.device_constants.B_REQUEST_GET,
            'W_VALUE': self.device_constants.W_VALUE,
            'W_INDEX': self.device_constants.W_INDEX,
            'VOLUME_REFRESH_DATA': self.device_constants.VOLUME_REFRESH_DATA,
            'DATA_LENGTH': self.device_constants.DATA_LENGTH,
            'LED_STATUS_ENABLED': self.device_constants.LED_STATUS_ENABLED,
            'LED_STATUS_TEMP_OFF': self.device_constants.LED_STATUS_TEMP_OFF,
            'LED_STATUS_OFF': self.device_constants.LED_STATUS_OFF
        } 