import logging
import os
import sys
from functools import reduce

import serial
from flask import Flask, jsonify, request
from serial.serialutil import SerialException

# Logging
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO')
logging.basicConfig(stream=sys.stdout,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=LOGLEVEL,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()

# Configuration
SERIAL_PORT = os.environ.get('SERIAL_PORT', None)


# Create Flask App
app = Flask(__name__)


class PhilipsBDM4065UC():
    """
    This provides a map of commands to codes based on information from [RS232-Monitor-Database](https://github.com/YooUp/RS232-Monitor-Database).
    Most of this code was copied from the Gist [Philips BDM4065UC tv/monitor RS232 control](https://gist.github.com/daanzu/352fd5560cc57aa08c3a67ec17c4b448).

    Attributes:
        port    The port underwhich your serial connection is available (example: /dev/ttyUSB0).
    """

    command_map = {
        "power get": [0x19],
        "power off": [0x18, 0x01],
        "power on": [0x18, 0x02],
        "input get": [0xad],
        "input dp": [0xac, 0x09, 0x04, 0x01, 0x00],
        "input hdmi": [0xac, 0x06, 0x02, 0x01, 0x00],
        "input hdmi2": [0xac, 0x06, 0x03, 0x01, 0x00],
        "input vga": [0xac, 0x05, 0x00, 0x01, 0x00],
    }

    def __init__(self, port):
        self.tv_serial = serial.Serial(port=port,
                                       baudrate=9600,
                                       parity=serial.PARITY_NONE,
                                       stopbits=serial.STOPBITS_ONE,
                                       bytesize=serial.EIGHTBITS)

    def send_command(self, command):

        if command.split(' ')[0] == 'volume':
            buf = bytearray([0x44, int(command.split(' ')[1])])
        else:
            buf = bytearray(self.command_map[command])

        buf.insert(0, 0xa6)  # header
        buf.insert(1, 0x01)  # id
        buf.insert(2, 0x00)  # category
        buf.insert(3, 0x00)  # page
        buf.insert(4, 0x00)  # function
        buf.insert(5, len(buf)-3)  # length
        buf.insert(6, 0x01)  # control
        buf.append(reduce(lambda a, b: a ^ b, buf))  # checksum

        self.tv_serial.write(buf)


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        command = request.args.get('cmd')
        option = request.args.get('option')

        try:
            tv = PhilipsBDM4065UC(port=SERIAL_PORT)
            tv.send_command(f"{command} {option}")
        except SerialException as e:
            logger.error(e)

        message = {
            "msg": f"Command: {command} - Option: {option}",
            "status": "200"
        }
    else:
        message = {
            "msg": "I am very awake!",
            "status": "200"
        }

    return jsonify(message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")
