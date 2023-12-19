import argparse
from main import M601

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--Mode", help = "Switch mouse mode (1-2)")
parser.add_argument("-r", "--Read", 
                    help = "Reads current mouse settings into .ini file",
                    metavar = "INI_FILE")
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
