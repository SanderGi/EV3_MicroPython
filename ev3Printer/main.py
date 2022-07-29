#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

#brick.sound.beep()

from drawText import *
# SPEED = 100
# WriterCM = 110
# Width = 9.5 * WriterCM
# PaperCM = -85

colorSensor = ColorSensor(Port.S4)
pen = Motor(Port.A)
writer = Motor(Port.D)
paper = Motor(Port.C)

def calibrate():
    brick.display.text("Please place paper in machine and use buttons to adjust pen and writer")
    brick.display.text("Click center button when finished")
    paper.run_time(-200, 100000, Stop.COAST, False)
    stillrunning = True
    centerNotPressed = True
    while stillrunning:
        stillrunning = False
        if colorSensor.color() != None:
            paper.stop()
        else:
            stillrunning = True
        if Button.CENTER in brick.buttons():
            centerNotPressed = False
        if centerNotPressed:
            stillrunning = True
            if Button.LEFT in brick.buttons():
                writer.run(-200)
            elif Button.RIGHT in brick.buttons():
                writer.run(200)
            else:
                writer.stop()
            if Button.UP in brick.buttons():
                pen.run_angle(200, 20)
            elif Button.DOWN in brick.buttons():
                pen.run_angle(200, -20)
    writer.reset_angle(0)
    paper.reset_angle(0)
    pen.reset_angle(0)
    PenUp(pen)

def endJob():
    PenUp(pen)
    writer.run_target(200, 0)
    paper.run_time(200, 5000)

def changePen():
    pen.run_angle(200, 300)
    while Button.CENTER not in brick.buttons():
        pass
    pen.run_angle(200, -300)

calibrate()

# for character in alphabet:
#     index = 0
#     for dot in alphabet[character]:
#         if index > 2:
#             alphabet[character][index] = (dot[0] - 0.2, dot[1])
#         index += 1
# PenDown(pen)
# goto(writer, paper, 2, 4)
displayMessage(writer, paper, pen, "QRSTUVWX", 1, 0, -14)

endJob()

#SetPenDown(True)
#pen.run_angle(200, -70) # -: down, +: up
#writer.run_angle(SPEED, Width)