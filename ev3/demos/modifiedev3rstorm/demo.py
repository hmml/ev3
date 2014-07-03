import ev3
from ev3.motor.lego import *
from ev3.robot.lego import *
from ev3.sensor.lego import *
import sys
import time
from threading import Timer

# TODO: there's a lot of similar code. Share as much as possible
# instead of copypasta.

class ModifiedEV3RStormRobotConfig(EV3RobotConfigurator):
    _is_init = False
    def setup(self):
        if not self._is_init:          
            self.drive = EV3Drive([ev3.MOTOR_B, ev3.MOTOR_C])
            self.canon = EV3Canon(ev3.MOTOR_A, 3)
            self.touch_sensor = EV3TouchSensor(ev3.SENSOR_1)
            self.color_sensor = EV3ColorSensor(ev3.SENSOR_3)
            self.ir_sensor = EV3IRSensor(ev3.SENSOR_4)
            self._is_init = True
        self.ir_sensor.set_proximity_mode()
        ev3.set_led(ev3.LED_GREEN_PULSE)
        self.color_sensor.set_reflect_mode()
        
    def tear_down(self):
        ev3.set_led(ev3.LED_GREEN)
        
    def get_left_motors(self):
        return ev3.MOTOR_B
    
    def get_right_motors(self):
        return ev3.MOTOR_C

        
class ModifiedEV3RStormRobotDriver_1(EV3RobotDriver):
    speed = EV3Motor.MAX_SPEED / 4
    turn_time = 1.55 # time based turning - not the most accurate - depends on speed.
    close_to_object_ir_threshold = 25
    close_to_object_cs_threshold = 2
 
    def __init__(self, configurator):
        super(ModifiedEV3RStormRobotDriver_1, self).__init__(configurator)
        
    def _is_close_to_object(self):
        return self.configurator.ir_sensor and self.configurator.color_sensor and \
            (self.configurator.ir_sensor.get_distance() <= self.close_to_object_ir_threshold or \
            self.configurator.color_sensor.get_value() >= self.close_to_object_cs_threshold)
    
    def _change_direction(self):
        # Check right side.
        ev3.unregisterEvent(self._is_close_to_object)
        ev3.set_led(ev3.LED_RED_PULSE)
        ev3.motor.lego.turn(self.configurator.drive,
                            EV3Drive.TURN_RIGHT,
                            self.speed,
                            self.speed,
                            self.configurator.get_left_motors(),
                            self.configurator.get_right_motors(),
                            True)
        time.sleep(self.turn_time)
        self.configurator.drive.stop()
        if self._is_close_to_object():
            # Right side is not good, turn left 
            ev3.motor.lego.turn(self.configurator.drive,
                                EV3Drive.TURN_LEFT,
                                self.speed,
                                self.speed,
                                self.configurator.get_left_motors(),
                                self.configurator.get_right_motors(),
                                True)
            time.sleep(2 * self.turn_time)
            self.configurator.drive.stop()
            
        if self._is_close_to_object():
            # Left is not good, go back.
            ev3.motor.lego.turn(self.configurator.drive,
                                EV3Drive.TURN_LEFT,
                                self.speed,
                                self.speed,
                                self.configurator.get_left_motors(),
                                self.configurator.get_right_motors(),
                                True)
            time.sleep(self.turn_time)
            self.configurator.drive.stop()
        self.configurator.drive.start(EV3Motor.MOVE_FORWARD, self.speed)
        ev3.set_led(ev3.LED_GREEN_PULSE)
        ev3.registerEvent(self._is_close_to_object, self._change_direction)            
        
    def start(self):
        print "Starting 1"
        super(ModifiedEV3RStormRobotDriver_1, self).start()
        if not self.configurator.drive:
            print "No drive no fun. Quitting."
            return
        
        # Go forward with 1/4 speed
        self.configurator.drive.start(EV3Motor.MOVE_FORWARD, self.speed)
        ev3.registerEvent(self.configurator.touch_sensor.is_pressed, self.stop)
        ev3.registerEvent(self._is_close_to_object, self._change_direction)
        
        
    def stop(self):
        if self.configurator.drive:
            self.configurator.drive.stop()
            ev3.unregisterEvent(self.configurator.touch_sensor.is_pressed)
            ev3.unregisterEvent(self._is_close_to_object)
        super(ModifiedEV3RStormRobotDriver_1, self).stop()
        
class ModifiedEV3RStormRobotDriver_2(ModifiedEV3RStormRobotDriver_1):
    def __init__(self, configurator):
        super(ModifiedEV3RStormRobotDriver_2, self).__init__(configurator)

    def _change_direction(self):
        # Check right side.
        ev3.unregisterEvent(self._is_close_to_object)
        ev3.set_led(ev3.LED_RED_PULSE)
        ev3.motor.lego.turn(self.configurator.drive,
                            EV3Drive.TURN_RIGHT,
                            self.speed,
                            self.speed,
                            self.configurator.get_left_motors(),
                            self.configurator.get_right_motors(),
                            True)
        time.sleep(self.turn_time)
        self.configurator.drive.stop()
        distance_right = self.configurator.ir_sensor.get_distance()
        if distance_right <= 73:
            # There is some object in sight. Check left. 
            ev3.motor.lego.turn(self.configurator.drive,
                                EV3Drive.TURN_LEFT,
                                self.speed,
                                self.speed,
                                self.configurator.get_left_motors(),
                                self.configurator.get_right_motors(),
                                True)
            time.sleep(2 * self.turn_time)
            self.configurator.drive.stop()
            distance_left = self.configurator.ir_sensor.get_distance()    
            if distance_left <= self.close_to_object_ir_threshold and distance_right <= self.close_to_object_ir_threshold:
                # Left is not good. Same right. Go back.
                ev3.motor.lego.turn(self.configurator.drive,
                                    EV3Drive.TURN_LEFT,
                                    self.speed,
                                    self.speed,
                                    self.configurator.get_left_motors(),
                                    self.configurator.get_right_motors(),
                                    True)
                time.sleep(self.turn_time)
                self.configurator.drive.stop()
            else:
                if distance_right >= distance_left: # Go right
                    ev3.motor.lego.turn(self.configurator.drive,
                                        EV3Drive.TURN_RIGHT,
                                        self.speed,
                                        self.speed,
                                        self.configurator.get_left_motors(),
                                        self.configurator.get_right_motors(),
                                        True)
                    time.sleep(2 * self.turn_time)
                # else go left
                    
        self.configurator.drive.start(EV3Motor.MOVE_FORWARD, self.speed)
        ev3.set_led(ev3.LED_GREEN_PULSE)
        ev3.registerEvent(self._is_close_to_object, self._change_direction)
        
    def start(self):
        print "Starting 2"
        super(ModifiedEV3RStormRobotDriver_2, self).start()


class ModifiedEV3RStormRobotDriver_3(ModifiedEV3RStormRobotDriver_1):
    _KEY_LEFT = 0
    _KEY_RIGHT = 1
    _KEY_UP = 2
    _KEY_DOWN = 3
    _KEY_ENTER = 4
    _KEYS_NUM = 5
    
    _DIR_LEFT = 0
    _DIR_RIGHT = 1
    _DIR_STRAIGHT = 2
    _DIR_BACK = 3
    _DIR_NONE = 4
    
    _STARTING = -1
    _WAIT_FOR_DIR = 0
    _WAIT_FOR_TIME = 1
    
    _TIME_RESOLUTION = 2

    def __init__(self, configurator):
        super(ModifiedEV3RStormRobotDriver_3, self).__init__(configurator)
        self._path = []
        self._current_dir = self._DIR_NONE
        self._current_time = 0
        self._mode = self._STARTING
        self._timer = None
        self._old_handler = [None] * self._KEYS_NUM
        self.close_to_object_cs_threshold = 1
        
    def key_to_dir(self, key):
        return key # key enum & dir enum are in sync.
    
    def _register_for_keys(self):
        self._old_handler[self._KEY_ENTER] = ev3.registerEvent(ev3.is_enter_button_pressed,
                                                               self._enter_key_pressed)
        self._old_handler[self._KEY_UP] = ev3.registerEvent(ev3.is_up_button_pressed,
                                                            self._up_pressed)
        self._old_handler[self._KEY_DOWN] = ev3.registerEvent(ev3.is_down_button_pressed,
                                                              self._down_pressed)
        self._old_handler[self._KEY_LEFT] = ev3.registerEvent(ev3.is_left_button_pressed,
                                                              self._left_pressed)
        self._old_handler[self._KEY_RIGHT] = ev3.registerEvent(ev3.is_right_button_pressed,
                                                               self._right_pressed)
        
    def _unregister_from_keys(self):
        # TODO this deserves a loop.
        ev3.unregisterEvent(ev3.is_enter_button_pressed)
        if self._old_handler[self._KEY_ENTER]:
            ev3.registerEvent(ev3.is_enter_button_pressed, 
                              self._old_handler[self._KEY_ENTER]['handle'],
                              *(self._old_handler[self._KEY_ENTER]['args']))
        ev3.unregisterEvent(ev3.is_up_button_pressed)
        if self._old_handler[self._KEY_UP]:
            ev3.registerEvent(ev3.is_up_button_pressed,
                              self._old_handler[self._KEY_UP]['handle'],
                              *(self._old_handler[self._KEY_UP]['args']))
        ev3.unregisterEvent(ev3.is_down_button_pressed)
        if self._old_handler[self._KEY_DOWN]:
            ev3.registerEvent(ev3.is_down_button_pressed,
                              self._old_handler[self._KEY_DOWN]['handle'],
                              *(self._old_handler[self._KEY_DOWN]['args']))
        ev3.unregisterEvent(ev3.is_left_button_pressed)
        if self._old_handler[self._KEY_LEFT]:
            ev3.registerEvent(ev3.is_left_button_pressed,
                              self._old_handler[self._KEY_LEFT]['handle']
                              *(self._old_handler[self._KEY_LEFT]['args']))
        ev3.unregisterEvent(ev3.is_right_button_pressed)
        if self._old_handler[self._KEY_RIGHT]:
            ev3.registerEvent(ev3.is_right_button_pressed,
                              self._old_handler[self._KEY_RIGHT]['handle']
                              *(self._old_handler[self.KEY_RIGHT]['args']))
        
    def _register_for_keys_no_recovery(self):
        ev3.registerEvent(ev3.is_enter_button_pressed, self._enter_key_pressed)
        ev3.registerEvent(ev3.is_up_button_pressed, self._up_pressed)
        ev3.registerEvent(ev3.is_down_button_pressed, self._down_pressed)
        ev3.registerEvent(ev3.is_left_button_pressed, self._left_pressed)
        ev3.registerEvent(ev3.is_right_button_pressed, self._right_pressed)
        
    def _unregister_from_keys_no_recovery(self):
        # TODO this deserves a loop.
        ev3.unregisterEvent(ev3.is_enter_button_pressed)
        ev3.unregisterEvent(ev3.is_up_button_pressed)
        ev3.unregisterEvent(ev3.is_down_button_pressed)
        ev3.unregisterEvent(ev3.is_left_button_pressed)
        ev3.unregisterEvent(ev3.is_right_button_pressed)
        
    def _go(self):
        ev3.set_led(ev3.LED_GREEN)
        ev3.registerEvent(self.configurator.touch_sensor.is_pressed, self.stop)
        ev3.registerEvent(self._is_close_to_object, self._next_step, True)
        self._next_step()
        
    def _next_step(self, because_is_close_to_object=False):
        if because_is_close_to_object:
            # Unregister to avoid spam until the object is avoided.
            ev3.unregisterEvent(self._is_close_to_object)
        else:
            # Might have been unregistered so make sure it's always registered.
            ev3.registerEvent(self._is_close_to_object, self._next_step, True)
        if self._timer:
            self._timer.cancel()
        self.configurator.drive.stop()
        # print "Close to object {0}".format(because_is_close_to_object)
        if len(self._path) > 0:
            moves = self._path[0]
            del self._path[0]
            move = moves[0]
            time = moves[1]
            # print "Move -> time {0} {1}".format(move, time)
            # Skip going forward if there's some obstackle in the way.
            self._timer = Timer(time if not because_is_close_to_object or move != self._DIR_STRAIGHT else 0,
                                self._next_step)
            self._timer.start()
            if move == self._DIR_STRAIGHT:
                if not because_is_close_to_object:
                    self.configurator.drive.start(EV3Drive.MOVE_FORWARD, self.speed)
            else:
                ev3.motor.lego.turn(self.configurator.drive,
                                    EV3Drive.TURN_LEFT if move == self._DIR_LEFT else EV3Drive.TURN_RIGHT,
                                    self.speed,
                                    self.speed,
                                    self.configurator.get_left_motors(),
                                    self.configurator.get_right_motors(),
                                    True)
        else:
            self.start()
        
    def start(self):
        print "Starting 3"
        if not self.configurator.drive:
            print "No drive no fun. Quitting."
            return
        
        ev3.set_led(ev3.LED_ORANGE_PULSE)
        self._register_for_keys()
    
    def _enter_key_pressed(self):
        time.sleep(0.75) # prevents key events spam (make a constant out of this!)
        if self._mode == self._STARTING:
            self._mode = self._WAIT_FOR_DIR
            return
            
        if self._mode == self._WAIT_FOR_TIME:
            # No spam while handling an event, please.
            self._unregister_from_keys_no_recovery()
            self._path.append([self._current_dir, self._current_time])
            self._current_dir = self._DIR_NONE
            self._current_time = 0
            self._mode = self._WAIT_FOR_DIR
            ev3.set_led(ev3.LED_ORANGE_PULSE)
            # Done. Carry on.
            self._register_for_keys_no_recovery()
        else:
            self._unregister_from_keys()
            self._go()
            
        
    def _arrow_key_pressed(self, key):
        time.sleep(0.75) # prevents key events spam
        if key == self._KEY_DOWN and self._mode == self._WAIT_FOR_DIR:
            # Don't go backwards.
            return
        # No spam while handling an event, please.
        self._unregister_from_keys_no_recovery()
        if self._mode == self._WAIT_FOR_DIR:
            self._current_dir = self.key_to_dir(key)
            print "Go to {0}...".format(self._current_dir)
            self._current_time = 0
            self._mode = self._WAIT_FOR_TIME
            ev3.set_led(ev3.LED_RED_PULSE)
        elif key == self._KEY_DOWN:
            self._current_time = self._current_time + self._TIME_RESOLUTION
            print "... for {0} secs...".format(self._current_time)
        # Done. Carry on.
        self._register_for_keys_no_recovery()
    
    def _up_pressed(self):
        self._arrow_key_pressed(self._KEY_UP)
        
    def _down_pressed(self):
        self._arrow_key_pressed(self._KEY_DOWN)
        
    def _left_pressed(self):
        self._arrow_key_pressed(self._KEY_LEFT)
        
    def _right_pressed(self):
        self._arrow_key_pressed(self._KEY_RIGHT)

    def stop(self):
        if self._timer:
            self._timer.cancel()
        if self.configurator.drive:
            self.configurator.drive.stop()
            ev3.unregisterEvent(self.configurator.touch_sensor.is_pressed)
        super(ModifiedEV3RStormRobotDriver_1, self).stop()


def get_driver(config):
    if len(sys.argv) < 2  or sys.argv[1] == "1":
        print "Variant 1"
        driver = ModifiedEV3RStormRobotDriver_1(config)
    elif sys.argv[1] == "2":
        print "Variant 2"
        driver = ModifiedEV3RStormRobotDriver_2(config)
    else:
        print "Variant 3"
        driver = ModifiedEV3RStormRobotDriver_3(config)
        
    return driver


if __name__ == "__main__":
    ev3.open_all_devices()

    robot = EV3Robot()
    
    robot.setup(get_driver(ModifiedEV3RStormRobotConfig()))
    
    ev3.registerEvent(ev3.is_enter_button_pressed, robot.start)

    print "Ready..."
    ev3.run()

    print "Done..."
    ev3.set_led(ev3.LED_BLACK)
    ev3.close_all_devices()
