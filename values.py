DPI = [500, 800, 1000, 1200, 1600, 2000,
       2400, 3000, 3200, 3500, 4000, 4500,
       5000, 5500, 6000, 7200]

polling_rate = [125, 250, 500, 1000]

buttons_codes = {
    'left': [0x11, 0x01, 0, 0],
    'right': [0x11, 0x02, 0, 0],
    'middle': [0x11, 0x04, 0, 0],
    'back': [0x11, 0x08, 0, 0],
    'forward': [0x11, 0x10, 0, 0],
    'scroll_up': [0x12, 0x01, 0, 0],
    'scroll_down': [0x12, 0xff, 0, 0],
    'key_combination': [0x21, 0, 0, 0],
    'fire_key': [0x31, 0, 0, 0],
    'double_click': [0x31, 0x01, 0x32, 0x02],
    'triple_click': [0x31, 0x01, 0x32, 0x03],
    'dpi_loop': [0x41, 0x00, 0, 0],
    'dpi_up': [0x41, 0x01, 0, 0],
    'dpi_down': [0x41, 0x02, 0, 0],
    'disable_button': [0x50, 0x01, 0, 0],
    'switch_effect': [0x50, 0x07, 0, 0]
}
