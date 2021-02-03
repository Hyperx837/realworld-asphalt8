from typing import Tuple

import pyautogui
from pyfirmata import Pin

from utils import ArduinoNano, colorize, console

print()
with console.status(
    "[bold steel_blue]Establishing Connection with Board...", spinner="dots12"
):
    board = ArduinoNano()
    console.log("[green] Board Initialized!!!")


def get_color(text: bool):
    color = "green" if text else "red"
    return colorize(str(text), color)


class Button:
    """abstracts common behaviour of button"""

    def __init__(self, pin: int, key: str) -> None:
        self.pin: Pin = board.get_pin(f"d:{pin}:i")
        self.prev_state = False
        self.key = key
        self.pin.read()

    @property
    def state(self) -> bool:
        return self.pin.read()

    def press_on_click(self):
        if self.state and not self.prev_state:
            pyautogui.keyDown(self.key)

        elif self.prev_state and not self.state:
            pyautogui.keyUp(self.key)

        self.prev_state = self.state

    def __repr__(self) -> str:
        color = "green" if self.state else "red"
        return colorize(f"Button({colorize(self.state, color)})", "yellow")


class TiltSensor:
    """abstracts the common behaviour of a tilt sensor"""

    def __init__(self, pin: int) -> None:
        self.pin: Pin = board.get_pin(f"d:{pin}:i")
        self.state = False
        self.read()

    def read(self) -> bool:
        """returns the state of the pin (high or low).

        Returns:
            bool: True for high, False for low
        """
        return self.pin.read()


class SteerWheel:
    """functions of steering wheel which is created by combining 2 tilt sensors"""

    def __init__(self, left_sensor: TiltSensor, right_sensor: TiltSensor, keymap: dict):
        self.left_sensor = left_sensor
        self.right_sensor = right_sensor
        self.keymap = keymap
        self.tilt_map = {
            (True, True): "straight",
            (True, False): "right",
            (False, True): "left",
            (False, False): "straight",  # for development
        }
        self.key_pressed: str = None
        self.colors = None

    @property
    def tilt(self) -> Tuple[bool, bool]:
        """read sensors and return the output, update colors

        Returns:
            Tuple[bool, bool]: return output in a tuple [0]: left sensor, [1]: right sensor
        """
        sensor_vals = self.left_sensor.read(), self.right_sensor.read()
        self.colors = (str(get_color(val)) for val in sensor_vals)
        return sensor_vals

    @property
    def tilt_state(self) -> str:
        if self.tilt == (None, None):
            return
        return self.tilt_map[self.tilt]

    def key2press(self) -> str:
        """returns the key to press when the according to the state

        Returns:
            str: the key can be a attr of Key class or a string
        """
        if self.tilt_state not in self.keymap:
            self.keymap[self.tilt_state] = None
        return self.keymap[self.tilt_state]

    def check_tilt(self):
        key = self.key2press()
        # print(key)
        # if there is a key2press and that key is not pressed
        if key and self.key_pressed != key:
            pyautogui.keyDown(key)

        elif not key and self.key_pressed:
            pyautogui.keyUp(self.key_pressed)

        # set the key_pressed to the current key (for the next round)
        self.key_pressed = key

    def __repr__(self):
        status = "{}, left={}, right={}".format(
            colorize(self.tilt_state, "cyan"), *self.colors
        )
        return colorize(f"SteerWheel({status})", "purple")
