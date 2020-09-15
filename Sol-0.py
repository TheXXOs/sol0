import pygame
import sys
from files import level
pygame.init()

#level.runLevel(screen, worldn, leveln, timeswon=0)

if pygame.__version__[0] != "2":
    print("Please upgrade to Pygame v2.0.0 or greater (it may still be in beta, that is ok though)")
    print("https://pypi.org/project/pygame/#history")
    sys.exit()

class TheTitle():
    def __init__(self):
        self.x = 351
        self.y = 1
        self.img = pygame.transform.scale(pygame.image.load("files/sprites/menus/title.png"),(416,136))
    def draw(self, screen):
        screen.blit(self.img,(self.x,self.y))

class Boop():
    def __init__(self):
        self.img = None
        self.x = 0
        self.y = 0
        self.w = 1
        self.h = 1
        self.showon = 0
    def changeimg(self, state=1):
        if self.img:
            self.ima = pygame.transform.scale(pygame.image.load("files/sprites/menus/"+self.img+"_"+str(state)+".png"),(self.w,self.h))
    def draw(self, screen):
        screen.blit(self.ima,(self.x,self.y))
    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0] in range(self.x, self.x+self.w) and pygame.mouse.get_pos()[1] in range(self.y, self.y+self.h)
##### Colours #####
BLACK = (  0,   0,  10)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREY  = ( 80,  80,  90)

##### Screen Initialisation #####
SCREEN_WIDTH = 768
SCREEN_HEIGHT = 448
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sol 0")
font = pygame.font.SysFont("OCR A Extended",25,False,False)
texta = font.render("Coding, some tiles, most",True,WHITE)
textb = font.render("backgrounds - Nick L (TheXXOs)",True,WHITE)
textc = font.render("Music and menu background - Jack R",True,WHITE)
textd = font.render("Player sprites and most tiles - Sam L",True,WHITE)
btns = []
btnl = [["credits",1,302,232,72,0],["settings",1,375,264,72,0],["start",1,229,184,72,0],
        ["1",0,0,192,128,1],["2",192,0,192,128,1],["3",384,0,192,128,1],
        ["4",576,0,192,128,1],["5",0,128,192,128,1],["6",192,128,192,128,1],
        ["7",384,128,192,128,1],["8",576,128,192,128,1], ["wback",292,276,184,72,1],
        ["lback",292,276,184,72,2],
        ["b1",0,0,192,192,2],["b2",192,0,192,192,2],["b3",384,0,192,192,2],
        ["b4",576,0,192,192,2],["cback",1,1,28*2,36*2,3]]
levels = {
    "1": [[0,True],[0,True],[0,True],[0,True]], # unlocking mechanism;
    "2": [[0,True],[0,True],[0,True],[0,True]],# the number is the times a level has been completed,
    "3": [[0,True],[0,True],[0,True],[0,True]],# the boolean is if it has been unlocked or not
    "4": [[0,True],[0,True],[0,True],[0,True]],
    "5": [[0,True],[0,True],[0,True],[0,True]],
    "6": [[0,True],[0,True],[0,True],[0,True]],
    "7": [[0,True],[0,True],[0,True],[0,True]],
    "8": [[0,True],[0,True],[0,True],[0,True]]}
bgd = pygame.image.load("files/sprites/bgd/menu.jpg")
bgd = pygame.transform.scale(bgd,(int(SCREEN_WIDTH),int(SCREEN_HEIGHT)))
# variable 6: 0 - main, 1 - worlds, 2 - levels, 3 - credits, 4 - playing level
slide = 0
for j in btnl:
    x = Boop()
    x.img = j[0]
    x.x = j[1]
    x.y = j[2]
    x.w = j[3]
    x.h = j[4]
    x.showon = j[5]
    x.changeimg()
    btns.append(x)
done = False
clock = pygame.time.Clock()
scrstat = 0
pygame.mixer.music.load("files/music/menu1.mp3")
mtime = 0.0
mtime += (pygame.mixer.music.get_pos()/1000)%10.707984
mtime = mtime%10.707984
pygame.mixer.music.play(-1,mtime)
waitup = ""
logo = TheTitle()
planetnum = ""
oldwaitup = ""
##### Main Program Loop #####
while not done:
    ##### Events Loop #####
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if pygame.mixer.music.get_busy():
                mtime += (pygame.mixer.music.get_pos()/1000)%10.707984
                mtime = mtime%10.707984
                pygame.mixer.music.stop()
            else:
                mtime = 0.0
            if waitup != oldwaitup:
                if waitup == "credits" or waitup == "start" or waitup == "lback": #or waitup == "settings"
                    pygame.mixer.music.load("files/music/menu2.mp3")
                elif waitup == "wback":
                    pygame.mixer.music.load("files/music/menu1.mp3")
                if waitup == "start":
                    slide = 1
                elif waitup == "credits":
                    slide = 3
                elif waitup == "wback":
                    slide = 0
                elif waitup == "lback":
                    slide = 1
                elif waitup == "cback":
                    slide = 0
                    pygame.mixer.music.load("files/music/menu1.mp3")
                elif waitup in ["1","2","3","4","5","6","7","8"]:
                    slide = 2
                    planetnum = waitup
                    pygame.mixer.music.load("files/music/menu3.mp3")
                elif waitup in ["b1","b2","b3","b4"]:
                    if levels[planetnum][int(waitup[1])-1][1]: # if the level is unlocked
                        slide = 4
                        a = level.runLevel(screen,planetnum,waitup[1],levels[planetnum][int(waitup[1])-1][0]) #this is the game, look at /files/level.py
                        if a: # if you beat the level
                            levels[planetnum][int(waitup[1])-1][0] += 1
                            if waitup == "b4" and planetnum != "8": # unlock the next one
                                levels[str(int(planetnum)+1)][0][1] = True # unlock the next one
                            elif waitup != "b4": # unlock the next one
                                levels[planetnum][int(waitup[1])][1] = True # unlock the next one
                            else: # if it's the last level,
                                print("You win") # you win (do something here)
                        oldwaitup = "aaaa"
                        slide = 2
                        pygame.mixer.music.load("files/music/menu3.mp3")
                            
                    pygame.mixer.music.load("files/music/menu3.mp3")
                oldwaitup = waitup
            pygame.mixer.music.play(-1,mtime)

    ##### Game logic #####
    for i in btns:
        if i.is_clicked() and slide == i.showon:
            i.changeimg(0)
            waitup = i.img
        elif slide == i.showon:
            i.changeimg()
    ##### Drawing code #####
    screen.fill(GREY)
    if slide != 4:
        screen.blit(bgd,(0,0))
    for i in btns:
        if slide == i.showon:
            i.draw(screen)
    if slide == 0:
        logo.draw(screen)
    if slide == 3:
        screen.blit(texta, [400,0])
        screen.blit(textb, [318,30])
        screen.blit(textd, [3,420])
        screen.blit(textc, [3,390])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
