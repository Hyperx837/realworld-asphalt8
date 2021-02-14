import asyncio
from typing import List, Union

from sensor import Button, SteerWheel
from utils import console, forever

button_data = {2: " ", 3: "w", 4: "s"}
buttons: List[Button] = [Button(pin, key) for pin, key in button_data.items()]

# steer wheel
keymap = {"straight": "", "right": "d", "left": "a"}
steer = SteerWheel(left_pin=5, right_pin=6, keymap=keymap)

# all sensors
SENSOR_TYPE = Union[SteerWheel, Button]
sensors: List[SENSOR_TYPE] = [*buttons, steer]
prev_state = {sensor: sensor.state for sensor in sensors}

clear_line = "\033[A\033[A"


@forever(delay=1)
async def log_status():
    """logs the status of given sensor with a 1 min delay"""
    print(clear_line)
    console.log(f"{sensors}")


@forever(delay=0.01)
async def detect_change() -> None:
    """run this code until arduino turns off"""
    for sensor in sensors:
        if sensor.prev_state != sensor.state:
            sensor.onchange()


async def main():
    await asyncio.gather(detect_change(), log_status())


if __name__ == "__main__":
    print()
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print(clear_line, "\n")

    console.log("[bold cyan]Exiting...")
