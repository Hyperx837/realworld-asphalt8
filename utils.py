import glob
import os
import sys

import pyfirmata
from rich.console import Console
from serial import tools

console = Console()


class NoValidPortError(Exception):
    pass


class BoardNotPluggedError(Exception):
    pass


class ArduinoNano(pyfirmata.Board):
    def __init__(self, *args, **kwargs):
        layout = {
            "digital": (1, 0, *range(2, 14)),
            "analog": tuple(range(7)),
            "pwm": (3, 5, 6, 9, 10, 11),
            "use_ports": True,
            "disabled": (0, 1),
        }
        if sys.platform == "linux":
            try:
                (port,) = glob.glob("/dev/ttyUSB*")

            except ValueError:
                raise BoardNotPluggedError

        elif sys.platform == "win32":
            comports = tools.list_ports.comports()
            (port, *_) = (port[0] for port in comports if "arduino" in port[1])

        else:
            # please set an environment variable for port (recommended) or set port manually
            port = os.environ.get("PORT")

        if port is None:
            raise NoValidPortError(
                "Hasn't Provided a valid port or arduino not plugged"
            )

        super().__init__(layout=layout, port=port, *args, **kwargs)
