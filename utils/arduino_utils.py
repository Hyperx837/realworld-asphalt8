from pyfirmata import Arduino


class Board(Arduino):
    def digital_write(self, pin, value):
        self.digital[pin].write(value)
