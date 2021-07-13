# Python Philips BDM4065UC Serial Remote

This project is an attempt to setup a small Python Flask-based web service on a Raspberry Pi to control a [Philips BDM4065UC](https://www.philips.com.au/c-p/BDM4065UC_75/brilliance-led-backlit-lcd-display) over RS-232C.  If you own a Philips BDM4065UC monitor, you have probably said to yourself, "why does this amazing piece of equipment not have a remote control"?  After all, the monitor's size and clarity of picture begs you to mount it to your wall so you can marvel at its awesomeness from the appropriate distance.  However, as soon as you need to adjust the volume of the integrated speakers or reconfigure the handy PIP features, you will have to blindly grope around the bottom right corner of the device and try to remember which direction to push the menu control button.  To their credit, Philips does make [SmartControl Software](https://www.philips.com.au/c-p/BDM4065UC_75/brilliance-led-backlit-lcd-display/support) that lets you remotely control the monitor over RS-232C using Windows...using Windows...what if I don't use Windows?  Are there any other options?  This repository represents my little journey down that rabbit hole, may it fill that shortcoming and enhance your experience using this otherwise perfect piece of display technology.

## Overview

This project includes a cli and a webservice version.  The cli version, `remote.py` under the `cli` folder, is a simple Python script that is a recreation of the [Philips BDM4065UC tv/monitor RS232 control](https://gist.github.com/daanzu/352fd5560cc57aa08c3a67ec17c4b448) code.  The web service version, `service.py` under the `webservice` folder, adapts the `remote.py` to make use of [Flask](https://flask.palletsprojects.com/en/2.0.x/).  The ultimate goal is to run the web service version on a Raspberry PI connected to the Philips BDM4065UC so the monitors controls can be accessed remotely.

## Hardware

The [Philips BDM4065UC](https://www.philips.com.au/c-p/BDM4065UC_75/brilliance-led-backlit-lcd-display) includes a RS-232 port in the form of a 3.5mm female audio jack.  This will require a couple of different types of cables to get connected to your desktop (or Raspberry Pi).  Using the notes in the [Philips BDM4065UC tv/monitor RS232 control](https://gist.github.com/daanzu/352fd5560cc57aa08c3a67ec17c4b448) gist as a guide, I ended up purchasing the following:

* [Sabrent USB 2.0 to Serial (9-Pin) DB-9 RS-232 Adapter Cable 6ft Cable](https://www.amazon.com/gp/product/B006AA04K0/ref=oh_aui_detailpage_o09_s00?ie=UTF8&psc=1)
* [SF Cable, DB9 Female to 3.5mm Serial Cable (6 Feet)](https://www.amazon.com/gp/product/B004T9BBJC/ref=oh_aui_detailpage_o09_s00?ie=UTF8&psc=1)
* [Your Cable Store Serial Port 9 Pin Null Modem Adapter](https://www.amazon.com/gp/product/B005QE4YLQ/ref=oh_aui_detailpage_o07_s00?ie=UTF8&psc=1)
* [Electop 2.5mm Male to 3.5mm(1/8 inch) Female Stereo Audio Jack Adapter](https://www.amazon.com/Electop-Female-Stereo-Adapter-Headphone/dp/B01GC6LR84/ref=sr_1_5?dchild=1&keywords=2.5mm+Male+to+3.5mm+Female&qid=1626194366&sr=8-5)

For those that want to go the Raspberry Pi route, I ordered a [Raspberry Pi Zero W](https://www.amazon.com/CanaKit-Raspberry-Wireless-Complete-Starter/dp/B072N3X39J/ref=sr_1_4?dchild=1&keywords=raspberry+pi+zero&qid=1626194442&sr=8-4).

## Running the CLI version

Python 3.8 was used during the development of this script, packages used can be found in the included `requirements.txt`.  Prior to running the script you must make sure that the user has permissions to access the serial port.  Since I am on Linux, this looked like:
```
chmod +777 /dev/ttyUSB0
```
Granted, it is a terrible practice to add all permissions to all users/groups here, I am being lazy.  Once you do have the permission sorted, simply use the command:
```
python remote.py --port <path to serial port> <command> <command option>
```

Here's a handy table of supported commands and options:
| Command | Options |
| --- | --- |
| power | off, on |
| input | dp, hdmi, hdmi2, vga |
| volume | _any int 0 to 100_ |

## Running the Web Service version

Python 3.8 was used during the development of this script, packages used can be found in the included `requirements.txt`.  Similar to the CLI version, the appropriate user permissions must be applied to the serial port, additionally you will need to export the variable `SERIAL_PORT=<path to serial port>` into the environment the web service is running in.  Once the user permissions and the exporting of the variable is sorted, you can start the web service:

```
gunicorn --bind=127.0.0.1:8080 service:app
```

Commands and options can then be submitted via curl:
```
curl -X POST "http://localhost:8080?cmd=<command>&option=<option>
```

## References
* [Philips BDM4065UC tv/monitor RS232 control](https://gist.github.com/daanzu/352fd5560cc57aa08c3a67ec17c4b448)
* [RS232-Monitor-Database](https://github.com/YooUp/RS232-Monitor-Database)
* [Philips Brilliance BDM4065UC User Manual](https://www.manualslib.com/manual/866028/Philips-Brillance-Bdm4065uc.html)
* [Philips BDM4065UC Command Protocols](https://www.avforums.com/attachments/philips-bdm4065uc-command-protocols-xls.625499/)

## Contributing

PRs are always welcome, a lot of this code is a cut and past job, with some minor tweaks here and there.  I am sure there are better ways to do some of this things here and suggestions are always welcome.  Feel free to submit an issue it you have a problem or a feature request, no guarantees how quickly I will get back to you or that I every will.
