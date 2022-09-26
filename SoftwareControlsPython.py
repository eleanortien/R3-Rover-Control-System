class data:
    def __init__(self):
        self.msg = str
        self.pastmsg = str 

class main:
    def run():
        import socket
        import pygame

        #Variable Setup
        ardPort = "com3" #Write com connected to Arduino here
        #board = Arduino(ardPort)
        delay = 0.015
        serverPort = 8090
        compIp = '192.168.1.11' #Make ip 192... (in document)
        echoNum = 1024

        #Controller Values
        leftStick = 1
        rightStick = 3 #or 1 and 3
        threshhold = 0.1
        #Pin unneeded in Python 
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

        packet = data()

        packet.pastmsg = ""
        #HOPEFULLY allows Python to communicate with Arduino via sockets
        host = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #host.bind(compIp, serverPort) #Talk to Arduino
        #Check bind function

    

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
            
                packet.msg= "DriveCommand_" + str(lw1) + "_" + str(rw1) + "_" + str(lw2) + "_" + str(rw2) + "_" + str(lw3) + "_" + str(rw3)

                if packet.pastmsg != packet.msg:
                    print(packet.msg)
                host.sendto(packet.msg.encode(), compIp, serverPort)


        #Keyboard Inputs
        #Initializing controller
        pygame.init()
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
                            drive(170 * leftMotion, 170 * leftMotion, 170 * leftMotion, 170 * rightMotion, 170 * rightMotion, 170 * rightMotion) # Set event value of each axis to multiply direction
                        #Turn left
                        elif abs(leftMotion) > threshhold:
                            drive(lw1 = 170 * leftMotion, lw2 = 170 * leftMotion, lw3 = 255 * leftMotion, rw1 = 70, rw2 = 70, rw3 = 70) 
                        #Turn right
                        elif abs(rightMotion) > threshhold:
                            drive(rw1 = 170 * rightMotion, rw2 = 170 * rightMotion, rw3 = 170 * rightMotion, lw1 = 70, lw2 = 70, lw3 = 70) 
                    
                
if __name__ == "__main__":
    program = main()
    program.run()


