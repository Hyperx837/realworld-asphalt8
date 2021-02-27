import asyncio
from typing import Union

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

pyautogui.FAILSAFE = False


class Sensor:
    def __init__(self) -> None:
        self.pin: Pin
        self._state: Union[bool, float] = False
        self.prev_state: Union[bool, float] = False

    @property
    def state(self) -> Union[bool, float]:
        """returns the state of the pin (high or low). if pin is None return False
        side effect: sets previous state

        Returns:
            bool: True for high, False for low
        """
        self.prev_state = self._state
        self._state = self.pin.read()
        return self._state

    def is_changed(self):
        return self.prev_state != self.state


class Button(Sensor):
    """abstracts common behaviour of button"""

    def __init__(self, pin: int, key: str) -> None:
        self.pin: Pin = board.get_pin(f"d:{pin}:i")
        self._state: bool = False
        self.prev_state: bool = False
        self.key = key
        super().__init__()

    @property
    def state(self) -> bool:
        """
        buttons are pulled up. have to inverse the input to
        get correct results

        Returns:
            bool: True for low, False for high
        """
        return not super().state

    def onchange(self) -> None:
        if self.state:
            pyautogui.keyDown(self.key)

        else:
            pyautogui.keyUp(self.key)

        # self.prev_state = self.state

    def __repr__(self) -> str:
        return colorize(
            f"Button({self.pin.pin_number}, {get_color(self.state)})", "yellow"
        )


class SteerWheel(Sensor):
    def __init__(self, keymap: dict) -> None:
        super().__init__()
        self.pin: Pin = board.get_pin("a:7:i")
        self.keymap = keymap
        self.prev_state: float = 0
        self.initial: float = 0
        self.initialize_input()
        self.range = 0.06
        self.mid_start = self.initial - self.range
        self.mid_end = self.initial + self.range
        console.log(
            f"[bold cyan] Steering Wheel middle ranging from {self.mid_start} to \
            {self.mid_end}"
        )
        self.key_pressed: str = ""

    def initialize_input(self) -> None:
        """initialize"""
        while not self.initial:
            self.initial = self.state

    @property
    def state(self) -> float:
        """round off sensor value to 2 decimal points

        Returns:
            float: sensor value with 2 decimal points
        """
        sensor_val = super().state
        if sensor_val is None:
            return sensor_val
        self._state = sensor_val
        return round(sensor_val, 2)

    @property
    def tilt(self) -> str:
        if self.state > self.mid_end:
            return "right"

        elif self.state < self.mid_start:
            return "left"

        return "straight"

    async def onchange(self) -> None:
        key: str = self.keymap.get(self.tilt, "")
        pyautogui.keyDown(key)
        await asyncio.sleep(0.005)
        pyautogui.keyUp(key)
        # # if there is a key to press and that key is not the key already pressed
        # if key and self.key_pressed != key:
        #     pyautogui.keyDown(key)
        #     pyautogui.keyUp(self.key_pressed)

        # elif not key and self.key_pressed:
        #     pyautogui.keyUp(self.key_pressed)

        # self.prev_state = self.state
        # # # set the key_pressed to the current key (for the next round)
        # self.key_pressed = key

    def __repr__(self):
        return colorize(
            f"SteerWheel({colorize(self.tilt, 'yellow')}, \
                {colorize(self.state, 'cyan')})",
            "purple",
        )
