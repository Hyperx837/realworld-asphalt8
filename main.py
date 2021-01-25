from pyfirmata import Pin, util
from pynput.keyboard import Controller, Key

from utils import ArduinoNano

keyboard = Controller()
board = ArduinoNano("/dev/ttyUSB0")

# start iterator to read pins without blocking main thread
it = util.Iterator()
it.start()

# pin setup
nitro_btn = board.get_pin("d:2:i")
accel_btn = board.get_pin("d:3:i")
brake_btn = board.get_pin("d:4:i")


def press_if_true(button: Pin, key: Key):
    """press key if button is pressed

    Args:
        button (Pin): button to read input from
        key (Key): key to press when button is pressed
    """
    if button.read():
        keyboard.press(key)

    else:
        keyboard.release(key)


def loop():
    """run this code until arduino turns off"""
    press_if_true(nitro_btn, Key.space)
    press_if_true(accel_btn, "w")
    press_if_true(brake_btn, "s")


if __name__ == "__main__":
    while True:
        try:
            loop()
        except KeyboardInterrupt:
            print("Exiting...")
            exit()
