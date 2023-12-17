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
        print(self.settings_1)
        print(self.settings_2)

    def write_settings(self):
        pass

    def parse_settings(self):
        pass

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
    mouse.change_mode(1)