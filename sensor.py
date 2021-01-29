import glob
from typing import Tuple

import pyautogui
from pyfirmata import Pin, util

from utils import ArduinoNano

(port,) = glob.glob("/dev/ttyUSB*")
board = ArduinoNano(port)

it = util.Iterator(board)
it.start()


class Button:
    def __init__(self, pin: str, key: str) -> None:
        self.pin: Pin = board.get_pin(pin)
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
        return f"Button({self.state})"


class TiltSensor:
    def __init__(self, pin: str) -> None:
        self.pin: Pin = board.get_pin(pin)
        self.state = False
        self.read()

    def read(self) -> bool:
        """returns the state of the pin (high or low).

        Returns:
            bool: True for high, False for low
        """
        return self.pin.read()


class SteerWheel:
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

    @property
    def tilt(self) -> Tuple[bool, bool]:
        return self.left_sensor.read(), self.right_sensor.read()

    @property
    def tilt_state(self) -> str:
        if self.tilt == (None, None):
            return
        return self.tilt_map[self.tilt]

    @property
    def key(self) -> str:
        """returns the key to press when the state is high

        Returns:
            str: the key can be a attr of Key class or a string
        """
        if self.tilt_state not in self.keymap:
            self.keymap[self.tilt_state] = None
        return self.keymap[self.tilt_state]

    def check_tilt(self):
        key, tilt_state, tilt = self.key, self.tilt_state, self.tilt
        print(key)
        # if there is a key to press and that key is not pressed
        if key and self.key_pressed != key:
            pyautogui.keyDown(key)

        elif not key and self.key_pressed:
            pyautogui.keyUp(self.key_pressed)

        # elif key is None and self.key_pressed:
        # pass
        self.key_pressed = key
        # if key is None:
        #     pass

        # else:
        #     pass

    def __repr__(self):
        return (
            f"SteerWheel({self.tilt_state}, left={self.tilt[0]}, right={self.tilt[1]})"
        )
