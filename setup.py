#!/usr/bin/env python
from distutils.core import setup

setup(name='python-ev3',
      version='0.2',
      description='Python library for Lego Mindstorms EV3',
      author='Gong Yi, hmml',
      author_email='topikachuthoruuu@163.com, hmml.code@gmail.com',
      url='https://github.com/hmml/ev3',
      packages=['ev3', 'ev3.rawdevice', 'ev3.motor', 'ev3.sensor']
      )
