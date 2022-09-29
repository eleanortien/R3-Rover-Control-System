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
        rightTrigger = 4
        leftTrigger = 5
        threshhold = 0.1
        crossButton = 1
        triButton = 2
        sqrButton = 3
        circButton = 4

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

        
        screwMove = 128
        hoistMove = 150
        swivelMove = 128
        clawMove = 128
        upExtMove = 128
        lowExtMove = 128
        leftSideSpeed = 128
        rightSideSpeed = 128

        drivePacket = data()
        armPacket = data()
        
        armPacket.pastmsg = ""
        drivePacket.pastmsg = ""

        #HOPEFULLY allows Python to communicate with Arduino via sockets
        host = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #host.bind(compIp, serverPort) #Talk to Arduino
        #Check bind function

    

        def drive(lw1 = 128, rw1 = 128, lw2 = 128, rw2 = 128, lw3 = 128, rw3 = 128):    
            wheels = [lw1, lw2, lw3, rw1, rw2, rw3]
         
            for wheel in range(len(wheels)):
                    #Check within boundaries
                if wheels[wheel] > 255:
                    wheels[wheel] = 255
                elif wheels[wheel] < 0:
                    wheels[wheel] = 0
                
            drivePacket.msg= "DriveCommand_" + str(lw1) + "_" + str(rw1) + "_" + str(lw2) + "_" + str(rw2) + "_" + str(lw3) + "_" + str(rw3)

            if drivePacket.pastmsg != drivePacket.msg:
                print(drivePacket.msg)
                host.sendto(drivePacket.msg.encode(), compIp, serverPort)
        
        def arm(upExt = 128, lowExt = 128, hoist = 150, screw = 128, claw = 128, swivel = 128):
            
            #Unlike other comps, hoist can not go to 128
            if hoist < 150:
                hoist = 150

            armComps = [upExt, lowExt, hoist, screw, claw, swivel]
            for comp in range(len(armComps)):
                if armComps[comp] > 255:
                    armComps[comp] = 255
                elif armComps[comp] < 0:
                    armComps[comp] = 0
    
            armPacket.msg = "ArmCommand_" + upExt + "_" + lowExt + "_" + screw + "_" + claw + "_" + hoist + "_" + swivel

            if armPacket.pastmsg != armPacket.msg: 
                print(armPacket.msg)
                host.sendto(drivePacket.msg.encode(), compIp, serverPort)
                


        #Keyboard Inputs
        #Initializing controller(s): 1 for arm, 1 for driving
        pygame.init()
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        if pygame.joystick.get_count() != 0:
            driveJoystick = joysticks[0]
            if pygame.joystick.get_count() == 2:
                armJoystick = joysticks[1]



        while True:
            for event in pygame.event.get():

                #Reinitializing Joysticks
                if event.type == pygame.JOYDEVICEADDED or event.type == pygame.JOYDEVICEREMOVED:
                    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
                    if pygame.joystick.get_count() != 0:
                        driveJoystick = joysticks[0]
                        if pygame.joystick.get_count() == 2:
                            armJoystick = joysticks[1]

             

                #Drive controls
                if event.joy == driveJoystick:
                    if event.type == pygame.JOYAXISMOTION:
                        if event.axis < 2:
                            #Get controllers' input
                            leftMotion = driveJoystick.get_axis(leftStick)
                            rightMotion = driveJoystick.get_axis(rightStick)
                            rTriggerMotion = driveJoystick.get_axis(rightTrigger)
                            lTriggerMotion = driveJoystick.get_axis(leftTrigger)

                            #Dead Zone
                            if abs(event.value) < threshhold:
                                drive()            
                                continue       

                            #Check which stick on the controller moves
                            #Simultaneous Motion
                            elif abs(leftMotion) > threshhold and abs(rightMotion) > threshhold:
                                leftSideSpeed = leftMotion * 170
                                rightSideSpeed = rightMotion * 170
                                #drive(170 * leftMotion, 170 * leftMotion, 170 * leftMotion, 170 * rightMotion, 170 * rightMotion, 170 * rightMotion) # Set event value of each axis to multiply direction
                            #Turn left
                            elif abs(leftMotion) > threshhold:
                                leftSideSpeed = leftMotion * 170
                                rightSideSpeed = rightMotion * 70
                                #drive(lw1 = 170 * leftMotion, lw2 = 170 * leftMotion, lw3 = 170 * leftMotion, rw1 = 70, rw2 = 70, rw3 = 70) 
                            #Turn right
                            elif abs(rightMotion) > threshhold:
                                leftSideSpeed = leftMotion * 70
                                rightSideSpeed = rightMotion * 170
                                #drive(rw1 = 170 * rightMotion, rw2 = 170 * rightMotion, rw3 = 170 * rightMotion, lw1 = 70, lw2 = 70, lw3 = 70) 
                            
                            
                            #Speed Increase
                            if abs(rTriggerMotion) > threshhold:
                                leftSideSpeed += 70
                                rightSideSpeed += 70
                            
                            #Speed Decrease
                            elif abs(lTriggerMotion) > threshhold:
                                leftSideSpeed -= 70
                                rightSideSpeed -=70
                            
                            drive(leftSideSpeed, leftSideSpeed, leftSideSpeed, rightSideSpeed, rightSideSpeed, rightSideSpeed)
                                
                
                #Arm Control
                #Hoist, joystick
                #Upper and lower, buttons?
                #Claw, trigger
                #Swivel, other joystick??????
                if event.joy == armJoystick:
                    if event.type == pygame.JOYAXISMOTION:
                        if event.axis < 2:
                            #Joystick Motion Controls
                            hoistMotion = armJoystick.get_axis(leftStick)
                            swivelMotion = armJoystick.get_axis(rightStick)
                            clawCloseMotion = armJoystick.get_axis(leftTrigger)
                            clawOpenMotion = armJoystick.get_axis(rightTrigger)
                            upExtMove = 128
                            lowExtMove = 128
                            screwMove = 128


                            if abs(event.value) < threshhold:
                                arm()            
                                continue       

                            #Check which stick on the controller moves
                            #Simultaneous Motion
                            elif abs(hoistMotion) > threshhold and abs(swivelMotion) > threshhold:
                                hoistMove = hoistMotion * 170
                                swivelMove = swivelMotion * 170

                            elif abs(hoistMotion) > threshhold:
                                hoistMove = hoistMotion * 170
                                swivelMove = swivelMotion * 70
                                #drive(lw1 = 170 * leftMotion, lw2 = 170 * leftMotion, lw3 = 170 * leftMotion, rw1 = 70, rw2 = 70, rw3 = 70) 
                            #Turn right
                            elif abs(swivelMotion) > threshhold:
                                hoistMove = leftMotion * 70
                                swivelMove = rightMotion * 170
                                drive(rw1 = 170 * rightMotion, rw2 = 170 * rightMotion, rw3 = 170 * rightMotion, lw1 = 70, lw2 = 70, lw3 = 70) 
                            
                            
                            #Claw Open
                            if abs(clawOpenMotion) > threshhold:
                                clawMove = clawOpenMotion * 170
                            
                            #Claw Close
                            elif abs(clawCloseMotion) > threshhold:
                                clawMove = clawOpenMotion * 70
                            
                            arm(hoist = hoistMove, claw = clawMove, swivel = swivelMove )
                    
                    if event.type == pygame.JOYBUTTONDOWN:
                        if armJoystick.get_button(crossButton):
                            upExtMove += 70
                        elif armJoystick.get_button(triButton):
                            upExtMove -= 70
                        if armJoystick.get_button(sqrButton):
                            lowExtMove += 70
                        elif armJoystick.get_button(circButton):
                            lowExtMove -= 70
                    
                    if event.type == pygame.JOYHATMOTION:
                        screwX, screwY = event.value
                        if screwX == -1:
                            screwMove -= 20
                        elif screwX == 1:
                            screwMove += 20
                        

                        


            
                    
                
if __name__ == "__main__":
    program = main()
    program.run()


