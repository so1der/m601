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
        self.dev.ctrl_transfer(
            0x21,   # bmRequestType
            0x09,   # bRequest
            0x0305, # ReportID:5, ReportType:3 (Feature) 
            1,      # wIndex: 1
            [5, 1, 0, 0, 0, 0] # the HID payload as a byte array
        )
        self.dev.ctrl_transfer(
            0xa1,   # bmRequestType
            0x01,   # bRequest
            0x0305, # ReportID:5, ReportType:3 (Feature) 
            1,      # wIndex: 1
            6 # the HID payload as a byte array
        )
        self.dev.ctrl_transfer(
            0x21,   # bmRequestType
            0x09,   # bRequest
            0x0305, # ReportID:5, ReportType:3 (Feature) 
            1,      # wIndex: 1
            [5, 2, 0, 0, 0, 0] # the HID payload as a byte array
        )
        self.dev.ctrl_transfer(
            0xa1,   # bmRequestType
            0x01,   # bRequest
            0x0305, # ReportID:5, ReportType:3 (Feature) 
            1,      # wIndex: 1
            6 # the HID payload as a byte array
        )
        self.dev.ctrl_transfer(
            0x21,   # bmRequestType
            0x09,   # bRequest
            0x0305, # ReportID:5, ReportType:3 (Feature) 
            1,      # wIndex: 1
            [5, 0x11, 0, 0, 0, 0] # the HID payload as a byte array
        )
        self.settings_1 = self.dev.ctrl_transfer(
            0xa1,   # bmRequestType
            0x01,   # bRequest
            0x0304, # ReportID:5, ReportType:3 (Feature) 
            1,      # wIndex: 1
            520 # the HID payload as a byte array
        )
        self.dev.ctrl_transfer(
            0x21,   # bmRequestType
            0x09,   # bRequest
            0x0305, # ReportID:5, ReportType:3 (Feature) 
            1,      # wIndex: 1
            [5, 0x21, 0, 0, 0, 0] # the HID payload as a byte array
        )
        self.settings_2 = self.dev.ctrl_transfer(
            0xa1,   # bmRequestType
            0x01,   # bRequest
            0x0304, # ReportID:5, ReportType:3 (Feature) 
            1,      # wIndex: 1
            520 # the HID payload as a byte array
        )
        print(self.settings_1)
        print(self.settings_2)

    def write_settings(self):
        pass

    def parse_settings(self):
        pass

    def make_package(self):
        pass

    def send_package(self):
        pass

    def get_package(self):
        pass


if __name__ == '__main__':

    mouse = M601()
    mouse.read_settings()