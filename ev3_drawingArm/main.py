#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

import math
import time

import robotMath
from robotMath import SPEED

# Write your program here
# brick.sound.beep()

pen = Motor(Port.A)
arm1 = Motor(Port.C)
arm2 = Motor(Port.B)

pen.reset_angle(0)
arm2.reset_angle(0)
arm1.reset_angle(0)
# arm1.set_pid_settings(angle_tolerance = 0)
# arm2.set_pid_settings(angle_tolerance = 0)

# robotMath.penDown(True, pen)
# time.sleep(5)
# robotMath.penDown(False, pen)
#pen.run_target(50, -70)
robotMath.MoveTo(200, 0, arm1, arm2)
time.sleep(1)
robotMath.penDown(True, pen)
time.sleep(1)
robotMath.MoveTo(200, 40, arm1, arm2)
time.sleep(1)
robotMath.MoveTo(160, 40, arm1, arm2)
time.sleep(1)
robotMath.MoveTo(160, 0, arm1, arm2)
time.sleep(1)
robotMath.MoveTo(200, 20, arm1, arm2)
time.sleep(1)

robotMath.penDown(False, pen)
arm1.run_target(SPEED, 0)
arm2.run_target(SPEED, 0)