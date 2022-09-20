from pyfirmata import Arduino, SERVO, util
from time import sleep
import socket
import pygame

#Variable Setup
ardPort = "com3" #Write com connected to Arduino here
board = Arduino(ardPort)
delay = 0.015
serverPort = 8090
compIp = '169.254.15.133'
echoNum = 1024

#Drive Pin Numbers
leftW1 = 11
leftW2 = 12
leftW3 = 24
rightW1 = 25
rightW2 = 28
rightW3 = 29
ledRed = 33
ledBlue = 34
ledGreen = 35

#Arm Pin Numbers
upperExt = 24
lowerEXT= 29
hoist = 25
screwdriver = 11
claw = 28
swivel = 12

#Sets each pin connection to servo motor
motorList = [leftW1, leftW2, leftW3, rightW1, rightW2, rightW3, ledRed, ledBlue, ledGreen, upperExt, lowerEXT, hoist, screwdriver, claw, swivel]
for pin in motorList:
    board.digital[pin].mode = SERVO

#HOPEFULLY allows Python to communicate with Arduino via sockets
host = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host.bind(compIp, serverPort) #Talk to Arduino

data, addr = host.recvfrom(1024) 
data.close()

def drive(lw1 = 128, rw1 = 128, lw2 = 128, rw2 = 128, lw3 = 128, rw3 = 128):
    host.sendto(str.encode("DriveCommand_" + str(lw1) + "_" + str(rw1) + "_" + str(lw2) + "_" + str(rw2) + "_" + str(lw3) + "_" + str(rw3)), addr)
#Keyboard Inputs
#Initializing controller
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            if event.axis < 2:
                #Check left joystick controls 
                if joysticks[0].get_axis(0):
                    print("left joystick")
                    drive()
        



