from typing import Generator, Tuple

import pyautogui
from pyfirmata import Pin

from utils import ArduinoNano, colorize, console, get_color, port

print()
with console.status(
    f"[bold steel_blue]Establishing Connection with Board at {port}...",
    spinner="dots12",
):
    board = ArduinoNano()
    console.log("[green] Board Initialized!!!")


class Sensor:
    """abstracts the common behaviour of a tilt sensor"""

    def __init__(self, pin: int) -> None:
        self.pin: Pin = board.get_pin(f"d:{pin}:i")
        self.pin.read()
        self._state: bool = False
        self.prev_state: bool = False

    @property
    def state(self) -> bool:
        """returns the state of the pin (high or low). if pin is None return False
        side effect: sets previous state

        Returns:
            bool: True for high, False for low
        """
        if self.__dict__.get("state"):
            self.prev_state = self._state
        self._state = self.pin.read()
        return self._state

    def is_changed(self):
        return self.prev_state != self.state


class Button(Sensor):
    """abstracts common behaviour of button"""

    def __init__(self, pin: int, key: str) -> None:
        self.prev_state = False
        self.key = key
        super().__init__(pin)

    def onchange(self) -> None:
        if self.state:
            pyautogui.keyDown(self.key)

        else:
            pyautogui.keyUp(self.key)

        self.prev_state = self.state

    @property
    def state(self) -> bool:
        """buttons are pulled up. gives 0 when pressed and 1 when
        released. have to inverse the input to get correct results

        Returns:
            bool: [description]
        """
        return not super().state

    def __repr__(self) -> str:
        return colorize(
            f"Button({self.pin.pin_number}, {get_color(self.state)})", "yellow"
        )


class SteerWheel:
    """functions of steering wheel which is created by combining 2 tilt sensors"""

    def __init__(
        self, *, left_sensor_pin: int, right_sensor_pin: int, keymap: dict
    ) -> None:
        self.left_sensor = Sensor(left_sensor_pin)
        self.right_sensor = Sensor(right_sensor_pin)
        self.keymap = keymap
        self.tilt_map = {
            (True, True): "straight",
            (True, False): "right",
            (False, True): "left",
            (False, False): "straight",  # for development
            (None, None): "",
        }
        self.key_pressed: str = ""
        self.prev_state: Tuple[bool, bool] = (False, False)

    @property
    def state(self) -> Tuple[bool, bool]:
        """read sensors and return the output, update colors

        Returns:
            Tuple[bool, bool]: return output in a tuple [0]: left sensor,
            [1]: right sensor
        """
        return (self.left_sensor.state, self.right_sensor.state)

    @property
    def colors(self) -> Generator[str, None, None]:
        return (get_color(state) for state in self.state)

    @property
    def tilt_state(self) -> str:
        return self.tilt_map[self.state]

    def onchange(self) -> None:
        key: str = self.keymap.get(self.tilt_state, "")

        # if there is a key to press and that key is not the key already pressed
        if key and self.key_pressed != key:
            pyautogui.keyDown(key)
            pyautogui.keyUp(self.key_pressed)

        elif not key and self.key_pressed:
            pyautogui.keyUp(self.key_pressed)

        self.prev_state = self.state
        # set the key_pressed to the current key (for the next round)
        self.key_pressed = key

    def is_changed(self):
        return self.prev_state != self.state

    def __repr__(self) -> str:
        status = "{}, left={}, right={}".format(
            colorize(self.tilt_state, "cyan"), *self.colors
        )
        return colorize(f"SteerWheel({status})", "purple")
