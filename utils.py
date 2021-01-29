import glob

import pyfirmata


class ArduinoNano(pyfirmata.Board):
    def __init__(self, *args, **kwargs):
        layout = {
            "digital": (1, 0, *range(2, 14)),
            "analog": tuple(range(7)),
            "pwm": (3, 5, 6, 9, 10, 11),
            "use_ports": True,
            "disabled": (0, 1)
            # ''
        }
        (port,) = glob.glob("/dev/ttyUSB*")
        super().__init__(layout=layout, port=port, *args, **kwargs)
