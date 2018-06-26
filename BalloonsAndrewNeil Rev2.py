### Balloon Game
### The object of this program is to shoot down balloons.
### Written by: Andrew Neil

#Import libraries
import pygame, sys, random

#Initialize the Pygame module
pygame.init()

#Setup the game window
width = 640
height = 480
size = [width, height]
screen = pygame.display.set_mode(size)                  #size of window
pygame.display.set_caption("Balloons by Andrew Neil")   #banner name
pygame.mouse.set_visible(False)                         #don't show mouse cursor

#Define RGB color code
red    = [255,0,0]
green  = [255,140,0]
blue   = [0,0,255]
purple = [255,0,255]
yellow = [255,255, 0]
black  = [0,0,0]
white  = [255,255,255]

#Define sounds
whoosh_sound  = pygame.mixer.Sound("WHOOSH.wav")
pop_sound     = pygame.mixer.Sound("POP.wav")
waiting_sound = pygame.mixer.Sound("house_lo.wav")
#crowd_sound   = pygame.mixer.Sound("Crowd.wav")

#Define background pictures
first_screen = pygame.image.load("bg_balloon.png").convert()
bg1          = pygame.image.load("grass and sky.png").convert()     #background level 1
bg2          = pygame.image.load("grassandsky2.jpg").convert()      #background level 2
bg3          = pygame.image.load("mountains.jpg").convert()         #background level 3
bg4          = pygame.image.load("bg_wyoming2.jpg").convert()       #background level 4
bg5          = pygame.image.load("bg_colorado.jpg").convert()       #background level 5
backgrounds  = [bg1, bg2, bg3, bg4, bg5]                            #list of backgrounds
for i in range(5):
    backgrounds[i] = pygame.transform.scale(backgrounds[i], size)   #scale to fit the window

#Define crossbow picture
crossbow_pic = pygame.image.load("crossbow.png").convert()          #picture of crossbow
scale        = 255, 85                                              #set size of crossbow
crossbow_pic = pygame.transform.scale(crossbow_pic, scale)          #scale crossbow
crossbow_pic.set_colorkey(white)

#Define aim picture
aim_pic = pygame.image.load("aim.png").convert()
aim_pic.set_colorkey(white)

#Define balloon for each level
red_balloon = pygame.image.load("RedBalloon.png").convert()
red_balloon.set_colorkey(black)

#Define Level Up graphics
levelUp_screen   = pygame.image.load("NextLevelScreen.png").convert()
bang             = pygame.image.load("boom.png")
game_over_screen = pygame.image.load("GameOver.png")

#Clock
clock        = pygame.time.Clock()
screenCenter = screen.get_rect().center

#Initialize the settings and score
hit          = False        #shot miss
hitCount     = 0            #number of hits is zero
start        = True         #game starts
over         = False        #game is not over
score        = 0            #no score
lvl          = 1            #start game at level
waves        = 1            #start each level with wave 1
bLvl         = 0            #first background image in the array
misses       = 5            #allow to up 5 misses
over         = False        #game is not over
update_score = True         #Update score
dim          = 64, 64       #dimension of hit target (x,y)
balloon_out  = 1            #start with 1 balloon in the beginning of the game
balloon_left = balloon_out  #balloon_left is the same as balloon in the beginning of the game
balloon_spot = []           #define array for balloon spot
offset =[]                  #define offset

#randomly select balloon start positions, stay from the edge of the window
for i in range(10):
    ranpos = [random.randint(60,width-60), random.randint(60,height-60)]    #randomly start to launch the balloon
    balloon_spot.append(ranpos)
#randomly select balloon speed between 1 and 4
for i in range(10):
    offset.append([random.randint(1,4),random.randint(1,4)])                #randomly offset the balloon

#Get mid points of the window
midx = screen.get_rect().centerx    #mid point of width
midy = screen.get_rect().centery    #mid point of height

done = False
#Continue until the user choose to QUIT
while not done:
    clock.tick(50)

    ### Start event ###
    for event in pygame.event.get():
        if event.type == pygame.QUIT:      #press "ESC" key to quit
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not start:
                for i in range(balloon_left):
                    x = balloon_spot[i][0]
                    y = balloon_spot[i][1]
                    #It is a hit if the balloon is within the dimension of the aim position
                    if (aim_pos[0] >= x and aim_pos[0] <= x + dim[0]) and (aim_pos[1] >= y and aim_pos[1] <= y + dim[1]):
                        hit_spot = balloon_spot[i]
                        balloon_spot.remove(balloon_spot[i])  #remove balloon when hit
                        balloon_left  -= 1      #decrease number of balloon
                        hitCount      += 1      #increase number of hit
                        hit = True              #set hit flag to true
                if not hit:
                    misses -= 1                 #decrease the misses count
                    whoosh_sound.play()         #plays "whoosh" sound when miss
                #randomize direction
                for i in range(balloon_left):
                    offset.insert(i, [random.randint(lvl,lvl+2),random.randint(lvl,lvl+2)])
        if event.type == pygame.KEYUP:          #active on key up
            if event.key == ord(' '):           #Spacebar to start the game
                if start:
                    start = False
            elif event.key == ord('f'):         #Select "f" to switch to full screen
                screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
            elif event.key == ord('w'):         #Select "w" to switch to windowed screen
                screen = screen = pygame.display.set_mode(size)
            elif event.key == pygame.K_ESCAPE:  #"Esc" key to exit the game
                done = True
            elif event.key == ord('r'):         #Select "r" tp restart the game
                if over:                        #reset when the game is over, not during the game
                    over = False
                    misses = 5
                    lvl = 1
                    balloon_left = 1
                    waves = 1
                    balloon_out  = 0
                    score = 0
                    start = True
                    hitCount = 0
                    update_score = True
    ### end of event ###

    ### First and LEVEL UP screens ###
    if start:
        #define text, size, and color
        font1 = pygame.font.SysFont(None, 50)
        font2 = pygame.font.SysFont(None, 30)
        font3 = pygame.font.SysFont(None, 30)

        text1 = font1.render('LEVEL ' + str(lvl), True, green)
        text2 = font2.render('[press space to continue]', True, green)
        text3 = font3.render('1 EXTRA SHOT AWARDED', True, yellow)

        #define text positions
        textRect1 = text1.get_rect()
        textRect1.centerx = midx
        textRect1.centery = midy
        textRect2 = text2.get_rect()
        textRect2.centerx = midx
        textRect2.centery = midy + 30           #offset from midy (middle of the screen)
        textRect3 = text3.get_rect()
        textRect3.centerx = midx
        textRect3.centery = height - 50         #offset from the bottom screen

        #create First and LEVEL screens
        screen.fill(black)
        if lvl == 1:
            screen.blit(first_screen,[0,0])     #setup FIRST screen
        if lvl > 1:
            screen.blit(levelUp_screen,[0,0])   #setup LEVEL screen
            screen.blit(text3, textRect3)
        screen.blit(text1, textRect1)
        screen.blit(text2, textRect2)
    ### end of LEVEL UP screen ###

    ### PLAY ACTION screens ###
    elif not over and not start:
        #checks if there are no balloons left
        if balloon_left == 0:
            if waves < 3:
                balloon_out = waves * lvl * 3   #number of balloons based on level and wave
                balloon_left = balloon_out
                waves+= 1                       #increment to the next wave
            else:                               #go to next level
                lvl         += 1                #increase level
                misses      += 1
                balloon_out  = lvl              #start with a number of balloons depending on each level
                balloon_left = balloon_out
                waves        = 1
                start        = True
                update_score = True
                if bLvl < 4:
                    bLvl += 1
                else:
                    bLvl = 0
            if lvl == 1:
                bLvl = 0
            elif lvl == 2:
                bLvl == 1
            elif lvl == 3:
                bLvl = 2
            elif lvl == 4:
                bLvl = 3
            elif lvl == 5:
                bLvl = 4
            for i in range(balloon_left):
                balloon_spot.append([random.randint(0,width-60), random.randint(0,height-60)])
                offset[i] = [random.randint(lvl, lvl+2), random.randint(lvl, lvl+2)]
        screen.fill(black)
        screen.blit(backgrounds[bLvl], [0,0])

        #Add explosion image
        if hit:
            #play a "pop" sound when there's a hit
            pop_sound.play()
            for i in range(balloon_left):
                screen.blit(red_balloon, balloon_spot[i])
                screen.blit(aim_pic, [aim_x, aim_y])
            #display an explosion image when there's hit
            for a in range(1,60,3):
                boom = pygame.transform.scale(bang,(a,a +6))
                screen.blit(boom, hit_spot)
                pygame.display.update()
            hit = False

        #display balloon left
        for i in range(balloon_left):
            screen.blit(red_balloon, balloon_spot[i])

            #checks if balloons hit the screen
            if balloon_spot[i][1] > (size[1] - dim[1]) or balloon_spot[i][1]<= 0:
                offset[i][1] = -offset[i][1]
            if balloon_spot[i][0] > size[0] - dim[0] or balloon_spot[i][0] <= 0:
                offset[i][0] = -offset[i][0]
            balloon_spot[i][1] += offset[i][1]
            balloon_spot[i][0] += offset[i][0]
        aim_pos = pygame.mouse.get_pos()    #get mouse position

        #END MAIN LOOP IF MISSED MORE THAN 3 TIMES
        if misses < 1:
            update_score = True
            over = True

        #Update current progress (wave, misses, level, balloons)
        font = pygame.font.SysFont(None, 30)
        text1 = font.render('BALLOONS: ' + str(hitCount), True, red)
        text2 = font.render('WAVE: ' + str(waves), True, green)
        text3 = font.render('MISSES LEFT: ' + str(misses), True, black)
        text4 = font.render('LEVEL: ' + str(lvl), True, yellow)
        screen.blit(text1,  [5,   5])
        screen.blit(text2,  [189, 5])
        screen.blit(text3,  [320, 5])
        screen.blit(text4,  [520, 3])

        #get cursor to center of image, dimensions are 61, 61
        aim_x = aim_pos[0] - 30
        aim_y = aim_pos[1] - 30
        if aim_x < size[0] and aim_y < size[1]:
            screen.blit(aim_pic, [aim_x, aim_y ])
            screen.blit(crossbow_pic, [aim_pos[0]-10, size[1]-scale[1]])
    ### end of not over and not start ###

    ### GAME OVER screen ###
    elif over:
        if update_score:
            score += lvl * hitCount * 10
            update_score = False
            hitCount = 0
        crowd_sound.play()

        #define text contents
        text1 = font.render('PRESS \'R\' TO RESTART ', True, white)         #/'/' = escape character
        text2 = font.render('AND \'ESC\' TO EXIT ', True, white)
        text3 = font.render('YOU SCORED ' + str(score)+ ' pts', True, yellow)

        #define text positions
        textRect1 = text1.get_rect()
        textRect1.centerx = midx
        textRect1.centery = midy - 35
        textRect2 = text2.get_rect()
        textRect2.centerx = midx
        textRect2.centery = midy
        textRect3 = text3.get_rect()
        textRect3.centerx = midx
        textRect3.centery = midy + 35

        #create "Game Over" screen
        screen.fill(black)
        screen.blit(game_over_screen, [0,0])
        screen.blit(text1, textRect1)
        screen.blit(text2, textRect2)
        screen.blit(text3, textRect3)
    ### end of GAME OVER screen ###

    #refresh the entire display
    pygame.display.flip()
#end of while loop

#exit the game
pygame.quit()
