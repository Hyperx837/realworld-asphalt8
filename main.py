import time

from pyfirmata import Pin, util
from pynput.keyboard import Controller, Key

from utils import ArduinoNano

keyboard = Controller()
board = ArduinoNano("/dev/ttyUSB1")

# start iterator to read pins without blocking main thread
it = util.Iterator(board)
it.start()

# pin setup
nitro_btn = board.get_pin("d:2:i")
accel_btn = board.get_pin("d:3:i")
brake_btn = board.get_pin("d:4:i")

is_pressed = {
    nitro_btn: False,
    accel_btn: False,
    brake_btn: False,
}


def press_if_true(button: Pin, key: Key):
    """press key if button is pressed

    Args:
        button (Pin): button to read input from
        key (Key): key to press when button is pressed
    """
    # print(button.read())
    if button.read() and not is_pressed[button]:
        # print("nitro")
        keyboard.press(key)
        is_pressed[button] = True

    else:
        # print("no nitro")
        keyboard.release(key)
        is_pressed[button] = False


def loop():
    """run this code until arduino turns off"""
    # print(nitro_btn.read())
    press_if_true(nitro_btn, Key.space)
    press_if_true(accel_btn, "w")
    press_if_true(brake_btn, "s")
    time.sleep(0.01)


if __name__ == "__main__":
    while True:
        try:
            loop()
        except KeyboardInterrupt:
            print("Exiting...")
            exit()
