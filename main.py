import time
from typing import Dict, Tuple, Union

from pyfirmata import Pin, util
from pynput.keyboard import Controller, Key

from utils import ArduinoNano

keyboard = Controller()
board = ArduinoNano("/dev/ttyUSB0")
KeyType = Union[Key, str]


def press_if_open(pin: Pin, key: KeyType) -> None:
    """press key if pin is open (high)

    Args:
        pin (Pin): button to read input from
        key (Key, str): key to press when pin is open
    """
    was_open = prev_state.get(pin, False)  # get the state of the pin in prevous round
    is_pressed = is_key_pressed.get(pin, False)
    if pin.read() and not was_open:
        keyboard.press(key)
        prev_state[pin] = True
        is_pressed[pin] = True

    elif is_pressed:
        keyboard.release(key)
        prev_state[pin] = False
        is_pressed[pin] = False


class Button:
    def __init__(self, pin: str, key: KeyType) -> None:
        self.pin: Pin = board.get_pin(pin)
        self.state = False
        self.key = key


class TiltSensor:
    def __init__(self, pin: str) -> None:
        self.pin: Pin = board.get_pin(pin)
        self.state = False

    def read(self) -> bool:
        """returns the state of the pin (high or low).

        Returns:
            bool: True for high, False for low
        """
        return self.pin.read()


class SteerWheel:
    def __init__(self, left_sensor: TiltSensor, right_sensor: TiltSensor, keymap: dict):
        self.left_sensor = left_sensor
        self.right_sensor = right_sensor
        self.keymap = keymap
        # self.tilt_state: str = "straight"
        self.tilt_map = {
            (True, True): "straight",
            (True, False): "right",
            (False, True): "left",
            (False, False): "straight",  # for development
        }

    @property
    def tilt(self) -> Tuple[bool, bool]:
        return self.left_sensor.read(), self.right_sensor.read()

    @property
    def tilt_state(self) -> str:
        return self.tilt_map[self.tilt]

    def get_key(self) -> KeyType:
        """returns the key to press when the state is high

        Returns:
            KeyType: the key can be a attr of Key class or a string
        """
        return self.keymap[self.tilt_state]

    def __repr__(self):
        return f"SteerWheel({self.tilt_state})"


# def tilter() -> None:
#     # keys to press according to tilt state
#     cmds: Dict[bool_tuple, str] = {
#         (True, False): "a",
#         (False, True): "d",
#     }
#     # get the tilt state of both sides in previous round if not found return True for both
#     prev_tilt_state: bool_tuple = prev_state.get("tilt", (True, True))
#     curr_tilt_state: bool_tuple = tilt_sense_left.read(), tilt_sense_right.read()
#     if curr_tilt_state == (None, None):
#         return

#     is_state_changed: bool = prev_tilt_state != curr_tilt_state
#     if is_state_changed:
#         is_tilted: bool = not all(curr_tilt_state)
#         if prev_tilt_state != (True, True):
#             release_key: str = cmds[prev_tilt_state]
#             keyboard.release(release_key)

#         if is_tilted:
#             press_key: str = cmds[curr_tilt_state]
#             keyboard.press(press_key)

#     prev_state["tilt"] = curr_tilt_state
# start iterator to read pins without blocking main thread

it = util.Iterator(board)
it.start()

# button pin setup
nitro_btn: Pin = board.get_pin("d:2:i")
accel_btn: Pin = board.get_pin("d:3:i")
brake_btn: Pin = board.get_pin("d:4:i")

# tilt sensors
tilt_sense_left = TiltSensor("d:5:i")
tilt_sense_right = TiltSensor("d:6:i")

# stores infor about pins in the previous round of main loop

bool_tuple = Tuple[bool]
prev_state: Dict[Pin, Union[bool_tuple, bool]] = {}
is_key_pressed: Dict[KeyType, str], bool] = {}


def main() -> None:
    """run this code until arduino turns off"""
    # print(nitro_btn.read())
    press_if_open(nitro_btn, Key.space)
    press_if_open(accel_btn, "w")
    press_if_open(brake_btn, "s")
    tilter()
    print(
        nitro_btn.read(),
        accel_btn.read(),
        brake_btn.read(),
        tilt_sense_left.read(),
        tilt_sense_right.read(),
    )
    time.sleep(1)


if __name__ == "__main__":
    print("main program starting...")
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Exiting...")
            exit()
