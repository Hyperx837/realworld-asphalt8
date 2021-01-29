import time
from typing import List, Union

from sensor import Button, SteerWheel, TiltSensor

nitro_btn = Button("d:2:i", " ")
accel_btn = Button("d:3:i", "w")
brake_btn = Button("d:4:i", "s")
buttons: List[Button] = [nitro_btn, accel_btn, brake_btn]

# tilt sensors
left_tilt = TiltSensor("d:5:i")
right_tilt = TiltSensor("d:6:i")

# steer wheel
keymap = {"right": "d", "left": "a"}
steer = SteerWheel(left_tilt, right_tilt, keymap)

# all sensors
sensors: List[Union[TiltSensor, Button]] = []


def main() -> None:
    """run this code until arduino turns off"""
    # print(nitro_btn.read())
    for button in buttons:
        button.press_on_click()

    steer.check_tilt()
    # print(*buttons, steer)
    time.sleep(0.01)


if __name__ == "__main__":
    print("main program starting...")
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Exiting...")
            exit()
