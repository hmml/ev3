"""Main module handling EV3 brick.

Responsible for initialization and deinitialization, buttons, LED light.
Defines multiple constants used in this module and various submodules.

Simple usage:
    >>> import ev3
    >>> ev3.open_all_devices()
    >>> ev3.set_led(ev3.LED_GREEN)

"""
import re
import time
import threading
from rawdevice import analogdevice, dcm, iicdevice, lcd, motordevice, sound, uartdevice, ui, lms2012

__version__ = '0.2'

_AMP_CIN = 22.0
_AMP_VIN = 0.5
_VCE = 0.05
_SHUNT_IN = 0.11
_AMP_COUT = 19.0
_SHUNT_OUT = 0.055
_events = {}

# EV3 brick buttons
BUTTON_UP = 0      #: button up
BUTTON_ENTER = 1   #: center button
BUTTON_DOWN = 2    #: button down
BUTTON_RIGHT = 3   #: button right
BUTTON_LEFT = 4    #: button left
BUTTON_BACK = 5    #: back button (top left)

# Sensor slots
SENSOR_1 = 0       #: sensor slot 1
SENSOR_2 = 1       #: sensor slot 2
SENSOR_3 = 2       #: sensor slot 3
SENSOR_4 = 3       #: sensor slot 4

# Motor slots
MOTOR_A = 0        #: motor slot A
MOTOR_B = 1        #: motor slot B
MOTOR_C = 2        #: motor slot C
MOTOR_D = 3        #: motor slot D

# EV3 led color
LED_BLACK = 0         #: no LED
LED_GREEN = 1         #: green LED
LED_RED = 2           #: green LED
LED_ORANGE = 3        #: orange LED
LED_GREEN_FLASH = 4   #: green LED flashing
LED_RED_FLASH = 5     #: red LED flashing
LED_ORANGE_FLASH = 6  #: orange LED flashing
LED_GREEN_PULSE = 7   #: green LED pulsing
LED_RED_PULSE = 8     #: red LED pulsing
LED_ORANGE_PULSE = 9  #: orange LED pulsing


def open_all_devices():
    """Open all devices for operation.

    Should be called before any interaction with EV3 brick or sensors.

    """
    analogdevice.open_device()
    dcm.open_device()
    iicdevice.open_device()
    lcd.open_device()
    motordevice.open_device()
    sound.open_device()
    uartdevice.open_device()
    ui.open_device()

    for port in range(0, 4):
        analogdevice.clear_change(port)
        uartdevice.reset(port)
        iicdevice.reset(port)


def close_all_devices():
    """Close all devices.

    """
    ui.close_device()
    uartdevice.close_device()
    sound.close_device()
    motordevice.close_device()
    lcd.close_device()
    iicdevice.close_device()
    dcm.close_device()
    analogdevice.close_device()


def get_battery():
    """Get battery status.

    Returns:
        tupple. (float, float, float)

    """
    CinV = lms2012.CtoV(
        float(analogdevice.get_analog().BatteryCurrent)) / _AMP_CIN
    battery_v = lms2012.CtoV(
        float(analogdevice.get_analog().Cell123456)) / _AMP_VIN + CinV + _VCE
    battery_i = CinV / _SHUNT_IN
    motor_i = lms2012.CtoV(
        float(analogdevice.get_analog().MotorCurrent) / _AMP_COUT) / _SHUNT_OUT
    return battery_v, battery_i, motor_i


def is_up_button_pressed():
    return ui.is_pressed(BUTTON_UP)


def is_down_button_pressed():
    return ui.is_pressed(BUTTON_DOWN)


def is_left_button_pressed():
    return ui.is_pressed(BUTTON_LEFT)


def is_right_button_pressed():
    return ui.is_pressed(BUTTON_RIGHT)


def is_enter_button_pressed():
    return ui.is_pressed(BUTTON_ENTER)


def is_button_pressed(button):
    """Check if given button is pressed.

    Args:
     button(int) values:
        - BUTTON_UP
        - BUTTON_ENTER
        - BUTTON_DOWN
        - BUTTON_RIGHT
        - BUTTON_LEFT
        - BUTTON_BACK

    Returns:
        bool.

    """
    return ui.is_pressed(button)


def set_led(light):
    """Set LED light on EV3 brick.

    Args:
       light (int):  LED to turn on.

    *light* values:
        - LED_BLACK
        - LED_GREEN
        - LED_RED
        - LED_ORANGE
        - LED_GREEN_FLASH
        - LED_RED_FLASH
        - LED_ORANGE_FLASH
        - LED_GREEN_PULSE
        - LED_RED_PULSE
        - LED_ORANGE_PULSE

    """
    ui.set_led(light)


def registerEvent(predicate, handle):
    events[predicate] = handle


def run():
    while True:
        if ui.is_pressed(BUTTON_BACK):
            break
        for predicate, handle in events.iteritems():
            if predicate():
                handle()
        time.sleep(0)
