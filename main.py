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
        handlers.append(logging.FileHandler(log_config.LOG_FILE))

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
        self.led_toggle.set_active(0)
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
        self.gain.set_active(0)
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
        self.filter.set_active(0)
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
        moondrop.set_volume(value)
        print(f"Volume set to {value}")

    def on_led_toggle_changed(self, combo: Gtk.ComboBoxText) -> None:
        """Handle the LED toggle change event."""
        text = combo.get_active_text()
        self.led_toggle_label.set_text(f"LED Toggle: {text}")
        moondrop.set_led_status(text)
        print(f"LED status set to {text}")

    def on_gain_changed(self, combo: Gtk.ComboBoxText) -> None:
        """Handle the gain selector change event."""
        text = combo.get_active_text()
        self.gain_label.set_text(f"Gain: {text}")
        moondrop.set_gain(text)
        print(f"Gain set to {text}")

    def on_filter_changed(self, combo: Gtk.ComboBoxText) -> None:
        """Handle the filter selector change event."""
        text = combo.get_active_text()
        self.filter_label.set_text(f"Filter: {text}")
        moondrop.set_filter(text)
        print(f"Filter set to {text}")

    def on_refresh_clicked(self, button: Optional[Gtk.Button]) -> None:
        """Handle the refresh button click event."""
        self.gain_label.set_text(f"Gain: {moondrop.get_gain()}")
        self.led_toggle_label.set_text(f"LED Toggle: {moondrop.get_current_led_status()}")
        self.slider.set_value(moondrop.get_current_volume())
        self.filter_label.set_text(f"Filter: {moondrop.get_filter()}")

    def on_save_clicked(self, button: Gtk.Button) -> None:
        """Handle the save settings button click event."""
        try:
            self.config.default_settings.DEFAULT_VOLUME = int(self.slider.get_value())
            self.config.default_settings.DEFAULT_LED_STATUS = self.led_toggle.get_active_text()
            self.config.default_settings.DEFAULT_GAIN = self.gain.get_active_text()
            self.config.default_settings.DEFAULT_FILTER = self.filter.get_active_text()
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
