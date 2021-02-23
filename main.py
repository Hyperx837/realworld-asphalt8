import asyncio
from typing import Awaitable, Generator, List, Set, Union

from sensor import Button, SteerWheel
from utils import console, exit_program

button_data = {10: "s", 11: " ", 12: "w"}
buttons: Set[Button] = {Button(pin, key) for pin, key in button_data.items()}

# keys to press when steer wheel is straight or turned right or left
keymap = {"straight": "", "right": "d", "left": "a"}
steer = SteerWheel(keymap)

# all sensors
SENSOR_TYPE = Union[SteerWheel, Button]
sensors: Set[SENSOR_TYPE] = {*buttons, steer}

clear_line = "\033[A\033[A"


async def log_status():
    """logs the status of given sensor with a 1 min delay"""
    while True:
        print(clear_line)
        console.log(f"{sensors}")
        asyncio.sleep(1)


async def main() -> None:
    """run this code until arduino turns off"""
    asyncio.create_task(log_status())
    while True:
        changed_sensors: List[Awaitable] = [
            sensor.onchange() for sensor in sensors if sensor.is_changed()
        ]
        asyncio.gather(*changed_sensors)

        await asyncio.sleep(0.01)


if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print(clear_line, "\n")

    exit_program()
