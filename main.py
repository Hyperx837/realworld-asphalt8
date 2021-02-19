import time
from typing import Set, Union

from sensor import Button, SteerWheel
from utils import console

# button_data = {2: " ", 3: "w", 4: "s"}
button_data = {2: " ", 3: "w"}
buttons: Set[Button] = {Button(pin, key) for pin, key in button_data.items()}

# keys to press when steer wheel is straight or turned right or left
keymap = {"straight": "", "right": "d", "left": "a"}
steer = SteerWheel(left_sensor_pin=5, right_sensor_pin=6, keymap=keymap)

# all sensors
SENSOR_TYPE = Union[SteerWheel, Button]
sensors: Set[SENSOR_TYPE] = {*buttons, steer}

clear_line = "\033[A\033[A"


def main() -> None:
    """run this code until arduino turns off"""
    while True:
        for sensor in sensors:
            if sensor.prev_state != sensor.state:
                sensor.onchange()
                print(clear_line)
                console.log(f"{sensors}")
        time.sleep(0.01)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print(clear_line, "\n")

    console.log("[bold cyan]Exiting...")
