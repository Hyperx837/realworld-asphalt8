import asyncio
from typing import Set, Union

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
def log_status():
    """logs the status of given sensor with a 1 min delay"""
    print(clear_line)
    console.log(f"{sensors}")


@forever(delay=0.01)
def button_observer() -> None:
    """run this code until arduino turns off"""
    for button in buttons:
        if button.is_changed():
            button.onchange()


async def steerwheel_observer():
    while True:
        if steer.is_changed():
            await steer.onchange()
        await asyncio.sleep(0.01)


async def main():
    tasks = [log_status(), button_observer(), steerwheel_observer()]
    try:
        await asyncio.gather(*tasks)

    except KeyboardInterrupt:
        print(clear_line, "\n")

    exit_program()


if __name__ == "__main__":
    asyncio.run(main())
