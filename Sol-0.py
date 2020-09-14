import pygame
from files import level
pygame.init()

#level.runLevel(screen, worldn, leveln, timeswon=0)

class TheTitle():
    def __init__(self):
        self.x = 176
        self.y = 5
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
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREY  = ( 80,  80,  90)

##### Screen Initialisation #####
SCREEN_WIDTH = 768
SCREEN_HEIGHT = 448
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sol 0")
btns = []
btnl = [["credits",268,297,232,72,0],["settings",252,224,264,72,0],["start",292,151,184,72,0],
        ["1",0,0,192,128,1],["2",192,0,192,128,1],["3",384,0,192,128,1],
        ["4",576,0,192,128,1],["5",0,128,192,128,1],["6",192,128,192,128,1],
        ["7",384,128,192,128,1],["8",576,128,192,128,1], ["wback",292,276,184,72,1]]
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
            if waitup == "credits" or waitup == "start": #or waitup == "settings"
                pygame.mixer.music.load("files/music/menu2.mp3")
            elif waitup == "wback":
                pygame.mixer.music.load("files/music/menu1.mp3")
            if waitup == "start":
                slide = 1
            elif waitup == "credits":
                slide = 3
            elif waitup == "wback":
                slide = 0
            elif waitup in ["5","7","8"]:
                slide = 4
                level.runLevel(screen,waitup,"1",0) # this is the main code, wow, go look at /files/level.py now
                pygame.mixer.music.load("files/music/menu2.mp3")
                slide = 1
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
    for i in btns:
        if slide == i.showon:
            i.draw(screen)
    if slide == 0:
        logo.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
