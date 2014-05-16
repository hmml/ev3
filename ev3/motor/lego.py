"""Classes for original Lego Mindstorms EV3 motors."""
from ..rawdevice import lms2012
from ..rawdevice import motordevice
import collections

MAX_SPEED_VALUE = 127

"""Class for manipulating a single instance of a motor.
   Motor must be one of ev3.MOTOR_* where * is A-D."""
class EV3Motor(object):
    MOVE_NONE = -1
    MOVE_BACKWARD = 0  
    MOVE_FORWARD = 1
    MAX_SPEED = 100
    UNKNOWN_SPEED = -1
    
    def __init__(self, port):
        self.port = port;
        self.port_mask = (1 << port);
        self.direction = self.MOVE_NONE
    
    """Private method for normalization the speed from 0-100 range to device's 0-127 range.
      (The device accepts values from 0-255 range however values above 128
      causes polarization to be inverted this is why 0-127 values are used to respect the direction
      passed to start())"""    
    def __to_max_speed(self, speed):
        speed = min(speed, self.MAX_SPEED)
        speed = max(speed, 0)
        speed = speed * MAX_SPEED_VALUE / self.MAX_SPEED;
        return speed
    
    """Private method for normalization the speed from device's 0-127 range to 0-100 range.
      See __to_max_speed()."""
    def __to_speed_range(self, speed):
        speed = min(speed, MAX_SPEED_VALUE)
        speed = max(speed, 0)
        speed = speed * self.MAX_SPEED / MAX_SPEED_VALUE;
        return speed
    
    """Starts the motor with the given direction and speed.
       The direction must be one of: MOVE_BACKWARD or MOVE_FORWARD.
       Speed must be in 1-100 range."""
    def start(self, direction, speed):
        if (direction == self.MOVE_NONE):
            return
        speed = self.__to_max_speed(speed)
        motordevice.reset(self.port_mask)
        self.set_direction(direction)
        motordevice.speed(self.port_mask, speed, True)
    
    def _set_direction(self, direction):
        print "_direction %d" % direction
        self.direction = direction

    """Sets motor's direction"""    
    def set_direction(self, direction):
        self._set_direction(direction)
        if (direction == self.MOVE_NONE):
            return
        print "direction %d" % direction
        motordevice.polarity(self.port_mask, direction)
    
    """Rotates the motor by the given angle at the given speed."""    
    def rotate(self, direction, speed, angle):
        motordevice.polarity(self.port_mask, direction)
        angle = max(0, angle);
        motordevice.step_speed(self.port_mask, speed, 0, angle, 0)
        
    """Stops the motor"""
    def stop(self):
        motordevice.stop(self.port_mask, False)
        self._set_direction(self.MOVE_NONE)
    
    """Sets motor's speed. If the motor is stopped it's started
       with the given speed and MOVE_FORWARD direction."""    
    def set_speed(self, speed):
        if (speed <= 0):
            self.stop()
            return
        if (self.get_direction() == self.MOVE_NONE):
            self.start(self.MOVE_FORWARD, speed)
            return

        speed = self.__to_max_speed(speed)
        motordevice.speed(self.port_mask, speed, True)

    """Accelerates the motor by the given delta.
       If (current speed + delta) exceeds the max speed limit
       the motor is accelerated to the max speed. If it runs with the max
       speed at time this is called this has no effect."""        
    def accelerate(self, delta):
        if (self.get_speed() == 0):
            self.start(self.MOVE_FORWARD, delta)
            return
        if (delta >= 0):
            delta = min(delta, self.MAX_SPEED)
            delta = max(delta, 0)
        else:
            delta = max(delta, -self.MAX_SPEED)
        self.set_speed(self.get_speed() + delta)
    
    """Same as accelerate() but it slows the motor down."""    
    def slow_down(self, delta):
        delta = abs(delta)
        self.accelerate(-delta)
    
    """Returns current speed of the motor."""    
    def get_speed(self):
        return self.__to_speed_range(motordevice.get_speed(self.port))
    
    """Returns current direction of the motor."""    
    def get_direction(self):
        return self.direction
    
    """Returns current tacho of the motor."""
    def get_tacho(self):
        if (self.get_direction() == self.MOVE_NONE):
            return motordevice.get_tacho(self.port)
        else:
            return motordevice.get_sensor(self.port)

    
"""Class for manipulating EV3 mindstorm robot's drive consisting of couple of motors.
   Motors can be manipulated at once and every one separately."""
class EV3Drive(EV3Motor):
    TURN_LEFT = 2
    TURN_RIGHT = 3
    MOTOR_ALL = 0xFF
        
    def __init__(self, motors):
        if not isinstance(motors, collections.Iterable):
            motors = [motors]
        motors = set(motors)
        self.map = {}
        self.motors = []
        self.port_mask = 0
        for index, motor_port in enumerate(set(motors)):
            self.map[motor_port] = index
            self.motors.insert(motor_port, EV3Motor(motor_port))
            self.port_mask |= 1 << motor_port
        self.direction = self.MOVE_NONE
     
    # Helper allowing to avoid code duplication   
    def __call_func(self, *args):
        which = args[len(args) - 1] # which must always be the last arg
        name = args[len(args) - 2] # name must always be the second arg from the end
        args = args[:len(args)-2] # remove which & name
        if not isinstance(which, collections.Iterable):
            which = [which]
        if (self.MOTOR_ALL in which):
            getattr(super(EV3Drive, self), name)(*args)
        else:
            for motor_index in set(which):
                if (motor_index in self.map):
                    getattr(self.motors[self.map[motor_index]], name)(*args)        
    
    """Similar to EV3Motor.start() with possibility to point at motor(s)
       which should be started."""
    def start(self, direction, speed, which = {MOTOR_ALL}):
        self.__make_sure_direction_is_consistent_everywhere(direction, which)
        self.__call_func(direction, speed, "start", which)
                    
    def __set_direction(self, direction, which):
        for motor_index in set(which):
            if (motor_index in self.map):
                self.motors[self.map[motor_index]]._set_direction(direction)
                
    def __make_sure_direction_is_consistent_everywhere(self, direction, which):
        if (self.MOTOR_ALL in which):
            self.__set_direction(direction, self.map.keys())
                    
    """Similar to EV3Motor.direction() with possibility to point at motor(s)
       polarity pf which should be changed."""    
    def set_direction(self, direction, which = {MOTOR_ALL}):
        if (direction == self.MOVE_NONE):
            return
        self.__make_sure_direction_is_consistent_everywhere(direction, which)
        self.__call_func(direction, "set_direction", which)

    
    """Similar to EV3Motor.rotate() with possibility to point at motor(s)
       which should be rotated."""        
    def rotate(self, direction, speed, angle, which = {MOTOR_ALL}):
        self.__call_func(direction, speed, angle, "rotate", which)
                    
    """Similar to EV3Motor.stop() with possibility to point at motor(s)
       which should be stopped."""    
    def stop(self, which = {MOTOR_ALL}):
        self.__make_sure_direction_is_consistent_everywhere(self.MOVE_NONE, which)        
        self.__call_func("stop", which)
                    
    """Similar to EV3Motor.set_speed() with possibility to point at motor(s)
       which should be applied the speed change."""    
    def set_speed(self, speed, which = {MOTOR_ALL}):
        self.__call_func(speed, "set_speed", which)
    
    """Similar to EV3Motor.accelerate() with possibility to point at motor(s)
       which should be accelerated."""    
    def accelerate(self, delta, which = {MOTOR_ALL}):
        if not isinstance(which, collections.Iterable):
            which = [which]
        # Not perfect but good enough. super(EV3Drive, self).accelerate() can't be called.
        if (self.MOTOR_ALL in which):
            for motor in self.motors:
                motor.accelerate(delta)
        else:
            for motor_index in set(which):
                if (motor_index in self.map):
                    self.motors[self.map[motor_index]].accelerate(delta)
                    
    """Similar to EV3Motor.accelerate() with possibility to point at motor(s)
       which should be slowed down."""    
    def slow_down(self, delta, which = {MOTOR_ALL}):
        if not isinstance(which, collections.Iterable):
            which = [which]
        # Not perfect but good enough. super(EV3Drive, self).slow_down() can't be called.
        if (self.MOTOR_ALL in which):
            for motor in self.motors:
                motor.slow_down(delta)
        else:
            for motor_index in set(which):
                if (motor_index in self.map):
                    self.motors[self.map[motor_index]].slow_down(delta)
                    
    """Gets speed of a one of the motors."""    
    def get_motor_speed(self, which):
        if (isinstance(which, collections.Iterable) or which == self.MOTOR_ALL or which not in self.map):
            return self.UNKNOWN_SPEED 
        else:
            return self.motors[self.map[which]].get_speed()
                 
        
    """Gets direction of a one of the motors."""
    def get_motor_direction(self, which):
        if (isinstance(which, collections.Iterable) or which == self.MOTOR_ALL or which not in self.map):
            return self.MOVE_NONE
        else:
            return self.motors[self.map[which]].get_direction()
        
    """Turns the drive be slowing down some of the motors to the given |steady_speed| and
       accelerating the other ones to |moving speed|.
       The direction of the turn is driven by |where| which either must be TURN_LEFT or
       must be TURN_RIGHT.
       If |in_place| is True motors which should be steady during the turn get the direction reverted
       to make turn faster (so when passing True as |in_place| it's recommended to pass same value as 
       |steady_speed| and |moving_speed|."""
    def turn(self, where, moving_speed, steady_speed, left_motors, right_motors, in_place):
        if (not isinstance(left_motors, collections.Iterable)):
            left_motors = [left_motors]
                 
        if (not isinstance(right_motors, collections.Iterable)):
            right_motors = [right_motors]

        direction = self.direction
        left_dir = self.get_motor_direction(left_motors[0])
        right_dir = self.get_motor_direction(right_motors[0])
        if (where == self.TURN_LEFT):
            left_speed = steady_speed
            right_speed = moving_speed
            if (in_place):
                if (direction == self.MOVE_FORWARD):
                    right_dir = self.MOVE_FORWARD
                    left_dir = self.MOVE_BACKWARD
                else:
                    right_dir = self.MOVE_BACKWARD
                    left_dir = self.MOVE_FORWARD
        else:
            left_speed = moving_speed
            right_speed = steady_speed
            if (in_place):
                if (direction == self.MOVE_FORWARD):
                    right_dir = self.MOVE_BACKWARD
                    left_dir = self.MOVE_FORWARD
                else:
                    right_dir = self.MOVE_FORWARD
                    left_dir = self.MOVE_BACKWARD
        
        self.set_speed(left_speed, left_motors)
        self.set_speed(right_speed, right_motors)
        self.set_direction(left_dir, left_motors)
        self.set_direction(right_dir, right_motors)

    
    
"""Class for manipulating EV3 mindstorm robot's canon."""
class EV3Canon(EV3Motor):
    UP = EV3Motor.MOVE_FORWARD
    STRAIGHT = EV3Motor.MOVE_BACKWARD
    MAX_POWER = EV3Motor.MAX_SPEED
    
    # |number_rotations_to_fire_one_bullet| depends on the construction i.e.
    # motor used cogwheels etc.
    def __init__(self, port, number_rotations_to_fire_one_bullet):
        super(EV3Canon, self).__init__(port)
        self.__bullet_coef = number_rotations_to_fire_one_bullet
        
    def shoot(self, direction, power, number_of_bullets):
        rot = 360 * number_of_bullets * self.__bullet_coef
        
        # current = abs(super(EV3Canon, self).get_tacho())
        # super(EV3Canon, self).start(direction, power)
        # target = current + rot
        
        # blocks until done.
        
        # while (True):
        #     current = abs(super(EV3Canon, self).get_tacho())
        #     if (current >= target):
        #         break
        # self.cease_fire()
        
        super(EV3Canon, self).rotate(direction, power, rot)
            
    def cease_fire(self):
        super(EV3Canon, self).stop()
                
        
__all__ = ['EV3Motor', 'EV3Drive', 'EV3Canon']
