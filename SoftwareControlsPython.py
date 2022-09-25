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

#Controller Values
leftStick = 0
rightStick = 1
threshhold = 0.1

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
    l1, l2, l3, r1, r2, r3 = 128
    wheelsFinal = [lw1, lw2, lw3, rw1, rw2, rw3]
    wheels = [l1, l2, l3, r1, r2, r3] 
    #Increment the motor turn??
    for i in range(128): #Increment motor starting from default (half length of 255)
        for wheel in range(len(wheelsFinal)):
            if wheelsFinal[wheel] < 128:
                wheels[wheel] -= 1    
            elif wheelsFinal[wheel] > 128:
                wheels[wheel] += 1
        host.sendto(str.encode("DriveCommand_" + str(lw1) + "_" + str(rw1) + "_" + str(lw2) + "_" + str(rw2) + "_" + str(lw3) + "_" + str(rw3)), addr)

#Keyboard Inputs
#Initializing controller
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

#Drive Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            if event.axis < 2:
                #Get controllers set up
                leftMotion = joysticks[0].get_axis(leftStick)
                rightMotion = joysticks[0].get_axis(rightStick)

                #Dead Zone
                if abs(event.value) < threshhold:
                    drive()                    

                #Check which stick on the controller moves
                #Simultaneous Motion
                elif abs(leftMotion) > threshhold and abs(rightMotion) > threshhold:
                    # Format like this??: drive(lw1 = lw2 = lw3 = 255 * leftMotion.value, rw1 = rw2 = rw3 = 255 *rightMotion.value)
                    drive(255 * leftMotion.value, 255 * leftMotion.value, 255 * leftMotion.value, 255 * rightMotion.value, 255 *rightMotion.value, 255 * rightMotion.value ) # Set event value of each axis to multiply direction
                #Turn left
                elif abs(leftMotion) > threshhold:
                    drive(lw1 = 255 * leftMotion.value, lw2 = 255 * leftMotion.value, lw3 = 255 * leftMotion.value, rw1 = 0, rw2 = 0, rw3 = 0) 
                #Turn right
                elif abs(rightMotion) > threshhold:
                    drive(rw1 = 255 * rightMotion.value, rw2 = 255 * rightMotion.value, rw3 = 255 * rightMotion.value, lw1 = 0, lw2 = 0, lw3 = 0) 
               
        



