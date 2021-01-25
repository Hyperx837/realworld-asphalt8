from pyfirmata import util
from pynput.keyboard import Controller, Key

from utils import ArduinoNano, delay

keyboard = Controller()
board = ArduinoNano('/dev/ttyUSB0')

# start iterator to read pins without blocking main thread
it = util.Iterator()
it.start()

# pin setup
nitro_btn = board.get_pin('d:2:i')
accel_btn = board.get_pin('d:3:i')
brake_btn = board.get_pin('d:4:i')


def loop():
    if nitro_btn.read():
        print('hi')


if __name__ == '__main__':
    while True:
        try:
            loop()
        except KeyboardInterrupt:
            print("Exiting...")
            exit()
