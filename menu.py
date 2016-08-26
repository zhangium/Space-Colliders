# menu.py

from pygame import *
from datetime import datetime
from math import *

backPic = image.load("background.jpg")
backPic = transform.scale(backPic,(2000,1000))
starsPic = image.load("starsNoBG.png")
starsPic = transform.scale(starsPic,(800,600))

class Draw:
    def __init__(self,planet,size):
        self.planet = planet
        self.size = size

    def drawBack(self):
        offx = 400-round(self.planet[0]*0.5)
        offy = 300-round(self.planet[1]*0.5)
        offx = offx%2000
        offy = offy%1000
        for dx in range(-2000,2000,2000):
            for dy in range(-1000,1001,1000):
                screen.blit(backPic,(offx+dx,offy+dy))

    def drawStars(self):
        offx = 400-round(self.planet[0]*0.1)
        offy = 300-round(self.planet[1]*0.1)
        offx = offx%800
        offy = offy%600
        for dx in range(-800,801,800):
            for dy in range(-600,601,600):
                screen.blit(starsPic,(offx+dx,offy+dy))

def instructions():
    running = True
    inst = image.load("instructions.jpg")
    inst = transform.smoothscale(inst, screen.get_size())
    screen.blit(inst,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False

        display.flip()
    return "menu"
        
def credit():
    running = True
    cred = image.load("credits.jpg")
    cred = transform.smoothscale(cred, screen.get_size())
    screen.blit(cred,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False

        display.flip()
    return "menu"

def menu():
    running = True
    font.init()
    myFont = font.SysFont("impact",20)
    myClock = time.Clock()
    buttons = [Rect(300,y*80+200,200,50) for y in range(3)]
    vals = ["PLAY","INSTRUCTIONS","CREDITS"]
    planet = [400,300]
    background = Draw(planet,None)
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "exit"

        mpos = mouse.get_pos()
        mb = mouse.get_pressed()

        planet[0] += 10
        planet[1] += 10
        background.drawBack()
        background.drawStars()
        
        for b,v in zip(buttons,vals):
            draw.rect(screen,(200,200,200),b)
            label = myFont.render((v),1,(0,0,0))
            offx = (200-len(v)*10)/2
            screen.blit(label,(b[0]+offx,b[1]+12))  #in middle of button
            if b.collidepoint(mpos):
                draw.rect(screen,(255,255,255),b,3)
                if mb[0]==1:
                    return v
            else:
                draw.rect(screen,(50,50,50),b,3)
                
        display.flip()

screen = display.set_mode((800, 600))
running = True
x,y = 0,0
OUTLINE = (150,50,30)
page = "menu"
while page != "exit":
    if page == "menu":
        page = menu()
    if page == "PLAY":
        page = menu()   #temp  
    if page == "INSTRUCTIONS":
        page = instructions()        
    if page == "CREDITS":
        page = credit()    
    
quit()
