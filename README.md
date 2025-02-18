# DawnPro-Utils
DawnPro-Utils is a tool used to control the Moondrop Dawn Pro AMP/DAC.

![screenshot](preview.png)

## Features

- Change the LED status (on, temp-off, off)
- Set the gain (low, high)
- Configure the filters:
    - Fast-roll-off-low-latency
    - Fast-roll-off-phase-compensated
    - Slow-roll-off-low-latency
    - Slow-roll-off-phase-compensated
    - Non-oversampling
- Adjust the volume

## Requirements

- Python
- `usb` module
- `PyGObject`

## Installation

To install pyusb, run:

```sh
pip install pyusb
```

To install PyGObject, it may depend on your distro or operating system:

https://pygobject.gnome.org/

## Setup

Add the following rule to your udev rules (you may need to adjust the rule name based on existing rules in `/etc/udev/rules.d/`):

```sh
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="2fc6", MODE="0666"' | sudo tee /etc/udev/rules.d/99-dawn-pro.rules
```

Then run:

```sh
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Usage

Ensure the DAC/AMP is plugged in before running the script.

To run the tool, execute the following command:

```sh
python main.py
```

## Acknowledgments
Inspired by:

"mdrop" by frahz: https://github.com/frahz/mdrop/
