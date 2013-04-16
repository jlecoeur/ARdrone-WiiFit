import libardrone
import wiiboard
import pygame
import time

def main(): 
    # init pygame
    pygame.init()     
    clock = pygame.time.Clock()

    # init wii balance board
    print ("Connecting to wii board...")
    board = wiiboard.Wiiboard()
    fichier = open('board_address.txt', 'r')
    address = fichier.readline()
    fichier.close()    
    if not address:
        address = '' 
        address = board.discover()    
        fichier = open('board_address.txt', 'w')
        fichier.write(address)
        fichier.close()
    print address    
    board.connect(address)
    time.sleep(0.1)
    board.setLight(True)

    # init ardrone
    W, H = 320, 240
    screen = pygame.display.set_mode((W, H))
    drone = libardrone.ARDrone()
    
    running = True
    flying = False

    while (running):
        if pygame.event.peek([pygame.QUIT,
                              wiiboard.WIIBOARD_BUTTON_RELEASE]):
            running = False
            flying = False
            drone.land()
            pygame.event.clear()                            # test
        elif pygame.event.peek(pygame.KEYUP):
            drone.hover()
            pygame.event.clear()                            # test
        elif pygame.event.peek(pygame.KEYDOWN):
            for event in pygame.event.get(pygame.KEYDOWN):
                if event.key == pygame.K_RETURN:
                    drone.takeoff()
                    flying = True
                elif event.key == pygame.K_SPACE:
                    drone.land()
                    flying = False
                elif event.key == pygame.K_BACKSPACE:
                    drone.reset()
                    flying = False
                elif event.key == pygame.K_ESCAPE:
                    drone.land()
                    running = False
                    flying = False
            pygame.event.clear()                            # test            
        elif pygame.event.peek(wiiboard.WIIBOARD_MASS):
            events = pygame.event.get(wiiboard.WIIBOARD_MASS)
            event = events[0]
            if(event.mass.totalWeight > 20):
                if not flying:
                    flying = True
                    time_take_off = time.time()
                    drone.takeoff()
#                print '_____'
                TL, TR, BL, BR = event.mass.topLeft, event.mass.topRight, event.mass.bottomLeft, event.mass.bottomRight
                TM = event.mass.totalWeight
                pitch = ((BL + BR) - (TL + TR)) / TM
                roll = ((TR + BR) - (TL + BL)) / TM
                yaw = 2 * ((TL - BL) - (TR - BR)) / TM 
                #print pitch, roll, yaw
                drone.move_and_turn(roll, pitch, 2 * yaw)
            else:
                if flying:
                    drone.land()
                    print '_____'                                    
                    print 'Flight time : ', time.time()-time_take_off, 's'
                    flying = False
        pygame.event.clear()
        clock.tick(50)

    board.disconnect()
    print "Shutting down...",
    drone.halt()
    pygame.quit()
    print "Ok."

#Run the script if executed
if __name__ == "__main__":
    main()
