"""This file contain class designed to communicate with mouse."""

import usb.core
import usb.util


class M601:
    """Represents a M601-RGB mouse."""

    def __init__(self):
        """Establish connection with a mouse."""
        self.VID = 0x258a
        self.PID = 0x1007

        self.dev = usb.core.find(idVendor=self.VID, idProduct=self.PID)

        if self.dev is None:
            raise ValueError('Device not found')

        # detach if busy:
        if self.dev.is_kernel_driver_active(1):
            try:
                self.dev.detach_kernel_driver(1)
            except usb.core.USBError as e:
                raise SystemError("Could not detatch kernel driver from interface({0}): {1}".format(1, str(e)))

    def read_settings(self):
        """Read current settings from mouse."""
        self.set_report(0x0305, [5, 1, 0, 0, 0, 0])
        self.get_report(0x0305, 6)
        self.set_report(0x0305, [5, 2, 0, 0, 0, 0])
        self.get_report(0x0305, 6)
        self.set_report(0x0305, [5, 0x11, 0, 0, 0, 0])
        self.settings_1 = self.get_report(0x0304, 520)
        self.set_report(0x0305, [5, 0x12, 0, 0, 0, 0])
        self.buttons_1 = self.get_report(0x0304, 520)
        self.set_report(0x0305, [5, 0x21, 0, 0, 0, 0])
        self.settings_2 = self.get_report(0x0304, 520)
        self.set_report(0x0305, [5, 0x22, 0, 0, 0, 0])
        self.buttons_2 = self.get_report(0x0304, 520)

    def write_settings(self, byte):
        """Write settings to the mouse.

        byte = 0x11 - Mode 1
        byte = 0x21 - Mode 2
        """
        self.set_report(0x0305, [5, byte, 0, 0, 0, 0])
        self.get_report(0x0304, 520)
        self.check_len(self.settings_package, 520)
        self.check_len(self.button_package, 520)
        self.set_report(0x0304, self.button_package)
        self.set_report(0x0304, self.settings_package)

    def parse_settings(self, settings):
        """Parse specific values from settings package."""
        settings = list(settings)
        self.raw_header = settings[0:10]

        self.raw_polling_rate = settings[10]
        self.raw_active_dpi_presets = settings[11]
        self.raw_disabled_dpi_presets = settings[12]
        self.raw_dpi_values = settings[13:18]
        self.raw_dpi_colors = settings[29:44]

        self.raw_current_lighting_effect = settings[53]

        self.raw_colorful_streaming_speed = settings[54]
        self.raw_colorful_streaming_direction = settings[55]

        self.raw_steady_brightness = settings[56]
        self.raw_steady_color = settings[57:60]

        self.raw_breathing_speed = settings[60]
        self.raw_breathing_number_of_colors = settings[61]
        self.raw_breathing_colors = settings[62:83]

        self.raw_tail_speed = settings[83]

        self.raw_neon_speed = settings[84]

        self.raw_colorful_steady_colors = settings[86:101]

        self.raw_flicker_colors = settings[111:117]

        self.raw_streaming_speed = settings[117]

        self.raw_wave_speed = settings[118]

    def parse_buttons(self, buttons):
        """Parse specific values from buttons package."""
        self.buttons_header = buttons[0:8]
        self.button_1 = buttons[8:12]
        self.button_2 = buttons[12:16]
        self.button_3 = buttons[16:20]
        self.button_4 = buttons[24:28]
        self.button_5 = buttons[20:24]
        self.button_6 = buttons[32:36]

    def make_package(self):
        """Make settings and buttons package."""
        self.settings_package = [*self.raw_header,
                                 self.raw_polling_rate,
                                 self.raw_active_dpi_presets,
                                 self.raw_disabled_dpi_presets,
                                 *self.raw_dpi_values,
                                 *[0] * 11, *self.raw_dpi_colors,
                                 *[0] * 9, self.raw_current_lighting_effect,
                                 self.raw_colorful_streaming_speed,
                                 self.raw_colorful_streaming_direction,
                                 self.raw_steady_brightness,
                                 *self.raw_steady_color,
                                 self.raw_breathing_speed,
                                 self.raw_breathing_number_of_colors,
                                 *self.raw_breathing_colors,
                                 self.raw_tail_speed,
                                 self.raw_neon_speed, 0x30,
                                 *self.raw_colorful_steady_colors,
                                 *[0] * 9, 2, *self.raw_flicker_colors,
                                 self.raw_streaming_speed,
                                 self.raw_wave_speed, *[0] * 401]

        disabled_button = [0x50, 0x01, 0, 0]

        self.button_package = [*self.buttons_header,
                               *self.button_1,
                               *self.button_2,
                               *self.button_3,
                               *self.button_5,
                               *self.button_4,
                               0x50, 0x06, 0, 0,
                               *self.button_6,
                               *disabled_button,
                               0x50, 0x06, 0, 0,
                               *disabled_button,
                               *disabled_button,
                               *disabled_button,
                               *disabled_button,
                               *disabled_button,
                               *disabled_button,
                               *disabled_button,
                               *disabled_button,
                               *disabled_button,
                               *disabled_button,
                               *disabled_button,
                               *[0] * 432]

    def set_report(self, wvalue, payload):
        """Send HID report."""
        self.dev.ctrl_transfer(
            0x21,    # bmRequestType
            0x09,    # bRequest
            wvalue,
            1,       # wIndex: 1
            payload  # the HID payload as a byte array
        )

    def get_report(self, wvalue, wlength):
        """Get HID report."""
        return self.dev.ctrl_transfer(
            0xa1,    # bmRequestType
            0x01,    # bRequest
            wvalue,
            1,       # wIndex: 1
            wlength  # the length of expected package to read
        )

    def check_len(self, package, length):
        """Check length of package."""
        if (len(package) != length):
            raise ValueError("Length of package is incorrect.")

    def change_mode(self, mode):
        """Change mouse mode."""
        if mode not in [1, 2]:
            raise ValueError('Wrong mode')
        self.set_report(0x0305, [5, 2, mode, 0, 0, 0])

    def hard_reset(self):
        """Reset mouse values by sending 4 hard coded packages."""
        from values import hard_reset_package_1, hard_reset_package_2, hard_reset_package_3, hard_reset_package_4
        self.set_report(0x0305, [5, 0x11, 0, 0, 0, 0])
        self.get_report(0x0304, 520)
        self.set_report(0x0304, hard_reset_package_2)
        self.set_report(0x0304, hard_reset_package_1)
        self.set_report(0x0305, [5, 0x21, 0, 0, 0, 0])
        self.get_report(0x0304, 520)
        self.set_report(0x0304, hard_reset_package_4)
        self.set_report(0x0304, hard_reset_package_3)
        self.change_mode(1)


if __name__ == '__main__':

    mouse = M601()
    mouse.read_settings()
