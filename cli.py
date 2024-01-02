import argparse
import configparser
from values import DPI, polling_rate, buttons_codes
from main import M601

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--Mode", help = "Switch mouse mode (1-2)")
parser.add_argument("-r", "--Read", 
                    help = "Reads current mouse settings into .ini file",
                    metavar = "FILE")
parser.add_argument("--hard_reset", 
                    help = """Writes hard coded reset packages into mouse.
                    Can help if mouse stopped responding """,
                    action='store_true')
parser.add_argument("-d", "--Dump", 
                    help = "Reads raw mouse settings into file",
                    metavar = "FILE")
parser.add_argument("-w", "--Write",
                    help = "Writes settings from .ini file into mouse",
                    metavar = "FILE")

args = parser.parse_args()

mouse = M601()

if args.Mode:
    mouse.change_mode(int(args.Mode))

if args.Dump:
    mouse.read_settings()
    with open(args.Dump, "w") as f:
        f.write(f"{mouse.settings_1} \n{mouse.buttons_1} \n{mouse.settings_2} \n{mouse.buttons_2} \n")



def make_ini(mode):
    ini = f"""[{mode}]
; This parameter sets the USB polling rate.
; Possible value for this mouse is 125, 250, 500, or 1000 Hz
usb_polling_rate = {polling_rate[mouse.raw_polling_rate - 1]}

; This parameter sets active DPI preset among enabled presets
; Note: This is not a preset number, it is it sequence number between enabled presets.
active_dpi_preset = {mouse.raw_active_dpi_presets >> 4}

; This parameter disables certain DPI presets, in order: 1 2 3 4 5
; where 0 - preset is enabled, 1 - preset is disabled
; for example, if you want to disable 4 and 3 DPI preset:
; disabled_dpi_presets = 00110
; if you want to disable only 1 preset:
; 10000
disabled_dpi_presets = {"{0:b}".format(mouse.raw_disabled_dpi_presets)[3:8][::-1]}

; These parameters are setting certain DPI values for certain DPI presets
; Possible DPI values for this mouse are:
; 500, 800, 1000, 1200, 1600, 2000, 2400, 3000, 3200, 3500, 4000, 4500,
; 5000, 5500, 6000, 7200.
dpi_1 = {DPI[mouse.raw_dpi_values[0] - 1]}
dpi_2 = {DPI[mouse.raw_dpi_values[1] - 1]}
dpi_3 = {DPI[mouse.raw_dpi_values[2] - 1]}
dpi_4 = {DPI[mouse.raw_dpi_values[3] - 1]}
dpi_5 = {DPI[mouse.raw_dpi_values[4] - 1]}

; These parameters are setting certain colors for certain DPI presets
; You will see these colors when switching between presets
; [Red, Green, Blue]
; Possible values are 0-255
dpi_1_color = {mouse.raw_dpi_colors[0:3]}
dpi_2_color = {mouse.raw_dpi_colors[3:6]}
dpi_3_color = {mouse.raw_dpi_colors[6:9]}
dpi_4_color = {mouse.raw_dpi_colors[9:12]}
dpi_5_color = {mouse.raw_dpi_colors[12:15]}

; These parameters are setting certain mouse buttons
; Possible values: left, right, middle, back, forward,
; scroll_up, scroll_down, double_click, triple_click,
; dpi_loop, dpi_up, dpi_down, disable_button, switch_effect
button_1 = {list(buttons_codes.keys())[list(buttons_codes.values()).index(list(mouse.button_1))]}
button_2 = {list(buttons_codes.keys())[list(buttons_codes.values()).index(list(mouse.button_2))]}
button_3 = {list(buttons_codes.keys())[list(buttons_codes.values()).index(list(mouse.button_3))]}
button_4 = {list(buttons_codes.keys())[list(buttons_codes.values()).index(list(mouse.button_4))]}
button_5 = {list(buttons_codes.keys())[list(buttons_codes.values()).index(list(mouse.button_5))]}
button_6 = {list(buttons_codes.keys())[list(buttons_codes.values()).index(list(mouse.button_6))]}

; This parameter sets the current lighting effect:
; 0 = None
; 1 = Colorful Streaming
; 2 = Steady
; 3 = Breathing
; 4 = Tail
; 5 = Neon
; 6 = Colorful Steady
; 7 = Flicker
; 8 = Streaming
; 9 = Wave
lighting_effect = {mouse.raw_current_lighting_effect}

; This parameter sets speed for the "Colorful Streaming" lighting effect
; Possible values are 1-3
colorful_streaming_speed = {mouse.raw_colorful_streaming_speed - 16}
; This parameter sets the direction for the "Colorful Streaming" lighting effect
; 0 = Backward, 1 = Forward
colorful_streaming_direction = {mouse.raw_colorful_streaming_direction}

; This parameter sets brightness for the "Steady" lighting effect
; Possible values are 25, 50, 75 or 100
steady_brightness = {int(mouse.raw_steady_brightness / 16 * 25)}
; This parameter sets color for the "Steady" lighting effect
; [Red, Green, Blue]
; Possible values are 0-255
steady_color = {mouse.raw_steady_color}

; This parameter sets speed for the "Breathing" lighting effect
; Possible values are 1-3
breathing_speed = {mouse.raw_breathing_speed - 48}
; This parameter sets amount of colors for the "Breathing" lighting effect
; Possible values are 1-7
breathing_number_of_colors = {mouse.raw_breathing_number_of_colors}
; These parameters are setting colors for the "Breathing" lighting effect
; [Red, Green, Blue]
; Possible values are 0-255
; Unused colors should be set as [0, 0, 0]
breathing_color_1 = {mouse.raw_breathing_colors[0:3]}
breathing_color_2 = {mouse.raw_breathing_colors[3:6]}
breathing_color_3 = {mouse.raw_breathing_colors[6:9]}
breathing_color_4 = {mouse.raw_breathing_colors[9:12]}
breathing_color_5 = {mouse.raw_breathing_colors[12:15]}
breathing_color_6 = {mouse.raw_breathing_colors[15:18]}
breathing_color_7 = {mouse.raw_breathing_colors[18:21]}

; This parameter sets speed for the "Tail" lighting effect
; Possible values are 1-3
tail_speed = {mouse.raw_tail_speed - 48}

; This parameter sets speed for the "Neon" lighting effect
; Possible values are 1-3
neon_speed = {mouse.raw_neon_speed - 48}

; These parameters are setting colors for certain LEDs in the "Colorful Steady" lighting effect
; [Red, Green, Blue]
; Possible values are 0-255
; You can disable certain LED by set it as [0, 0, 0]
colorful_steady_LED1_color = {mouse.raw_colorful_steady_colors[0:3]}
colorful_steady_LED2_color = {mouse.raw_colorful_steady_colors[3:6]}
colorful_steady_LED3_color = {mouse.raw_colorful_steady_colors[6:9]}
colorful_steady_LED4_color = {mouse.raw_colorful_steady_colors[9:12]}
colorful_steady_LED5_color = {mouse.raw_colorful_steady_colors[12:15]}

; These parameters are setting colors for the "Flicker" lighting effect
; [Red, Green, Blue]
; Possible values are 0-255
flicker_color_1 = {mouse.raw_flicker_colors[0:3]}
flicker_color_2 = {mouse.raw_flicker_colors[3:6]}

; This parameter sets the speed for the "Streaming" lighting effect
; Possible values are 1-3
streaming_speed = {mouse.raw_streaming_speed - 48}

; This parameter sets speed for the "Wave" lighting effect
; Possible values are 1-3
wave_speed = {mouse.raw_wave_speed - 48}

"""
    return ini

if args.Read:
    mouse.read_settings()
    mouse.parse_settings(mouse.settings_1)
    mouse.parse_buttons(mouse.buttons_1)
    with open(f"{args.Read}.ini", "w") as f:
        f.write(make_ini("mode_1"))
    mouse.parse_settings(mouse.settings_2)
    mouse.parse_buttons(mouse.buttons_2)
    with open(f"{args.Read}.ini", "a") as f:
        f.write(make_ini("mode_2"))

def parse_ini(mode):
    mouse.raw_polling_rate = polling_rate.index(int(mode['usb_polling_rate'])) + 1
    mouse.raw_active_dpi_presets = int(f"{mode['active_dpi_preset']}{mode['disabled_dpi_presets'].count('0')}", 16)
    mouse.raw_disabled_dpi_presets = int(mode['disabled_dpi_presets'][::-1], 2) + 224
    for i in range(5):
        mouse.raw_dpi_values[i] = DPI.index(int(mode[f'dpi_{i + 1}'])) + 1
    dpi_colors = ""
    for i in range(5):
        dpi_colors += mode[f'dpi_{i + 1}_color']
    dpi_colors = dpi_colors.replace("][", ",").replace("[", "").replace("]", "")
    dpi_colors = dpi_colors.split(",")
    for i in range(15):
        mouse.raw_dpi_colors[i] = int(dpi_colors[i])
    mouse.raw_current_lighting_effect = int(mode['lighting_effect'])
    mouse.raw_colorful_streaming_speed = int(mode['colorful_streaming_speed']) + 16
    mouse.raw_colorful_streaming_direction = int(mode['colorful_streaming_direction'])
    mouse.raw_steady_brightness = int(int(mode['steady_brightness']) * 16 / 25)
    steady_color = mode['steady_color']
    steady_color = steady_color.replace("[", "").replace("]", "")
    steady_color = steady_color.split(",")
    for i in range(3):
        mouse.raw_steady_color[i] = int(steady_color[i])
    mouse.raw_breathing_speed = int(mode['breathing_speed']) + 48
    mouse.raw_breathing_number_of_colors = int(mode['breathing_number_of_colors'])
    breathing_colors = ""
    for i in range(7):
        breathing_colors += mode[f'breathing_color_{i+1}']
    breathing_colors = breathing_colors.replace("][", ",").replace("[", "").replace("]", "")
    breathing_colors = breathing_colors.split(",")
    for i in range(21):
        mouse.raw_breathing_colors[i] = int(breathing_colors[i])
    mouse.raw_tail_speed = int(mode['tail_speed']) + 48
    mouse.raw_neon_speed = int(mode['neon_speed']) + 48
    colorful_steady_colors = ""
    for i in range(5):
        colorful_steady_colors += mode[f'colorful_steady_LED{i + 1}_color']
    colorful_steady_colors = colorful_steady_colors.replace("][", ",").replace("[", "").replace("]", "")
    colorful_steady_colors = colorful_steady_colors.split(",")
    for i in range(15):
        mouse.raw_colorful_steady_colors[i] = int(colorful_steady_colors[i])
    flicker_colors = ""
    for i in range(2):
        flicker_colors += mode[f'flicker_color_{i + 1}']
    flicker_colors = flicker_colors.replace("][", ",").replace("[", "").replace("]", "")
    flicker_colors = flicker_colors.split(",")
    for i in range(6):
        mouse.raw_flicker_colors[i] = int(flicker_colors[i])
    mouse.raw_streaming_speed = int(mode['streaming_speed']) + 48
    mouse.raw_wave_speed = int(mode['wave_speed']) + 48

    mouse.button_1 = buttons_codes[mode['button_1']]
    mouse.button_2 = buttons_codes[mode['button_2']]
    mouse.button_3 = buttons_codes[mode['button_3']]
    mouse.button_4 = buttons_codes[mode['button_4']]
    mouse.button_5 = buttons_codes[mode['button_5']]
    mouse.button_6 = buttons_codes[mode['button_6']]


if args.Write:
    mouse.read_settings()
    config = configparser.ConfigParser()
    config.read(args.Write)
    config_1 = config['mode_1']
    config_2 = config['mode_2']
    mouse.parse_settings(mouse.settings_1)
    mouse.parse_buttons(mouse.buttons_1)
    parse_ini(config_1)
    mouse.make_package()
    mouse.write_settings(0x11)
    mouse.parse_settings(mouse.settings_2)
    mouse.parse_buttons(mouse.buttons_2)
    parse_ini(config_2)
    mouse.make_package()
    mouse.write_settings(0x21)


if args.hard_reset:
    mouse.hard_reset()
