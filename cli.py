import argparse
from values import DPI, polling_rate
from main import M601

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--Mode", help = "Switch mouse mode (1-2)")
parser.add_argument("-r", "--Read", 
                    help = "Reads current mouse settings into .ini file",
                    metavar = "FILE")
parser.add_argument("-d", "--Dump", 
                    help = "Reads raw mouse settings into file",
                    metavar = "FILE")
args = parser.parse_args()

mouse = M601()

if args.Mode:
    mouse.change_mode(int(args.Mode))


if args.Dump:
    mouse.read_settings()
    with open(args.Dump, "w") as f:
        f.write(f"{mouse.settings_1} \n {mouse.settings_2} \n")



def make_ini(mode):
    ini = f"""[{mode}]

usb_polling_rate = {polling_rate[mouse.raw_polling_rate - 1]}
active_dpi_preset = {mouse.raw_active_dpi_presets >> 4}

dpi_1 = {DPI[mouse.raw_dpi_values[0] - 1]}
dpi_2 = {DPI[mouse.raw_dpi_values[1] - 1]}
dpi_3 = {DPI[mouse.raw_dpi_values[2] - 1]}
dpi_4 = {DPI[mouse.raw_dpi_values[3] - 1]}
dpi_5 = {DPI[mouse.raw_dpi_values[4] - 1]}

dpi_1_color = {mouse.raw_dpi_colors[0:3]}
dpi_2_color = {mouse.raw_dpi_colors[3:6]}
dpi_3_color = {mouse.raw_dpi_colors[6:9]}
dpi_4_color = {mouse.raw_dpi_colors[9:12]}
dpi_5_color = {mouse.raw_dpi_colors[12:15]}

lighting_effect = {mouse.raw_current_lighting_effect}

colorful_streaming_speed = {mouse.raw_colorful_streaming_speed - 16}
colorufl_streaming_direction = {mouse.raw_colorful_streaming_direction}

steady_brightness = {int(mouse.raw_steady_brightness / 16 * 25)}
steady_color = {mouse.raw_steady_color}

breathing_speed = {mouse.raw_breathing_speed - 48}
breathing_number_of_colors = {mouse.raw_breathing_number_of_colors}
breathing_color_1 = {mouse.raw_breathing_colors[0:3]}
breathing_color_2 = {mouse.raw_breathing_colors[3:6]}
breathing_color_3 = {mouse.raw_breathing_colors[6:9]}
breathing_color_4 = {mouse.raw_breathing_colors[9:12]}
breathing_color_5 = {mouse.raw_breathing_colors[12:15]}
breathing_color_6 = {mouse.raw_breathing_colors[15:18]}
breathing_color_7 = {mouse.raw_breathing_colors[18:21]}

tail_speed = {mouse.raw_tail_speed - 48}

neon_speed = {mouse.raw_neon_speed - 48}

colorful_steady_LED1_color = {mouse.raw_colorful_steady_colors[0:3]}
colorful_steady_LED2_color = {mouse.raw_colorful_steady_colors[3:6]}
colorful_steady_LED3_color = {mouse.raw_colorful_steady_colors[6:9]}
colorful_steady_LED4_color = {mouse.raw_colorful_steady_colors[9:12]}
colorful_steady_LED5_color = {mouse.raw_colorful_steady_colors[12:15]}

streaming_speed = {mouse.raw_streaming_speed - 48}

wave_speed = {mouse.raw_wave_speed - 48}

"""
    return ini

if args.Read:
    mouse.read_settings()
    mouse.parse_settings(mouse.settings_1)
    with open(f"{args.Read}.ini", "w") as f:
        f.write(make_ini("mode_1"))
    mouse.parse_settings(mouse.settings_2)
    with open(f"{args.Read}.ini", "a") as f:
        f.write(make_ini("mode_2"))