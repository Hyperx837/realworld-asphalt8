import pyfirmata


class ArduinoNano(pyfirmata.Board):
    def __init__(self, *args, **kwargs):
        nano_layout = {
            'digital': (1, 0, *range(2, 14)),
            'analog': tuple(range(7)),
            'pwm': (3, 5, 6, 9, 10, 11),
            'use_ports': True,
            'disabled': (0, 1)
            # ''
        }
        super().__init__(layout=nano_layout, *args, **kwargs)
