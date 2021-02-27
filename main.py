import asyncio
from typing import Awaitable, List, Set, Union

from sensor import Button, SteerWheel
from utils import console, exit_program, forever

button_data = {10: "s", 11: " ", 12: "w"}
# button_data = {11: " ", 12: "w"}
buttons: Set[Button] = {Button(pin, key) for pin, key in button_data.items()}

# keys to press when steer wheel is straight or turned right or left
keymap = {"straight": "", "right": "d", "left": "a"}
steer = SteerWheel(keymap)

# all sensors
SENSOR_TYPE = Union[SteerWheel, Button]
sensors: Set[SENSOR_TYPE] = {*buttons, steer}

clear_line = "\033[A\033[A"


@forever(delay=1)
async def log_status():
    """logs the status of given sensor with a 1 min delay"""
    print(clear_line)
    console.log(f"{sensors}")


@forever(delay=0.01)
async def button_observer() -> None:
    """run this code until arduino turns off"""
    changed_buttons: List[Awaitable] = [
        button.onchange() for button in buttons if button.is_changed()
    ]
    await asyncio.gather(*changed_buttons)


@forever(delay=0.05)
async def steerwheel_observer():
    if steer.is_changed():
        await steer.onchange()


async def main():
    tasks = [log_status(), steerwheel_observer(), button_observer(), steer.press_key()]
    try:
        await asyncio.gather(*tasks)

    except KeyboardInterrupt:
        print(clear_line, "\n")

    exit_program()


if __name__ == "__main__":
    asyncio.run(main())
