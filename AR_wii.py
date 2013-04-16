import libardrone
import wiiboard
import pygame
import time

def main(): 
    # init wii balance board
    print ("Connecting to wii board...")
    board = wiiboard.Wiiboard()
    #try:
    address = board.discover()    
    board.connect(address)
    time.sleep(0.1)
    board.setLight(True)
    print('OK, Wii board connected')
    #except:
    print('Error : No WiiBoard detected')

    # init ardrone
    #W, H = 320, 240
    #screen = pygame.display.set_mode((W, H))
    drone = libardrone.ARDrone()
    
    # init pygame
    pygame.init()     
    clock = pygame.time.Clock()
    running = True
    flying = False
    
    while (running):
        if pygame.event.peek([pygame.QUIT,
                              wiiboard.WIIBOARD_BUTTON_RELEASE]):
            running = False
            flying = False
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
                    drone.reset()
                    running = False
                    flying = False
                elif event.key == pygame.K_w:
                    drone.move_forward()
                elif event.key == pygame.K_s:
                    drone.move_backward()
                elif event.key == pygame.K_a:
                    drone.move_left()
                elif event.key == pygame.K_d:
                    drone.move_right()
                elif event.key == pygame.K_UP:
                    drone.move_up()
                elif event.key == pygame.K_DOWN:
                    drone.move_down()
                elif event.key == pygame.K_LEFT:
                    drone.turn_left()
                elif event.key == pygame.K_RIGHT:
                    drone.turn_right()
                elif event.key == pygame.K_1:
                    drone.speed = 0.1
                elif event.key == pygame.K_2:
                    drone.speed = 0.2
                elif event.key == pygame.K_3:
                    drone.speed = 0.3
                elif event.key == pygame.K_4:
                    drone.speed = 0.4
                elif event.key == pygame.K_5:
                    drone.speed = 0.5
                elif event.key == pygame.K_6:
                    drone.speed = 0.6
                elif event.key == pygame.K_7:
                    drone.speed = 0.7
                elif event.key == pygame.K_8:
                    drone.speed = 0.8
                elif event.key == pygame.K_9:
                    drone.speed = 0.9
                elif event.key == pygame.K_0:
                    drone.speed = 1.0
            pygame.event.clear()                            # test            
        elif pygame.event.peek(wiiboard.WIIBOARD_MASS):
            events = pygame.event.get(wiiboard.WIIBOARD_MASS)
            event = events[0]
            if(event.mass.totalWeight > 20):
                #if not flying:
                flying = True
                drone.takeoff()
                print '_____'
                TL, TR, BL, BR = event.mass.topLeft, event.mass.topRight, event.mass.bottomLeft, event.mass.bottomRight
                TM = event.mass.totalWeight
                pitch = ((BL + BR) - (TL + TR)) / TM
                roll = ((TR + BR) - (TL + BL)) / TM
                yaw = 2 * ((TL - BL) - (TR - BR)) / TM 
                print pitch, roll, yaw
                drone.move_and_turn(roll, pitch, yaw)
            else:
                if flying:
                    drone.land()
                    flying = False
        pygame.event.clear()
#        try:
#            surface = pygame.image.fromstring(drone.image, (W, H), 'RGB')
#            hud_color = (255, 0, 0) if drone.navdata.get('drone_state', dict()).get('emergency_mask', 1) else (10, 10, 255)
#            bat = drone.navdata.get(0, dict()).get('battery', 0)
#            f = pygame.font.Font(None, 20)
#            hud = f.render('Battery: %i%%' % bat, True, hud_color)
#            screen.blit(surface, (0, 0))
#            screen.blit(hud, (10, 10))
#        except:
#            pass
#        pygame.display.flip()
        clock.tick(50)
#        pygame.display.set_caption("FPS: %.2f" % clock.get_fps())

    board.disconnect()
    print "Shutting down...",
    drone.halt()
    pygame.quit()
    print "Ok."

#Run the script if executed
if __name__ == "__main__":
    main()
