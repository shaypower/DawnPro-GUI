import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from device.moondrop import Moondrop

moondrop = Moondrop()

class ModernGUI(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Moondrop Dawn Pro Control")
        self.set_default_size(400, 300)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.vbox.set_margin_top(10)
        self.vbox.set_margin_bottom(20)
        self.vbox.set_margin_start(10)
        self.vbox.set_margin_end(10)
        self.add(self.vbox)

        # Volume
        self.slider = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
        self.slider.set_value(50)
        self.slider.set_margin_bottom(10)
        self.vbox.pack_start(self.slider, True, True, 0)
        self.slider.connect("value-changed", self.on_slider_value_changed)

        # LED
        self.led_toggle_label = Gtk.Label(label="LED Toggle: On")
        self.led_toggle_label.set_margin_top(10)
        self.vbox.pack_start(self.led_toggle_label, True, True, 0)
        self.led_toggle = Gtk.ComboBoxText()
        self.led_toggle.append_text("On")
        self.led_toggle.append_text("Temporarily Off")
        self.led_toggle.append_text("Off")
        self.led_toggle.set_active(0)
        self.led_toggle.set_margin_bottom(10)
        self.vbox.pack_start(self.led_toggle, True, True, 0)
        self.led_toggle.connect("changed", self.on_led_toggle_changed)

        # Gain
        self.gain_label = Gtk.Label(label="Gain: Low")
        self.gain_label.set_margin_top(10)
        self.vbox.pack_start(self.gain_label, True, True, 0)
        self.gain = Gtk.ComboBoxText()
        self.gain.append_text("Low")
        self.gain.append_text("High")
        self.gain.set_active(0)
        self.gain.set_margin_bottom(10)
        self.vbox.pack_start(self.gain, True, True, 0)
        self.gain.connect("changed", self.on_gain_changed)

        # Filter
        self.filter_label = Gtk.Label(label="Filter: Fast Roll-Off Low Latency")
        self.filter_label.set_margin_top(10)
        self.vbox.pack_start(self.filter_label, True, True, 0)
        self.filter = Gtk.ComboBoxText()
        self.filter.append_text("Fast Roll-Off Low Latency")
        self.filter.append_text("Fast Roll-Off Phase Compensated")
        self.filter.append_text("Slow Roll-Off Low Latency")
        self.filter.append_text("Slow Roll-Off Phase Compensated")
        self.filter.append_text("Non-Oversampling")
        self.filter.set_active(0)
        self.filter.set_margin_bottom(10)
        self.vbox.pack_start(self.filter, True, True, 0)
        self.filter.connect("changed", self.on_filter_changed)

        # Refresh
        self.refresh_button = Gtk.Button(label="Refresh")
        self.refresh_button.set_margin_top(20)
        self.refresh_button.connect("clicked", self.on_refresh_clicked)
        self.vbox.pack_start(self.refresh_button, True, True, 0)

        self.on_refresh_clicked(None)

    def on_slider_value_changed(self, slider):
        value = int(slider.get_value())
        moondrop.set_volume(value)
        print(f"Volume set to {value}")

    def on_led_toggle_changed(self, combo):
        text = combo.get_active_text()
        self.led_toggle_label.set_text(f"LED Toggle: {text}")
        moondrop.set_led_status(text)
        print(f"LED status set to {text}")

    def on_gain_changed(self, combo):
        text = combo.get_active_text()
        self.gain_label.set_text(f"Gain: {text}")
        moondrop.set_gain(text)
        print(f"Gain set to {text}")

    def on_filter_changed(self, combo):
        text = combo.get_active_text()
        self.filter_label.set_text(f"Filter: {text}")
        moondrop.set_filter(text)
        print(f"Filter set to {text}")

    def on_refresh_clicked(self, button):
        self.gain_label.set_text(f"Gain: {moondrop.get_gain()}")
        self.led_toggle_label.set_text(f"LED Toggle: {moondrop.get_current_led_status()}")
        self.slider.set_value(moondrop.get_current_volume())
        self.filter_label.set_text(f"Filter: {moondrop.get_filter()}")

win = ModernGUI()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

