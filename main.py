import gi
from typing import Optional
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from device.moondrop import Moondrop
from device.config import AppConfig
import sys
import os
import logging


def setup_logging(config: AppConfig) -> None:
    """Set up logging configuration.

    Args:
        config: Application configuration instance.
    """
    log_config = config.logging
    handlers = [logging.StreamHandler()]

    if log_config.LOG_FILE:
        # Expand ~ in log file path
        log_file_path = os.path.expanduser(log_config.LOG_FILE)
        # Create log directory if it doesn't exist
        log_dir = os.path.dirname(log_file_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        handlers.append(logging.FileHandler(log_file_path))

    logging.basicConfig(
        level=getattr(logging, log_config.LOG_LEVEL),
        format=log_config.LOG_FORMAT,
        handlers=handlers
    )


def show_error_dialog(message: str) -> None:
    """Display an error dialog with the given message.

    Args:
        message: The error message to display.
    """
    dialog = Gtk.MessageDialog(
        parent=None,
        flags=0,
        message_type=Gtk.MessageType.ERROR,
        buttons=Gtk.ButtonsType.CLOSE,
        text=message
    )
    dialog.run()
    dialog.destroy()


def show_success_dialog(message: str) -> None:
    """Display a success dialog with the given message.

    Args:
        message: The success message to display.
    """
    dialog = Gtk.MessageDialog(
        parent=None,
        flags=0,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.CLOSE,
        text=message
    )
    dialog.run()
    dialog.destroy()


def load_config() -> AppConfig:
    """Load application configuration.

    Returns:
        AppConfig instance with loaded settings.
    """
    config_path = os.path.expanduser('~/.config/dawnpro/config.json')
    return AppConfig.load_from_file(config_path)


# Load configuration
config = load_config()
setup_logging(config)

try:
    moondrop = Moondrop(config)
except ValueError as err:
    show_error_dialog(str(err))
    sys.exit(1)


class ModernGUI(Gtk.Window):
    """Main GUI window for the Moondrop Dawn Pro Control application."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize the GUI window and its components.

        Args:
            config: Application configuration instance.
        """
        super().__init__(title="Moondrop Dawn Pro Control")
        self.config = config
        self.set_default_size(
            config.ui_metrics.WINDOW_WIDTH,
            config.ui_metrics.WINDOW_HEIGHT
        )

        self.vbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=config.ui_metrics.SPACING
        )
        self.vbox.set_margin_top(config.ui_metrics.MARGIN_TOP)
        self.vbox.set_margin_bottom(config.ui_metrics.MARGIN_BOTTOM)
        self.vbox.set_margin_start(config.ui_metrics.MARGIN_START)
        self.vbox.set_margin_end(config.ui_metrics.MARGIN_END)
        self.add(self.vbox)

        self.create_volume_slider()
        self.create_led_toggle()
        self.create_gain_selector()
        self.create_filter_selector()
        self.create_button_box()

        # Apply saved settings to device if config file exists, then refresh UI
        config_path = os.path.expanduser('~/.config/dawnpro/config.json')
        if os.path.exists(config_path):
            self.apply_saved_settings()
        self.on_refresh_clicked(None)

    def create_volume_slider(self) -> None:
        """Create and configure the volume slider."""
        self.slider = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 60, 1)
        self.slider.set_value(self.config.default_settings.DEFAULT_VOLUME)
        self.slider.set_margin_bottom(self.config.ui_metrics.MARGIN_BOTTOM)
        self.vbox.pack_start(self.slider, True, True, 0)
        self.slider.connect("value-changed", self.on_slider_value_changed)

    def create_led_toggle(self) -> None:
        """Create and configure the LED toggle."""
        self.led_toggle_label = Gtk.Label(
            label=f"LED Toggle: {self.config.default_settings.DEFAULT_LED_STATUS}"
        )
        self.led_toggle_label.set_margin_top(self.config.ui_metrics.MARGIN_TOP)
        self.vbox.pack_start(self.led_toggle_label, True, True, 0)
        self.led_toggle = Gtk.ComboBoxText()
        self.led_toggle.append_text("On")
        self.led_toggle.append_text("Temporarily Off")
        self.led_toggle.append_text("Off")
        # Set active based on loaded default
        led_map = {"On": 0, "Temporarily Off": 1, "Off": 2}
        self.led_toggle.set_active(led_map.get(self.config.default_settings.DEFAULT_LED_STATUS, 0))
        self.led_toggle.set_margin_bottom(self.config.ui_metrics.MARGIN_BOTTOM)
        self.vbox.pack_start(self.led_toggle, True, True, 0)
        self.led_toggle.connect("changed", self.on_led_toggle_changed)

    def create_gain_selector(self) -> None:
        """Create and configure the gain selector."""
        self.gain_label = Gtk.Label(
            label=f"Gain: {self.config.default_settings.DEFAULT_GAIN}"
        )
        self.gain_label.set_margin_top(self.config.ui_metrics.MARGIN_TOP)
        self.vbox.pack_start(self.gain_label, True, True, 0)
        self.gain = Gtk.ComboBoxText()
        self.gain.append_text("Low")
        self.gain.append_text("High")
        # Set active based on loaded default
        self.gain.set_active(0 if self.config.default_settings.DEFAULT_GAIN == "Low" else 1)
        self.gain.set_margin_bottom(self.config.ui_metrics.MARGIN_BOTTOM)
        self.vbox.pack_start(self.gain, True, True, 0)
        self.gain.connect("changed", self.on_gain_changed)

    def create_filter_selector(self) -> None:
        """Create and configure the filter selector."""
        self.filter_label = Gtk.Label(
            label=f"Filter: {self.config.default_settings.DEFAULT_FILTER}"
        )
        self.filter_label.set_margin_top(self.config.ui_metrics.MARGIN_TOP)
        self.vbox.pack_start(self.filter_label, True, True, 0)
        self.filter = Gtk.ComboBoxText()
        self.filter.append_text("Fast Roll-Off Low Latency")
        self.filter.append_text("Fast Roll-Off Phase Compensated")
        self.filter.append_text("Slow Roll-Off Low Latency")
        self.filter.append_text("Slow Roll-Off Phase Compensated")
        self.filter.append_text("Non-Oversampling")
        # Set active based on loaded default
        filter_map = {
            "Fast Roll-Off Low Latency": 0,
            "Fast Roll-Off Phase Compensated": 1,
            "Slow Roll-Off Low Latency": 2,
            "Slow Roll-Off Phase Compensated": 3,
            "Non-Oversampling": 4
        }
        self.filter.set_active(filter_map.get(self.config.default_settings.DEFAULT_FILTER, 0))
        self.filter.set_margin_bottom(self.config.ui_metrics.MARGIN_BOTTOM)
        self.vbox.pack_start(self.filter, True, True, 0)
        self.filter.connect("changed", self.on_filter_changed)

    def create_button_box(self) -> None:
        """Create and configure the button box with refresh and save buttons."""
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_margin_top(self.config.ui_metrics.MARGIN_TOP)
        self.refresh_button = Gtk.Button(label="Refresh")
        self.refresh_button.connect("clicked", self.on_refresh_clicked)
        button_box.pack_start(self.refresh_button, True, True, 0)
        self.save_button = Gtk.Button(label="Save Settings")
        self.save_button.connect("clicked", self.on_save_clicked)
        button_box.pack_start(self.save_button, True, True, 0)
        self.vbox.pack_start(button_box, True, True, 0)

    def on_slider_value_changed(self, slider: Gtk.Scale) -> None:
        """Handle the volume slider value change event."""
        value = int(slider.get_value())
        if not moondrop.set_volume(value):
            show_error_dialog(f"Failed to set volume to {value}")
            logging.error(f"Failed to set volume to {value}")
        else:
            logging.info(f"Volume set to {value}")

    def on_led_toggle_changed(self, combo: Gtk.ComboBoxText) -> None:
        """Handle the LED toggle change event."""
        text = combo.get_active_text()
        self.led_toggle_label.set_text(f"LED Toggle: {text}")
        if not moondrop.set_led_status(text):
            show_error_dialog(f"Failed to set LED status to {text}")
            logging.error(f"Failed to set LED status to {text}")
        else:
            logging.info(f"LED status set to {text}")

    def on_gain_changed(self, combo: Gtk.ComboBoxText) -> None:
        """Handle the gain selector change event."""
        text = combo.get_active_text()
        self.gain_label.set_text(f"Gain: {text}")
        if not moondrop.set_gain(text):
            show_error_dialog(f"Failed to set gain to {text}")
            logging.error(f"Failed to set gain to {text}")
        else:
            logging.info(f"Gain set to {text}")

    def on_filter_changed(self, combo: Gtk.ComboBoxText) -> None:
        """Handle the filter selector change event."""
        text = combo.get_active_text()
        self.filter_label.set_text(f"Filter: {text}")
        if not moondrop.set_filter(text):
            show_error_dialog(f"Failed to set filter to {text}")
            logging.error(f"Failed to set filter to {text}")
        else:
            logging.info(f"Filter set to {text}")

    def apply_saved_settings(self) -> None:
        """Apply saved settings from config to the device."""
        try:
            # Apply volume
            volume = self.config.default_settings.DEFAULT_VOLUME
            if volume is not None:
                moondrop.set_volume(volume)
                logging.info(f"Applied saved volume: {volume}")
            
            # Apply LED status
            led_status = self.config.default_settings.DEFAULT_LED_STATUS
            if led_status:
                moondrop.set_led_status(led_status)
                logging.info(f"Applied saved LED status: {led_status}")
            
            # Apply gain
            gain = self.config.default_settings.DEFAULT_GAIN
            if gain:
                moondrop.set_gain(gain)
                logging.info(f"Applied saved gain: {gain}")
            
            # Apply filter
            filter_type = self.config.default_settings.DEFAULT_FILTER
            if filter_type:
                moondrop.set_filter(filter_type)
                logging.info(f"Applied saved filter: {filter_type}")
        except Exception as e:
            logging.warning(f"Failed to apply some saved settings: {e}")

    def on_refresh_clicked(self, button: Optional[Gtk.Button]) -> None:
        """Handle the refresh button click event."""
        # Get current device state
        current_gain = moondrop.get_gain()
        current_led = moondrop.get_current_led_status()
        current_volume = moondrop.get_current_volume()
        current_filter = moondrop.get_filter()
        
        # Update labels
        if current_gain:
            self.gain_label.set_text(f"Gain: {current_gain}")
            # Sync combo box: "Low" = 0, "High" = 1
            self.gain.set_active(0 if current_gain == "Low" else 1)
        
        if current_led:
            self.led_toggle_label.set_text(f"LED Toggle: {current_led}")
            # Sync combo box: "On" = 0, "Temporarily Off" = 1, "Off" = 2
            led_map = {"On": 0, "Temporarily Off": 1, "Off": 2}
            self.led_toggle.set_active(led_map.get(current_led, 0))
        
        if current_volume is not None:
            self.slider.set_value(current_volume)
        
        if current_filter:
            self.filter_label.set_text(f"Filter: {current_filter}")
            # Sync combo box
            filter_map = {
                "Fast Roll-Off Low Latency": 0,
                "Fast Roll-Off Phase Compensated": 1,
                "Slow Roll-Off Low Latency": 2,
                "Slow Roll-Off Phase Compensated": 3,
                "Non-Oversampling": 4
            }
            self.filter.set_active(filter_map.get(current_filter, 0))

    def on_save_clicked(self, button: Gtk.Button) -> None:
        """Handle the save settings button click event."""
        try:
            # Get current values from UI
            volume = int(self.slider.get_value())
            led_status = self.led_toggle.get_active_text()
            gain = self.gain.get_active_text()
            filter_type = self.filter.get_active_text()
            
            # Validate values are not None
            if led_status is None or gain is None or filter_type is None:
                show_error_dialog("Cannot save: Some settings are not selected")
                logging.error("Attempted to save with None values")
                return
            
            # Update config
            self.config.default_settings.DEFAULT_VOLUME = volume
            self.config.default_settings.DEFAULT_LED_STATUS = led_status
            self.config.default_settings.DEFAULT_GAIN = gain
            self.config.default_settings.DEFAULT_FILTER = filter_type
            
            # Save to file
            config_path = os.path.expanduser('~/.config/dawnpro/config.json')
            self.config.save_to_file(config_path)

            show_success_dialog("Settings saved successfully!")
            logging.info("Settings saved to configuration file")
        except Exception as e:
            error_msg = f"Failed to save settings: {str(e)}"
            show_error_dialog(error_msg)
            logging.error(error_msg)


win = ModernGUI(config)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
