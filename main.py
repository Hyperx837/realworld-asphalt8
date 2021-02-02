import time
from typing import List, Union

from sensor import Button, SteerWheel, TiltSensor
from utils import console

nitro_btn = Button(2, " ")
accel_btn = Button(3, "w")
brake_btn = Button(4, "s")
buttons: List[Button] = [nitro_btn, accel_btn, brake_btn]

# tilt sensors
left_tilt = TiltSensor(5)
right_tilt = TiltSensor(6)

# steer wheel
keymap = {"right": "d", "left": "a"}
steer = SteerWheel(left_tilt, right_tilt, keymap)

# all sensors
sensors: List[Union[TiltSensor, Button]] = []

clear_line = "\033[A\033[A"


def main() -> None:
    """run this code until arduino turns off"""
    for button in buttons:
        button.press_on_click()

    # steer.check_tilt()
    # print(clear_line)
    print(*buttons, steer)
    time.sleep(0.01)


if __name__ == "__main__":
    while True:
        try:
            main()
            print(clear_line)
        except KeyboardInterrupt:
            print(clear_line, "\n")
            break

    console.log("[bold cyan]Exiting...")
