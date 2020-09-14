import pygame
import sys
#pygame.init()

#if pygame.__version__[0] != "2":
#    print("Please upgrade to Pygame v2.0.0 or greater (it may still be in beta, that is ok though)")
#    print("https://pypi.org/project/pygame/#history")
#    sys.exit()

class tile():
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.imgpath = "sprites/world/test/centre.png"
        self.death = False
        self.goal = False
        self.type = "" #this is here purely to prevent crashes
    def drawStart(self):
        self.img = pygame.transform.scale(pygame.image.load(self.imgpath),(32,32))
    def draw(self, screen, offset):
        screen.blit(self.img,[self.xpos-offset,self.ypos])
    def checkoverlap(self, playerxtop, playerytop, playerxbot, playerybot):
        if pygame.Rect(self.xpos,self.ypos,32,32).clipline(playerxtop, playerytop, playerxbot, playerybot) != ():
            return True
        else:
            return False
class toggleTile():
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.type = "death" #death, button, flag
        self.status = True
        self.toggled = False
        self.death = False #this is here purely to prevent crashes
        self.goal = False #this is here purely to prevent crashes
    def drawStart(self):
        self.onimg = pygame.transform.scale(pygame.image.load("sprites/world/test/blocks/"+self.type+"/on.png"),(32,32))
        self.offimg = pygame.transform.scale(pygame.image.load("sprites/world/test/blocks/"+self.type+"/off.png"),(32,32))
    def draw(self, screen, offset):
        if self.status:
            screen.blit(self.onimg,[self.xpos-offset,self.ypos])
        else:
            screen.blit(self.offimg,[self.xpos-offset,self.ypos])
    def checkoverlap(self, playerxtop, playerytop, playerxbot, playerybot):
        if pygame.Rect(self.xpos,self.ypos,32,32).clipline(playerxtop, playerytop, playerxbot, playerybot) != () and self.status:
            return True
        else:
            return False
    def toggle(self):
        if not self.toggled:
            if self.status:
                self.status = False
            else:
                self.status = True
class Button():
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.type = "" #this is here purely to prevent crashes
        self.status = True
        self.toggled = True
        self.death = False #this is here purely to prevent crashes
        self.goal = False #this is here purely to prevent crashes
    def drawStart(self):
        self.onimg = pygame.transform.scale(pygame.image.load("sprites/world/test/blocks/buttonpress/on.png"),(32,32))
        self.offimg = pygame.transform.scale(pygame.image.load("sprites/world/test/blocks/buttonpress/off.png"),(32,32))
    def draw(self, screen, offset):
        if self.status:
            screen.blit(self.onimg,[self.xpos-offset,self.ypos])
        else:
            screen.blit(self.offimg,[self.xpos-offset,self.ypos])
    def checkoverlap(self, playerxtop, playerytop, playerxbot, playerybot):
        if pygame.Rect(self.xpos,self.ypos,32,32).clipline(playerxtop, playerytop, playerxbot, playerybot) != ():
            self.toggle()
            return True
        else:
            return False
    def toggle(self):
        if self.toggled:
            pygame.mixer.music.load("sfx/button.wav")
            pygame.mixer.music.play()
            if self.status:
                self.status = False
            else:
                self.status = True
            self.toggled = False
            return True
        else:
            return False
class player():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.img = "stand"
        self.facing = False
        self.jump = 0
    def draw(self, screen, offset):
        if self.facing:
            screen.blit(pygame.transform.flip(pygame.transform.scale(pygame.image.load("sprites/player/"+self.img+".png"),(32,32)), True, False),[self.x-offset,self.y])
        else:
            screen.blit(pygame.transform.scale(pygame.image.load("sprites/player/"+self.img+".png"),(32,32)),[self.x-offset,self.y])
    def move(self, left=False):
        """change left=False to left=True to move left instead of right"""
        if left:
            self.x -= 5
        else:
            self.x += 5

def runLevel(screen,worldn,leveln, timeswon=0):
    offset = 0

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
        "6": "decal6",
        "7": "decal7",
        "8": "decal8",
        "9": "decal9",
        "h": "bubble",
        "x": "tbbeam",
        "s": "lrbeam",
        "w": "rbeam",
        "e": "tbeam",
        "d": "lbeam",
        "/": "death",
        "!": "win"}
    togglecorr = {
        "<": ["button",True],
        ",": ["button",False],
        ">": ["death",True],
        ".": ["death",False],
        ":": ["flag",True],
        ";": ["flag",False]}
    walkanim = ["stand","w1","stand","w2"]
    walkpos = 0

    ##### Colours #####
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    RED   = (255,   0,   0)
    GREY  = ( 77,  77,  77)

    ##### Screen Initialisation #####
    SCREEN_WIDTH = 768
    SCREEN_HEIGHT = 448
    #size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    #screen = pygame.display.set_mode(size)
    #pygame.display.set_caption("Sol 0 testing")
    bgd = pygame.image.load("sprites/bgd/"+worldn+".png")
    bgd = pygame.transform.scale(bgd,(int(SCREEN_WIDTH),int(SCREEN_HEIGHT)))
    tiles=[]
    file = open("levels/"+worldn+"/"+leveln+".txt","r")
    cy = 0
    playerx = 0
    playery = 0
    optionmenu = False
    optionmenua = False

    for line in file:
        line = line.replace("\n","")
        cx = 0
        for character in line:
            if character != " " and character != "0":
                if character not in togglecorr and character != "?":
                    newt = tile()
                elif character == "?":
                    newt = Button()
                else:
                    newt = toggleTile()
                newt.xpos = cx*32
                newt.ypos = cy*32
                if character not in togglecorr and character != "?":
                    newt.imgpath = "sprites/world/"+worldn+"/"+tilecorr[character]+".png"
                    if tilecorr[character] == "death":
                        newt.death = True
                    elif character == "!":
                        newt.goal = True
                elif character != "?":
                    newt.type = togglecorr[character][0]
                    newt.status = togglecorr[character][1]
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
    pwalk = 0
    done = False
    clock = pygame.time.Clock()
    goingl = False
    goingr = False
    playerdeath = False
    buttonpressed = True
    wToG = {
        "1": 11.2,
        "2": 8.9,
        "3": 10.4,
        "4": 24.8,
        "5": 3.7,
        "6": 9.8,
        "7": 8.9,
        "8": 3.7,
        "test":0.1}
    ##### Main Program Loop #####
    while not done:
        jumping = False
        ##### Events Loop #####
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playr.facing = True
                    goingl = True
                elif event.key == pygame.K_RIGHT:
                    playr.facing = False
                    goingr = True
                elif event.key == pygame.K_UP:
                    jumping = True
                elif event.key == pygame.SPACE:
                    if optionmenu:
                        optionmenu = False
                    else:
                        optionmenu = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    goingl = False
                elif event.key == pygame.K_RIGHT:
                    goingr = False

        ##### Game logic #####
        gravity = wToG[worldn] #mercury = 3.7, venus = 8.9, earth = 9.8, mars = 3.7
        #jupiter = 24.8, saturn = 10.4, uranus = 8.9, neptune = 11.2
        lok = False
        rok = False
        uok = False
        dok = False
        for i in tiles:
            if (playerdeath and i.type=="death") or (i.type=="button" and (not buttonpressed)) or (i.type=="flag" and timeswon>0):
                i.toggle()
                i.toggled = True
            elif isinstance(i,toggleTile) and i.type == "button":
                i.toggled = False
            if not isinstance(i, Button):
                a = i.checkoverlap(playr.x,playr.y,playr.x,playr.y+31)
                b = i.checkoverlap(playr.x+31,playr.y,playr.x+31,playr.y+31)
                c = i.checkoverlap(playr.x+5,playr.y+1, playr.x+26, playr.y+1)
                d = i.checkoverlap(playr.x+5,playr.y+33, playr.x+26, playr.y+33)
            else:
                a = i.checkoverlap(playr.x,playr.y,playr.x,playr.y+31)
                b = i.checkoverlap(playr.x+31,playr.y,playr.x+31,playr.y+31)
                c = i.checkoverlap(playr.x+5,playr.y+1, playr.x+26, playr.y+1)
                d = i.checkoverlap(playr.x+5,playr.y+33, playr.x+26, playr.y+33)
                buttonpressed = i.status
                print(buttonpressed)
            if playr.y < 0:
                playr.y = 1
            elif playr.y > SCREEN_HEIGHT-32:
                playr.y = SCREEN_HEIGHT-33
            if a:
                lok = True
            if b:
                rok = True
            if c:
                uok = True
                playr.y = i.ypos+32
            if d:
                dok = True
                playr.y = i.ypos-32
            if (a or b or c or d) and i.death:
                playr.y = playery
                playr.x = playerx
                playerdeath = True
                pygame.mixer.music.load("sfx/hit.wav")
                pygame.mixer.music.play()
            if (a or b or c or d) and i.goal:
                return True
            if (not (a or b or c or d)) and isinstance(i, Button):
                i.toggled = True
        if dok and (goingl or goingr):
            if pwalk > 5:
                playr.img = walkanim[walkpos%4]
                walkpos += 1
                pwalk = 0
            else:
                pwalk += 1
        else:
            playr.img = "stand"
            walkpos = 0
            pwalk = 0
        if goingl and not lok and not optionmenua:
            playr.move(True)
        if goingr and not rok and not optionmenua:
            playr.move(False)
        if optionmenu:
            optionmenua = True
        else:
            optionmenua = False
        if dok or uok:
            playr.jump = 0
        elif playr.jump - gravity/60*32 > -32:
            playr.jump -= gravity/60*32
        else:
            playr.jump = -31
        if dok and jumping:
            playr.jump += 30 # jump height of the player
            pygame.mixer.music.load("sfx/jump.wav")
            pygame.mixer.music.play()
        if not optionmenua:
            playr.y -= int(playr.jump)
        while playr.x > SCREEN_WIDTH+offset-128:
            offset += 1
        while playr.x < offset+128 and offset>=0:
            offset -= 1
        if playr.x<0:
            playr.x=0
        ##### Drawing code #####
        screen.fill(GREY)
    #    screen.blit(bgd,(0,0))
    #    screen.blit(bgd,(int(SCREEN_WIDTH/2),0))
    #    screen.blit(bgd,(int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2)))
    #    screen.blit(bgd,(0,int(SCREEN_HEIGHT/2)))
        playr.draw(screen, offset)
        for i in tiles:
            i.draw(screen, offset)
        if optionmenua:
            pygame.draw.rect(screen,BLACK,pygame.Rect(50,50,668,348))
        pygame.display.flip()
        clock.tick(60)
#pygame.mixer.init()
#runLevel()
