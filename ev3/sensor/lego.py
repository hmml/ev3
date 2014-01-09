"""Classes for original Lego Mindstorms EV3 sensors.

Supported sensors:
    - Color sensor
    - Infrared sensor
    - Touch sensor

"""
import sensor
from ..rawdevice import lms2012


class EV3ColorSensor(sensor.UartSensor):
    """Color sensor.

    Sensor can operate in 3 different modes:
        - reflection
        - ambient
        - color

    In color mode sensor detects one of the following colors:
        - COLOR_NONE
        - COLOR_BLACK
        - COLOR_BLUE
        - COLOR_GREEN
        - COLOR_YELLOW
        - COLOR_RED
        - COLOR_WHITE
        - COLOR_BROWN

    Args:
        port(int): possible values:
            - ev3.SENSOR_1
            - ev3.SENSOR_2
            - ev3.SENSOR_3
            - ev3.SENSOR_4

    """

    COLOR_NONE = 0
    COLOR_BLACK = 1
    COLOR_BLUE = 2
    COLOR_GREEN = 3
    COLOR_YELLOW = 4
    COLOR_RED = 5
    COLOR_WHITE = 6
    COLOR_BROWN = 7

    def __init__(self, port):
        self.port = port
        super(EV3ColorSensor, self).__init__(port)

    def set_reflect_mode(self):
        """Set reflection mode.

        """
        self.set_mode(0)

    def set_ambient_mode(self):
        """Set ambient mode.

        """
        self.set_mode(1)

    def set_color_mode(self):
        """Set color mode.

        """
        self.set_mode(2)

    def set_ref_raw_mode(self):
        self.set_mode(3)

    def set_rgb_raw_mode(self):
        self.set_mode(4)

    def set_col_cal_mode(self):
        self.set_mode(5)

    def get_value(self):
        """Get sensor value.

        Returns:
            int.

            In ambient mode::
                0 -- total darkness
                74 -- direct light

            In reflect mode::
                TODO

            In color mode::
                0 -- 7 (COLOR_NONE, COLOR_BLACK, COLOR_BLUE, COLOR_GREEN, COLOR_YELLOW, COLOR_RED, COLOR_WHITE, COLOR_BROWN)

        """
        return super(EV3ColorSensor, self).get_value()

    def color_to_string(self):
        """Get string representation of color (use in *color mode*).

        Returns:
            string. One of ("NONE", "BLACK", "BLUE", "GREEN", "YELLOW", "RED", "WHITE", "BROWN")

        """
        return ["NONE", "BLACK", "BLUE", "GREEN", "YELLOW", "RED", "WHITE", "BROWN"][self.get_value()]


class EV3IRSensor(sensor.UartSensor):
    """Infrared sensor.

    Sensor can operate in three diffrent modes:
        - proximity
        - seek
        - remote control

    Args:
        port(int): possible values:
            - ev3.SENSOR_1
            - ev3.SENSOR_2
            - ev3.SENSOR_3
            - ev3.SENSOR_4

    """

    BUTTON_NONE = 0
    BUTTON_TOP_LEFT = 1
    BUTTON_BOTTOM_LEFT = 2
    BUTTON_TOP_RIGHT = 3
    BUTTON_RIGHT = 4
    BUTTON_TOP_LEFT_TOP_RIGHT = 5
    BUTTON_TOP_LEFT_BOTTOM_RIGHT = 6
    BUTTON_BOTTOM_LEFT_TOP_RIGHT = 7
    BUTTON_BOTTOM_LEFT_BOTTOM_RIGHT = 8
    BUTTON_CENTRE_BEACON = 9
    BUTTON_BOTTOM_LEFT_TOP_LEFT = 10
    BUTTON_TOP_RIGHT_BOTTOM_RIGHT = 11

    CHANNEL_1 = 0
    CHANNEL_2 = 1
    CHANNEL_3 = 3
    CHANNEL_4 = 4

    def __init__(self, port):
        self.port = port
        super(EV3IRSensor, self).__init__(port)

    def set_proximity_mode(self):
        """Set proximity mode.

        """
        self.set_mode(0)

    def set_seek_mode(self):
        """Set seek mode.

        """
        self.set_mode(1)

    def set_remote_control_mode(self):
        """Set remote control mode.

        """
        self.set_mode(2)

    def get_distance(self):
        """Get distance (use in proximity mode).

        Returns:
            int. The return values in range::

               0 -- close
               100 -- far away

        .. note::
            I got 67 as maximum distance value.

        """
        return self.get_value()

    def get_remote_control_command(self, channel=CHANNEL_1):
        """Get remote command (use in remote control mode).

        Returns:
            int. One of the BUTTON_* values.

        .. note::
            CHANNEL_1 is top position of switch.

        """
        return self.get_value_bytes()[chan]

    def get_direction_and_distance(self, channel=CHANNEL_1):
        """Get direction and distance (use in seek mode).

        Returns:
            tupple, (direction(int), distance(int))::

               direction: -25 (left) -- +25 (right)
               distance: 1 -- 100

        Notes:
            CHANNEL_1 is top position of switch.

        """
        return self.get_all_direction_and_distance()[chan]

    def get_all_directions_and_distances(self):
        """Get direction and distance for all channels (use in seek mode).

        Returns:
            list, [(direction(int), distance(int)) x 4]::

               direction: -25 (left) -- +25 (right)
               distance: 1 -- 100

        .. note::

            Empty channel return (0, -128).
            CHANNEL_1 is top position of switch.

        """
        allchannels = self.get_value_bytes()[0:8]
        i = 0
        values = []
        while (i < 4):
            values.append((allchannels[i * 2], allchannels[i * 2 + 1]))
            i += 1
        return values


class EV3TouchSensor(sensor.AnalogSensor):
    """Touch sensor.

    Args:
        port(int): possible values:
            - ev3.SENSOR_1
            - ev3.SENSOR_2
            - ev3.SENSOR_3
            - ev3.SENSOR_4

    """
    def __init__(self, port):
        self.port = port
        super(EV3TouchSensor, self).__init__(port)

    def is_pressed(self):
        """Check if touch sensor button is pressed.

        Returns:
            bool.

        """
        return self.get_pin6_value() > lms2012.ADC_REF / 2


__all__ = ['EV3IRSensor', 'EV3TouchSensor', 'EV3ColorSensor']
