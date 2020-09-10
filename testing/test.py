import pygame
import sys
pygame.init()
if pygame.__version__[0] != "2":
    print("Please upgrade to Pygame v2.0.0 or greater (it may still be in beta, that is ok though)")
    print("https://pypi.org/project/pygame/#history")
    sys.exit()
tilecorr = {
    "z": "tlcorner",
    "v": "tedge",
    "m": "trcorner",
    "q": "blcorner",
    "t": "bedge",
    "p": "brcorner",
    "a": "ledge",
    "g": "centre",
    "l": "redge",
    "1": "decal1",
    "2": "decal2",
    "3": "decal3",
    "4": "decal4",
    "5": "decal5",
    "h": "bubble"}

class tile():
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.imgpath = "sprites/test/centre.png"
    def drawStart(self):
        self.img = pygame.transform.scale(pygame.image.load(self.imgpath),(32,32))
    def draw(self, screen):
        screen.blit(self.img,[self.xpos*32,self.ypos*32])
    def checkoverlap(self, playerxtop, playerytop, playerxbot, playerybot):
        if pygame.Rect(self.xpos*32,self.ypos*32,32,32).clipline(playerxtop, playerytop, playerxbot, playerybot) != ():
            return True
        else:
            return False

class player():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.img = "sprites/player.png"
        self.imgr = pygame.transform.scale(pygame.image.load(self.img),(32,32))
        self.imgl = pygame.transform.flip(self.imgr, True, False)
        self.facing = False
    def draw(self, screen):
        if self.facing:
            screen.blit(self.imgl,[self.x,self.y])
        else:
            screen.blit(self.imgr,[self.x,self.y])
    def move(self, left=False):
        """change left=False to left=True to move left instead of right"""
        if left:
            self.x -= 2
        else:
            self.x += 2

##### Colours #####
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREY  = ( 77,  77,  77)

##### Screen Initialisation #####
SCREEN_WIDTH = 768
SCREEN_HEIGHT = 448
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sol 0 testing")
#bgd = pygame.image.load("sprites/bgd/test.png")
#bgd = pygame.transform.scale(bgd,(int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2)))
tiles=[]
file = open("levels/test.txt","r")
cy = 0
playerx = 0
playery = 0
for line in file:
    line = line.replace("\n","")
    cx = 0
    for character in line:
        if character != " " and character != "0":
            newt = tile()
            newt.xpos = cx
            newt.ypos = cy
            newt.imgpath = "sprites/test/"+tilecorr[character]+".png"
            newt.drawStart()
            tiles.append(newt)
        elif character == "0":
            playerx = cx*32
            playery = cy*32
        cx += 1
    cy += 1
playr = player()
playr.x = playerx
playr.y = playery
done = False
clock = pygame.time.Clock()
goingl = False
goingr = False
##### Main Program Loop #####
while not done:
    ##### Events Loop #####
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playr.facing = True
                goingl = True
            elif event.key == pygame.K_RIGHT:
                playr.facing = False
                goingr = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                goingl = False
            elif event.key == pygame.K_RIGHT:
                goingr = False

    ##### Game logic #####
    lok = False
    rok = False
    for i in tiles:
        a = i.checkoverlap(playr.x,playr.y,playr.x,playr.y+31)
        b = i.checkoverlap(playr.x+32,playr.y,playr.x+32,playr.y+31)
        if a:
            lok = True
        if b:
            rok = True
    if goingl and not lok:
        playr.move(True)
    if goingr and not rok:
        playr.move(False)
    ##### Drawing code #####
    screen.fill(GREY)
#    screen.blit(bgd,(0,0))
#    screen.blit(bgd,(int(SCREEN_WIDTH/2),0))
#    screen.blit(bgd,(int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2)))
#    screen.blit(bgd,(0,int(SCREEN_HEIGHT/2)))
    for i in tiles:
        i.draw(screen)
    playr.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
