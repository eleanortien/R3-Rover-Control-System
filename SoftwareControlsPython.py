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

defaultPMV = 128

#Sets each pin connection to servo motor
motorList = [leftW1, leftW2, leftW3, rightW1, rightW2, rightW3, ledRed, ledBlue, ledGreen, upperExt, lowerEXT, hoist, screwdriver, claw, swivel]
for pin in motorList:
    board.digital[pin].mode = SERVO

#HOPEFULLY allows Python to communicate with Arduino via sockets
host = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host.bind(compIp, serverPort) #Talk to Arduino

data, addr = host.recvfrom(1024) 
data.close()

def drive(lw1, rw1, lw2, rw2, lw3, rw3):
    host.sendto(str.encode("DriveCommand_" + str(lw1) + "_" + str(rw1) + "_" + str(lw2) + "_" + str(rw2) + "_" + str(lw3) + "_" + str(rw3)), addr)
#Keyboard Inputs
#Initializing controller
pygame.joystick.init()
for i in range(pygame.joystick.getcount()):
    joysticks = [pygame.joystick.Joystick(i)]

for event in pygame.event.get():
    if event.type == pygame.JOYAXISMOTION:
        if event.axis < 2:
            drive()



