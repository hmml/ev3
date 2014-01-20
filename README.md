Program Lego Mindstorms EV3 in Python
=======================================

Before you start
----------------
You need to have [custom distribution](https://github.com/hmml/python-ev3). Prebuild image may not come with the latest version of ev3 module so make sure you follow instuction below to update it.


Quick start
-----------

Once you have a working environment, connect to EV3 brick and launch Python (executed on EV3RSTORM):

    $ ssh root@10.0.1.1
    root@python-ev3:~# python      
    [GCC 4.6.3] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import ev3
    >>> ev3.open_all_devices()
    >>> ev3.get_battery()
    (6911.138911088911, 46.41822823641005, 0.0)
    >>> ev3.set_led(ev3.LED_GREEN)
    >>> ev3.close_all_devices()
    
Reading sensors:    
    
    >>> import ev3
    >>> from ev3.sensor.lego import EV3TouchSensor
    >>> ev3.open_all_devices()
    >>> touch_sensor = EV3TouchSensor(ev3.SENSOR_1)
    >>> while True:
    ...     if touch_sensor.is_pressed(): print "pressed"
    ... 
    pressed    # I've pressed touch sensor
    (ctrl+c to break the loop)
    
### Documentation

Generated documentation available at [readthedocs.org](http://ev3.readthedocs.org/en/latest/).


Status
------

Some parts are still not implemented or lack high level API - pull requests are welcome.


Updating module on EV3 brick
----------------------------

Configuring key based authorisation. This step is required only once:

	$ ssh root@10.0.1.1 mkdir -p .ssh
	$ cat ~/.ssh/id_rsa.pub | ssh root@10.0.1.1 'cat >> .ssh/authorized_keys'

Whenever you want to update `ev3` module just invoke:

	$ ./update.sh

*Note: this may take a while.*

