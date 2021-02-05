from typing import Generator, Tuple

import pyautogui
from pyfirmata import Pin

from utils import ArduinoNano, colorize, console, get_color

print()
with console.status(
    "[bold steel_blue]Establishing Connection with Board...", spinner="dots12"
):
    board = ArduinoNano()
    console.log("[green] Board Initialized!!!")


class Sensor:
    """abstracts the common behaviour of a tilt sensor"""

    def __init__(self, pin: int) -> None:
        self.pin: Pin = board.get_pin(f"d:{pin}:i")
        self.pin.read()
        # self.read()

    @property
    def state(self) -> bool:
        """returns the state of the pin (high or low).

        Returns:
            bool: True for high, False for low
        """
        return self.pin.read()


class Button(Sensor):
    """abstracts common behaviour of button"""

    def __init__(self, pin: int, key: str) -> None:
        self.prev_state = False
        self.key = key
        super().__init__(pin)

    @property
    def state(self) -> bool:
        """returns the value of the button pin

        Returns:
            bool: True for high False for low
        """
        return self.pin.read()

    def press_on_click(self) -> None:
        if self.state and not self.prev_state:
            pyautogui.keyDown(self.key)

        elif self.prev_state and not self.state:
            pyautogui.keyUp(self.key)

        self.prev_state = self.state

    def __repr__(self) -> str:
        return colorize(f"Button({get_color(self.state)})", "yellow")


class SteerWheel:
    """functions of steering wheel which is created by combining 2 tilt sensors"""

    def __init__(self, *, left_pin: int, right_pin: int, keymap: dict) -> None:
        self.left_sensor = Sensor(left_pin)
        self.right_sensor = Sensor(right_pin)
        self.keymap = keymap
        self.tilt_map = {
            (True, True): "straight",
            (True, False): "right",
            (False, True): "left",
            (False, False): "straight",  # for development
            (None, None): "",
        }
        self.key_pressed: str = ""

    @property
    def tilt(self) -> Tuple[bool, bool]:
        """read sensors and return the output, update colors

        Returns:
            Tuple[bool, bool]: return output in a tuple [0]: left sensor, [1]: right sensor
        """
        return (self.left_sensor.state, self.right_sensor.state)

    @property
    def colors(self) -> Generator[str, None, None]:
        return (get_color(val) for val in self.tilt)

    @property
    def tilt_state(self) -> str:
        return self.tilt_map[self.tilt]

    def check_tilt(self) -> None:
        key: str = self.keymap.get(self.tilt_state, "")

        # if there is a key2press and that key is not pressed
        if key and self.key_pressed != key:
            pyautogui.keyDown(key)

        elif not key and self.key_pressed:
            pyautogui.keyUp(self.key_pressed)

        # set the key_pressed to the current key (for the next round)
        self.key_pressed = key

    def __repr__(self) -> str:
        status = "{}, left={}, right={}".format(
            colorize(self.tilt_state, "cyan"), *self.colors
        )
        return colorize(f"SteerWheel({status})", "purple")
