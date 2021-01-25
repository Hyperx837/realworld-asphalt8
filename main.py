from pynput.keyboard import Controller, Key

from utils import ArduinoNano, delay

keyboard = Controller()
board = ArduinoNano('/dev/ttyUSB0')

it =

nitro_button = board.get_pin('d:2:i')


def loop():
    pass


if __name__ == '__main__':
    while True:
        try:
            loop()
        except KeyboardInterrupt:
            print("Exiting...")
            exit()
