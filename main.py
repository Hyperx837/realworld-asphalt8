import time
from threading import Thread
from typing import List, Union

from sensor import Button, SteerWheel
from utils import console


def log_status(sensors: list):
    """logs the status of given sensor with a 1 min delay

    Args:
        sensors (tuple): tuple of sensors
    """
    print()
    while run_program:
        print(clear_line)
        console.log(f"{sensors}")
        time.sleep(1)


def main() -> None:
    """run this code until arduino turns off"""
    global run_program
    status_thread.start()
    try:
        while True:
            for button in buttons:
                button.press_on_click()

            time.sleep(0.01)

    except KeyboardInterrupt:
        print(clear_line, "\n")
        run_program = False

    console.log("[bold cyan]Exiting...")


button_data = {2: " ", 3: "w", 4: "s"}
buttons: List[Button] = [Button(pin, key) for pin, key in button_data.items()]

# steer wheel
keymap = {"straight": "", "right": "d", "left": "a"}
steer = SteerWheel(left_pin=5, right_pin=6, keymap=keymap)

# all sensors
sensors: List[Union[SteerWheel, Button]] = [*buttons, steer]

clear_line = "\033[A\033[A"
run_program = True
status_thread = Thread(target=log_status, args=(sensors,))

if __name__ == "__main__":
    main()
