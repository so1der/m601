This Python script allows you to control the Redragon M601 gaming mouse from your terminal!

**Disclaimer: This software is not supported by the manufacturer of the hardware in any way, and relies completely on information from reverse-engineering. There is no warranty, especially in case of damage to the hardware**

First of all, make sure that the VID and PID of your mouse match these: "258a:1007"
You can check it by executing the following command in your terminal:
```bash
lsusb
```
You'll get similar output:
```bash
Bus 001 Device 008: ID 258a:1007 SINOWEALTH Wired Gaming Mouse
```
If your VID:PID didn't match 258a:1007, or you have a different mouse from Redragon, you can check [mouse_m908](https://github.com/dokutan/mouse_m908) repository from [dokutan](https://github.com/dokutan). 

After you ensured that VID:PID of your mouse is correct, you can try to change mouse mode:
```bash
python cli.py -m 1
python cli.py -m 2
```
If the mouse did respond, congratulations! It means your mouse is likely supported by this software!

# First steps
First of all, you need to clone this repository to your machine:
```bash
git clone https://github.com/so1der/m601
cd m601
```
After that, you need to make a virtual environment:
```bash
python -m venv venv
```
And activate it:
```bash
source venv/bin/activate
```
Now you can install the main requirement of this script - python library [PyUSB](https://pypi.org/project/pyusb/) by executing the command:
```bash
pip install pyusb
```
or
```bash
pip install -r requirements.txt
```
Now you can use it!
```bash
python cli.py -h
```
But before that, you may need to add VID and PID into udev rules. To do so, go to /etc/udev/rules.d/ and create the file "99-m601.rules", and add there via nano following line:
```text
SUBSYSTEM=="usb", ATTRS{idVendor}=="258a", ATTRS{idProduct}=="1007", MODE="0666"
```
```bash
cd /etc/udev/rules.d/
touch 99-m601.rules
nano 99-m601.rules
```
# Compiling
But once you close your terminal, the environment will be deactivated. In order not to activate the virtual environment every time you need to change something in your mouse, you can simply compile the executable binary file and put it in your /usr/local/bin directory. To do so, you need to install PyInstaller:
```bash
pip install pyinstaller
```
And now you can compile executable file from cli.py file, in this case, pyinstaller will collect all requirements by itself:
```bash
pyinstaller --onefile cli.py
```
Now you have an executable file in your dist/ directory. Move to this directory:
```bash
cd dist
```
And rename the executable file to your liking: 
```bash
mv cli m601
```
You can ensure that everything went well by executing this file:
```bash
./m601 -h
```
It should output a help message.
Now you can copy it in your /usr/local/bin/ directory:
```bash
sudo cp m601 /usr/local/bin/
```
After that, you can deactivate the virtual environment and execute this file in any library!
```bash
m601 -h
```
# Usage
First of all, you need to read the current settings from your mouse:
```bash
m601 -r settings
# or
python cli.py -r settings 
```
This will generate "settings.ini" file. This .ini file contains very detailed info about all parameters of the mouse that you can change. Please, read it carefully, cause I can't predict how the mouse will behave if some of the parameters contain values that they should not contain. So please, read "Possible values" for each parameter before changing it. 
Please note, that to change even the smallest settings, the mouse receives a big package with all settings, so if you need to change, for example, lighting mode, the programm still needs to send DPI values, USB polling rate, and all other parameters, so don't delete anything from .ini file, just modify it in within the given limits.
After you modify .ini file to your liking, you need to write it to the mouse:
```bash
m601 -w settings.ini
# or
python cli.py -w settings.ini
```
Thats it! Your new settings should be already in the mouse.
In addition, you can also change the mouse mode:
```bash
m601 -m 1
m601 -m 2
# or
python cli.py -m 1
python cli.py -m 2
```
And damp raw data from the mouse for debugging purposes:
```bash
m601 -d dump
# or
python cli.py -d dump
```
