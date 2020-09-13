import pygame
pygame.init()

class Button():
    def __init__(self):
        self.img = None
        self.x = 0
        self.y = 0
        self.w = 1
        self.h = 1
    def changeimg(self, state=1):
        if self.img:
            self.ima = pygame.transform.scale(pygame.image.load("sprites/menus/"+self.img+"_"+str(state)+".png"),(self.w,self.h))
    def draw(self, screen):
        screen.blit(self.ima,(self.x,self.y))
    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0] in range(self.x, self.x+self.w) and pygame.mouse.get_pos()[1] in range(self.y, self.y+self.h)
##### Colours #####
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

##### Screen Initialisation #####
SCREEN_WIDTH = 768
SCREEN_HEIGHT = 448
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sol 0 menu testing")
btns = []
btnl = [[["credits",268,147,232,72],["settings",252,74,264,72],["start",292,1,184,72]]]
for i in btnl:
    for j in i:
        x = Button()
        x.img = j[0]
        x.x = j[1]
        x.y = j[2]
        x.w = j[3]
        x.h = j[4]
        x.changeimg()
        btns.append(x)
done = False              
clock = pygame.time.Clock()
scrstat = 0
mtime = 0.0
waitup = ""
pygame.mixer.music.set_endevent(123456789)
##### Main Program Loop #####
while not done:
    ##### Events Loop #####
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONUP or event.type == 123456789:
            if pygame.mixer.music.get_busy():
                mtime += (pygame.mixer.music.get_pos()/1000)%10.707984
                mtime = mtime%10.707984
                pygame.mixer.music.stop()
            else:
                mtime = 0.0
            print(mtime)
            if waitup == "credits":
                pygame.mixer.music.load("music/menu3.mp3")
            elif waitup == "settings":
                pygame.mixer.music.load("music/menu2.mp3")
            elif waitup == "start":
                pygame.mixer.music.load("music/menu1.mp3")
            pygame.mixer.music.play(-1,mtime)
            

    ##### Game logic #####
    for i in btns:
        if i.is_clicked():
            i.changeimg(0)
            waitup = i.img
        else:
            i.changeimg()
    ##### Drawing code #####
    screen.fill(WHITE)
    for i in btns:
        i.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
