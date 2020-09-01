import pygame
pygame.init()

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
    "0": "centre",
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

tiles=[]
file = open("levels/test.txt","r")
cy = 0
for line in file:
    line = line.replace("\n","")
    cx = 0
    for character in line:
        if character != " ":
            newt = tile()
            newt.xpos = cx
            newt.ypos = cy
            newt.imgpath = "sprites/test/"+tilecorr[character]+".png"
            newt.drawStart()
            tiles.append(newt)
        cx += 1
    cy += 1
done = False
clock = pygame.time.Clock()

##### Main Program Loop #####
while not done:
    ##### Events Loop #####
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    ##### Game logic #####
    
    ##### Drawing code #####
    screen.fill(GREY)
    for i in tiles:
        i.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
