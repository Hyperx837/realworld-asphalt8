import asyncio
import glob
import os
import sys
import functools
from typing import Callable, Union

import pyfirmata
import serial
from rich.console import Console
from serial import tools

console = Console(highlight=False)


class NoValidPortError(Exception):
    pass


class BoardNotPluggedError(Exception):
    pass


def colorize(text: str, color: str) -> str:
    return f"[{color}]{text}[/{color}]"


def forever(*, delay: Union[int, float]):
    def wrapper(coro: Callable):
        @functools.wraps(coro)
        async def wrapped(*args, **kwargs):
            while True:
                await coro(*args, **kwargs)
                await asyncio.sleep(delay)

        return wrapped

    return wrapper


def get_color(text: bool):
    color = "green" if text else "red"
    return colorize(str(text), color)


class ArduinoNano(pyfirmata.Board):
    def __init__(self, port=None, *args, **kwargs):
        layout = {
            "digital": (1, 0, *range(2, 14)),
            "analog": tuple(range(7)),
            "pwm": (3, 5, 6, 9, 10, 11),
            "use_ports": True,
            "disabled": (0, 1),
        }
        if port is None:
            if sys.platform == "linux":
                try:
                    (port,) = glob.glob("/dev/ttyUSB*")

                except ValueError:
                    raise BoardNotPluggedError

            elif sys.platform == "win32":
                comports = tools.list_ports.comports()
                (port, *_) = (
                    port[0] for port in comports if "arduino" in port[1]
                )

            else:
                # please set an environment variable for port (recommended) or set port manually
                port = os.environ.get("PORT")
        try:
            super().__init__(layout=layout, port=port, *args, **kwargs)

        except serial.SerialException:
            console.log("[red] No valid port found!!")
            console.log("[bold cyan]Exiting...")

        it = pyfirmata.util.Iterator(self)
        it.start()
