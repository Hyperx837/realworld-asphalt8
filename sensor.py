import asyncio
from typing import Union

import pyautogui
from pyfirmata import Pin

from utils import ArduinoNano, colorize, console, exit_program, get_color, port

print()
with console.status(
    f"[bold steel_blue]Establishing Connection with Board at {port}...",
    spinner="dots12",
):
    board = ArduinoNano()
    console.log("[green] Board Initialized!!!")


class Sensor:
    def __init__(self) -> None:
        self.pin: Pin
        self._state: Union[bool, int] = False
        self.prev_state: Union[bool, int] = False

    @property
    def state(self) -> Union[bool, int]:
        """returns the state of the pin (high or low). if pin is None return False
        side effect: sets previous state

        Returns:
            bool: True for high, False for low
        """
        self._state = self.pin.read()
        self.prev_state = self.__dict__.get("state", False)
        return self._state

    def is_changed(self):
        return self.prev_state != self.state


class Button(Sensor):
    """abstracts common behaviour of button"""

    def __init__(self, pin: int, key: str) -> None:
        super().__init__()
        self.pin: Pin = board.get_pin(f"d:{pin}:i")
        self._state: bool = False
        self.prev_state: bool = False
        self.key = key

    @property
    def state(self) -> bool:
        """
        buttons are pulled up. have to inverse the input to
        get correct results

        Returns:
            bool: True for low, False for high
        """
        return not super().state

    async def onchange(self) -> None:
        if self.state:
            pyautogui.keyDown(self.key)

        else:
            pyautogui.keyUp(self.key)

        self.prev_state = self.state
        await asyncio.sleep(0.1)

    def __repr__(self) -> str:
        return colorize(
            f"Button({self.pin.pin_number}, {get_color(self.state)})", "yellow"
        )


class SteerWheel(Sensor):
    def __init__(self, keymap: dict) -> None:
        super().__init__()
        self.pin: Pin = board.get_pin("a:7:i")
        self.keymap = keymap
        self.prev_state: int = 0
        self.initial: int = 0
        self.initialize_input()
        self.range = 0.08
        self.mid_start = self.initial - self.range
        self.mid_end = self.initial + self.range
        console.log(
            f"[bold cyan] Steering Wheel middle ranging from {self.mid_start} to \
            {self.mid_end}"
        )
        self.key_pressed: str = ""

    def initialize_input(self) -> None:
        """initialize"""
        count = 0
        while not self.initial:
            self.initial = self.state
            # if count == 15:
            #     console.log("[bold orange] Board Not Connected Properly")
            #     exit_program()
            count += 1

    @property
    def tilt_state(self) -> str:
        if self.state > self.mid_end:
            return "right"

        elif self.state < self.mid_start:
            return "left"

        return "straight"

    async def onchange(self) -> None:
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
        await asyncio.sleep(0.5)

    def __repr__(self):
        return colorize(
            f"SteerWheel({colorize(self.tilt_state, 'yellow')}, \
                {colorize(self.state, 'cyan')})",
            "purple",
        )


# class RotaryEncoder:
#     def __init__(self) -> None:
#         self.clk_pin: Pin = board.get_pin("d:2:i")
#         self.dt_pin: Pin = board.get_pin("d:2:i")
#         self.prev_state: Tuple[bool, bool] = (False, False)
#         self.count = 0

#     @property
#     def state(self) -> Tuple[bool, bool]:
#         return self.clk_pin.read(), self.dt_pin.read()

#     def is_changed(self):
#         return self.prev_state != self.state

#     def counter(self):
#         clk_state, dt_state = self.state
#         if clk_state != dt_state:
#             self.count += 1

#         else:
#             self.count -= 1

#     def onchange(self):
#         pass
