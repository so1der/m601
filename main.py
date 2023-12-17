import usb.core
import usb.util

class M601:
    def __init__(self):
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
        self.set_report([5, 1, 0, 0, 0, 0])
        self.get_report(0x0305, 6)
        self.set_report([5, 2, 0, 0, 0, 0])
        self.get_report(0x0305, 6)
        self.set_report([5, 0x11, 0, 0, 0, 0])
        self.settings_1 = self.get_report(0x0304, 520)
        self.set_report([5, 0x21, 0, 0, 0, 0])
        self.settings_2 = self.get_report(0x0304, 520)
        #print(self.settings_1)
        #print(self.settings_2)

    def write_settings(self):
        pass


    def parse_settings(self, settings):
        self.raw_polling_rate = settings[10]
        self.raw_active_dpi_presets = settings[11]
        self.raw_enabled_dpi_presets = settings[12]
        self.raw_dpi_values = [0] * 5
        for i in range(5):
            self.raw_dpi_values[i] = settings[13 + i]
        self.raw_dpi_colors = [0] * 15
        for i in range(15):
            self.raw_dpi_colors[i] = settings[29 + i]

        self.raw_current_lighting_effect = settings[53]

        self.raw_colorful_streaming_speed = settings[54]
        self.raw_colorful_streaming_direction = settings[55]

        self.raw_steady_brightness = settings[56]
        self.raw_steady_color = [0] * 3
        for i in range(3):
            self.raw_steady_color[i] = settings[57 + i]

        self.raw_breathing_speed = settings[60]
        self.raw_breathing_number_of_colors = settings[61]
        self.raw_breathing_colors = [0] * 21
        for i in range(21):
            self.breathing_colors[i] = settings[62 + i]

        self.raw_tail_speed = settings[83]

        self.raw_neon_speed = settings[84]

        self.raw_colorful_steady_colors = [0] * 15
        for i in range(15):
            self.raw_colorful_steady_colors[i] = settings[86 + i]

        self.raw_streaming_speed = settings[117]

        self.raw_wave_speed = settings[118]


    def make_package(self):
        pass

    def set_report(self, payload):
        self.dev.ctrl_transfer(
            0x21,   # bmRequestType
            0x09,   # bRequest
            0x0305, # ReportID:5, ReportType:3 (Feature) 
            1,      # wIndex: 1
            payload # the HID payload as a byte array
        )

    def get_report(self, wValue, wLength):
        return self.dev.ctrl_transfer(
            0xa1,   # bmRequestType
            0x01,   # bRequest
            wValue,
            1,      # wIndex: 1
            wLength # the length of expected package to read
        )

    def change_mode(self, mode):
        if mode not in [1, 2]:
            raise ValueError('Wrong mode')
        self.set_report([5, 2, mode, 0, 0, 0])


if __name__ == '__main__':

    mouse = M601()
    mouse.read_settings()
    mouse.parse_settings(mouse.settings_2)