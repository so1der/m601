import argparse
from main import M601

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--Mode", help = "Switch mouse mode (1-2)")
args = parser.parse_args()

if args.Mode:
    mouse = M601()
    mouse.change_mode(int(args.Mode))