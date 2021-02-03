import time
from threading import Thread
from typing import List

from sensor import Button, SteerWheel, TiltSensor
from utils import console


def log_status(sensors: tuple):
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
sensors = (*buttons, steer)

clear_line = "\033[A\033[A"
run_program = True
status_thread = Thread(target=log_status, args=(sensors,))

if __name__ == "__main__":
    main()
