""" The interface class providing the way to configure an EV3 lego robot. 

    The robot is represented by an instance of EV3Robot class.
    This is meant to be derived from and passed to EV3RobotDriver instance.
"""
class EV3RobotConfigurator(object):
    drive = None
    touch_sensor = None
    ir_sensor = None
    color_sensor = None
    touch_sensor = None
     
    def setup(self):
        pass
    
    def tear_down(self):
        pass
    
    def get_left_motors(self):
        return None
    
    def get_right_motors(self):
        return None

""" The interface class providing the way to drive an EV3 lego robot.

    The robot is represented by an instance of EV3Robot class.
    This is meant to be derived from and passed to EV3Robot instance.
"""
class EV3RobotDriver(object):
    def __init__(self, configurator):
        self.configurator = configurator
            
    def setup(self):
        self.configurator.setup()
        
    def tear_down(self):
        self.configurator.tear_down()
        
    def start(self):
        pass
    
    def stop(self):
        pass

""" The class representing an EV3 lego robot. """        
class EV3Robot(object):
    _driver = None
    def setup(self, driver):
        if self._driver:
            self._driver.tear_down()

        self._driver = driver
        driver.setup()
        
    def tear_down(self):
        self._driver.tear_down()

    def start(self):
        self._driver.start()
        
    def stop(self):
        self._driver.stop()


__all__ = ['EV3RobotConfigurator', 'EV3RobotDriver', 'EV3Robot']