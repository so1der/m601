This Python script allow you to control Redragon M601 gaming mouse from your terminal!

First of all, make sure that VID and PID of your mouse match these: "258a:1007"
You can check it by executing following command in your terminal:
```bash
lsusb
```
You'll get similar output:
```bash
Bus 001 Device 008: ID 258a:1007 SINOWEALTH Wired Gaming Mouse
```
If your VID:PID didn't match 258a:1007, or you have different mouse from Redragon, you can check [mouse_m908](https://github.com/dokutan/mouse_m908) repository from [dokutan](https://github.com/dokutan). 

After you ensured that VID:PID of your mouse are correct, you can try to change mouse mode:
```bash
python cli.py -m 1
python cli.py -m 2
```
