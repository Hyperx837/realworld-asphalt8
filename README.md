# Real World - Asphalt8

real world asphalt (RWA in short) is a physical controller for Asphalt8 (by changing keys can be used in other games). Since python can't directly communicate with arduino firmata is used as a bridge. following are some demos of the project.

<img src="./demos/front.jpeg" alt="front" width="300">
<img src="./demos/side.jpeg" alt="side" width="300" align="right">
<br><br>
<img src="./demos/output.gif">

### How it works?

there are two buttons under each paddle that you see in the image. there is another button close to the right hand in the steering wheel. and steering wheel is attached to a potentiometer. when a button is pressed the program identifies the signal and then presses the key accordingly. when steering wheel is turned program identifies whether it's center, left or right according to the tilt. all the keys can be pressed parallely. here are the buttons and the keys supposed to be pressed.

**_Buttons_**

- **Accelerator Button (right paddle)** - w
- **Brake Button (left paddle)** - s
- **Nitro Button (Steer Wheel)** - space

**_Steer Wheel_**

- **Straight** - Nothing
- **Left** - a
- **Right** - d

### Prerequisites

- Python 3.7 or later
- poetry (optinal)
- an arduino
- 3 buttons (script will run without buttons)
- Arduino IDE (btw if we call it an IDE vim is an OS)

### Getting started

Install arduino IDE from [www.arduino.cc](https://www.arduino.cc/) and install it.

upload the Standardfirmata sketch to
the arduino from firmata library.

first clone the project cd into it

```
git clone https://github.com/Anu2001dev/realworld-asphalt8
cd realworl-asphalt8
```

installs deps. you can install via pip but poetry is recommended for maintainability

`pip`

```
pip installl -r requirements.txt
```

`poetry`

```
poetry install
```

finally

```
python main.py
```

## Built With

- [Poetry](https://python-poetry.org/) - Dependency Management
- [Rich](https://github.com/willmcgugan/rich) - Logging Colorized Output
- [Pyfirmata](https://github.com/tino/pyFirmata) - Python Firmata Client
- [PyAutoGUI](https://github.com/asweigart/pyautogui) - Pressing Keys

## Builders

- **Me** - Code
- **Visal Ranindu** - All the mechanical work (Although he doesn't know any coding he is a great engineer)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
