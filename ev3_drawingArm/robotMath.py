from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

import math
SPEED = 20.0

armX = -10
armY = 215 / 2
armLen1 = 90
armLen2 = 155

def penDown(down, pen):
    if down:
        pen.run_target(50, 80)
    else:
        pen.run_target(50, 0)

def DegreeFromSides(a, b, oppSq):
    ans = (a * a) + (b * b) - oppSq
    ans /= (2 * a * b)
    ans = math.acos(ans)
    return ans * 180 / math.pi

def MoveTo(x, y, arm1, arm2):
    distanceSq = (x - armX) * (x - armX) + (y - armY) * (y - armY)
    targetAngle2 = 180 - DegreeFromSides(armLen1, armLen2, distanceSq)
    targetAngle1 = - DegreeFromSides(armLen1, math.sqrt(distanceSq), armLen2 * armLen2) + math.atan2(y - armY, x - armX) * 180 / math.pi

    targetAngle1 = LimitAngle(targetAngle1, -130, 30)
    targetAngle2 = LimitAngle(targetAngle2, -90, 120)

    deltaAngle1 = math.fabs(targetAngle1 - arm1.angle())
    deltaAngle2 = math.fabs(targetAngle2 - arm2.angle())

    if deltaAngle1 >= deltaAngle2:
        speed1 = SPEED
        speed2 = deltaAngle2 / (deltaAngle1 / SPEED)
    else:
        speed2 = SPEED
        speed1 = deltaAngle1 / (deltaAngle2 / SPEED)

    speed1 = LimitAngle(speed1, 5, 70)
    speed2 = LimitAngle(speed2, 5, 70)

    arm1.run_target(speed1, targetAngle1, Stop.COAST, False)
    arm2.run_target(speed2, targetAngle2)

# def GetPosition(a1, a2):
#     a1 *= Math.PI / 180
#     a2 *= Math.PI / 180
#     return { "x": armX + armLen1 * math.cos(a1) + armLen2 * math.cos(a2 + a1), "y": armY + armLen1 * math.sin(a1) + armLen2 * math.sin(a2 + a1)) }

def LimitAngle(value, low, top):
    return max(min(value, top), low)