from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

from threading import Thread
import math

SPEED = 100
WriterCM = 110
Width = 9.5 * WriterCM
PaperCM = 80

characterSpacing = 0.1
def displayMessage(writer, paper, pen, message, fontSize, xcm, ycm):
    for character in message:
        print(character)
        if character in alphabet:
            letter=alphabet[character]
            PenUp(pen)
            for dot in letter:
                #print(str(xcm + dot[0]*fontSize) + "||" + str(ycm + dot[1]*fontSize))
                goto(writer, paper, xcm + dot[0]*fontSize, ycm + dot[1]*fontSize)
                #wait(100) #####
                PenDown(pen)
            # dot = letter[len(letter) -1] #####
            # goto(writer, paper, xcm + dot[0]*fontSize, ycm + dot[1]*fontSize) ####
            xcm += fontSize
        elif character == " ":
            xcm += fontSize
        xcm += characterSpacing

def goto(writer, paper, xcm, ycm):
    dx = math.fabs(xcm * WriterCM - writer.angle())
    dy = math.fabs(ycm * PaperCM - paper.angle())
    hypo = math.sqrt(dx*dx + dy*dy) / SPEED
    if hypo == 0:
        print("dx: " + str(dx) + " dy: " + str(dy) + " Ax: " + str(xcm * WriterCM) + " Ay: " + str(ycm * PaperCM) + " hyp: " + str(hypo))
        return
    speedX = dx / hypo + 0.6
    speedY = dy / hypo + 0.6
    #print("Vx: " + str(speedX) + " Vy: " + str(speedX) + " Ax: " + str(xcm * WriterCM) + " Ay: " + str(ycm * PaperCM))
    if speedX >= 1: #and dx * WriterCM > 2:
        writer.run_target(speedX, xcm * WriterCM, Stop.COAST, False)
    else: print("  Vx: " + str(speedX - 0.6))
    if speedY >= 1: #and dy * PaperCM > 2:
        wait(40)
        paper.run_target(speedY, ycm * PaperCM)
    else:
        print("  Vy: " + str(speedY - 0.6))
        wait(xcm * WriterCM / speedX * 1000)
    while writer.speed() > 0 or paper.speed() > 0:
        wait(100)

#     dx = math.fabs(xcm * WriterCM - writer.angle())
#     dy = math.fabs(ycm * PaperCM - paper.angle())
#     speed = dy / dx * SPEED
#     w = Thread(target=func1, args=(writer, xcm))
#     p = Thread(target=func2, args=(paper, ycm, speed))
#     w.start()
#     p.start()
#     #print(min(dx, dy) / min(speed, SPEED) * 1000)
#     wait(min(dx, dy) / min(speed, SPEED) * 1000)

# def func1(writer, xcm):
#     writer.run_target(SPEED, xcm * WriterCM)

# def func2(paper, ycm, speed):
#     wait(300)
#     paper.run_target(speed, ycm * PaperCM)

def PenDown(pen):
    pen.run_target(200, 0)

def PenUp(pen):
    pen.run_target(200, 100)

alphabet = {
    'A': [(0.2,0),(0.5,1),(0.75,0.5),(0.25,0.5),(0.75,0.5),(1,0)],
    'B': [(0.2,0),(0.2,1),(0.625,1),(0.625,0.5),(0,0.5),(0.75,0.5),(0.75,0),(0,0)],
    'C': [(0.75,0),(0,0),(0,1),(0.75,1)],
    'D': [(0.2,0),(0.2,1),(0.625,1),(0.75,0.5),(0.625,0),(0,0)],
    'E': [(0.75,0),(0,0),(0,0.5),(0.75,0.5),(0,0.5),(0,1),(0.75,1)],
    'F': [(0.2,0),(0.2,0.5),(0.75,0.5),(0,0.5),(0,1),(0.75,1)],
    'G': [(0.75,0.5),(0.5,0.5),(0.75,0.5),(0.75,0),(0,0),(0,1),(0.75,1)],
    'H': [(0,0),(0,1),(0,0.5),(0.75,0.5),(0.75,1),(0.75,0)],
    'I': [(0,0),(0.5,0),(0.25,0),(0.25,1),(0,1),(0.5,1)],
    'J': [(0,0.125),(0.125,0),(0.375,0),(0.5,0.125),(0.5,1)],
    'K': [(0,0),(0,1),(0,0.5),(-0.1,0.5),(0.75,1),(-0.2,0.5),(0.75,0)],
    'L': [(0,0),(0,1),(0,0),(0.75,0)],
    'M': [(0,0),(0,1),(0.5,0),(1,1),(1,0)],
    'N': [(0,0),(0,1),(0.75,0),(0.75,1)],
    'O': [(0.4,0),(0,0.4),(0.4,1),(0.8,0.5),(0.3,0)],
    'P': [(0.2,0),(0.2,1),(0.75,1),(0.75,0.5),(0,0.5)],
    'Q': [(0.8,0),(0,0),(0,1),(0.8,1),(0.8,0),(0.4,0.4),(1,-0.2)],
    'R': [(0,0),(0,1),(0.75,1),(0.75,0.5),(0,0.5),(0.9,0)],
    'S': [(0,0),(0.8,0),(0.8,0.5),(0,0.5),(0,1),(0.8,1)],
    'T': [(0,1),(0.5,1),(0.5,0),(0.5,1),(1,1)],
    'U': [(0,1),(0,0.125),(0.125,0),(0.625,0),(0.75,0.125),(0.75,1)],
    'V': [(0,1),(0.375,0),(0.75,1)],
    'W': [(0,1),(0.25,0),(0.5,1),(0.75,0),(1,1)],
    'X': [(0,0),(0.375,0.5),(0,1),(0.375,0.5),(0.75,1),(0.375,0.5),(0.75,0)],
    'Y': [(0,1),(0.375,0.5),(0.375,0),(0.375,0.5),(0.75,1)],
    'Z': [(0,1),(0.75,1),(0,0),(0.75,0)],
}