"""
Annie Zhang
ICS 3U
Mr. McKenzie
Final Project

Space Colliders

Based on flash game "Planets Collide".
Use WASD controls and left-click to shoot (endless ammunition). Objective of the game is to become
the largest planet, starting from an asteroid, growing to become Mercury, Mars, Venus, Earth,
Neptune, Uranus, Saturn, and Jupiter, respectively. Players gain size by pulling in smaller planets
and asteroids. If health or time reaches 0, game over. Same goes for if the player gets pulled in
by a bigger object. Health decreases as aliens invade the player's space.
"""
#==================START==============================================================
from pygame import *
from random import *
from math import *
import glob
init()
mixer.init()
#================CLASSES=================================================================
class Background:
    def __init__(self,playerPos):
        self.playerPos = playerPos

    def back(self):
        offx = 500-round(self.playerPos[0]*0.2)
        offy = 300-round(self.playerPos[1]*0.2)
        offx = offx%2000
        offy = offy%1000
        for dx in range(-2000,2001,2000):       #2000 is width of background image
            for dy in range(-1000,1001,1000):   #1000 is height of bg image
                screen.blit(backPic,(offx+dx,offy+dy))

    def stars(self):
        offx = 500-round(self.playerPos[0]*0.1)
        offy = 300-round(self.playerPos[1]*0.1)
        offx = offx%1000
        offy = offy%600
        for dx in range(-1000,1001,1000):   #1000 is width of stars image
            for dy in range(-600,601,600):  #600 is height of stars image
                screen.blit(starsPic,(offx+dx,offy+dy))
    
class Player:
    def __init__(self,pos,speed,size,pic,health):
        self.pos = pos
        self.speed = speed
        self.size = size
        self.pic = planPic
        self.health = health
        
    def friction(self):
        self.speed[0] *= 0.99   #Slows down player after a while
        self.speed[1] *= 0.99

    #PLAYER GRAVITY: pulls player toward bigger planets
    def gravity(self):
        global page
        G = 10
        for obj in objects:
            pic = obj.pic
            w = pic.get_width()
            h = pic.get_height()
            m1 = obj.size**3*10000
            dx = obj.pos[0]-self.pos[0]
            dy = obj.pos[1]-self.pos[1]
            r = hypot(dx,dy)
            if obj.pic.get_height() < self.size and r<=300:
                obj.gravity()
            else:
                if r <= obj.size*h*0.8:
                    self.health = -1
                    page = "GAME OVER"
                if r <= 300:
                    #PHYSICS: Fg = G(m1)(m2)/(r^2) = acc(m2)
                    acc = G*m1/(r**2)
                    ang = atan2(dy,dx)  #aang
                    self.speed[0] += acc*cos(ang)
                    self.speed[1] += acc*sin(ang)

    def move(self,keys):
        if keys[K_a]:
            self.speed[0] -= .3
        if keys[K_d]:
            self.speed[0] += .3
        if keys[K_w]:
            self.speed[1] -= .3
        if keys[K_s]:
            self.speed[1] += .3
        if abs(self.speed[0]) > 10:     #Don't want player travelling too fast, max out at speed of 10
            self.speed[0] = 10 * (self.speed[0] / abs(self.speed[0]))
        if abs(self.speed[1]) > 10:
            self.speed[1] = 10 * (self.speed[1] / abs(self.speed[1]))
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        self.friction()
        self.gravity()
        generateChunks(self.pos[0],self.pos[1]) #Create new chunk of planets around player ("endless")

    def draw(self):
        if 300<self.size<=400:   #Only for saturn because saturn's rings are greater than its height
            screen.blit(self.pic,(500-self.size,300-self.size//2))
        else:
            screen.blit(self.pic,(500-self.size//2,300-self.size//2))
        
class Alien:
    def __init__(self,pos,health,pic):
        self.pos = pos
        self.health = health
        self.pic = pic
        
    def move(self):
        dx = self.pos[0]-player.pos[0]
        dy = self.pos[1]-player.pos[1]
        d = hypot(dx,dy)
        ang = atan2(dy,dx)

        vx = 10*cos(ang)
        vy = 10*sin(ang)

        vx -= 8*player.size*dx/d**2        #Repel alien from player
        vy -= 8*player.size*dy/d**2

        for a in aliens:
            if a != self:
                ax = a.pos[0] - self.pos[0] #Distance between fellow aliens
                ay = a.pos[1] - self.pos[1]
                d = hypot(ax,ay)
                ang = atan2(ay,ax)
                vx += 40*ax/d**2            #Repels each alien from each other so they're not in each
                vy += 40*ay/d**2            #other's personal space
        
        self.pos[0] -= vx   
        self.pos[1] -= vy
        
    def draw(self):
        offx = 500-round(player.pos[0])
        offy = 300-round(player.pos[1])
        if abs(self.pos[0]-player.pos[0]) < 2000 and abs(self.pos[1]-player.pos[1]) < 1000:
            w = self.pic.get_width()
            h = self.pic.get_height()
            screen.blit(self.pic,(self.pos[0]+offx-w//2,self.pos[1]+offy-h//2))
            draw.rect(screen,(255,0,0),(self.pos[0]+offx-w//2,self.pos[1]+offy-15,self.health,5))

    def attack(self):
        dx = self.pos[0]-player.pos[0]
        dy = self.pos[1]-player.pos[1]
        d = hypot(dx, dy)
        if d < 100:
            player.health -= 0.1    #Kills player slower

class Object:   #Planets
    def __init__(self,pos,size,speed,pic):
        self.pos = pos
        self.size = size
        self.speed = speed
        self.pic = transform.scale(pic,(int(pic.get_width()*size),int(pic.get_height()*size)))

    def move(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]

    def draw(self):
        offx = 500-round(player.pos[0])
        offy = 300-round(player.pos[1])
        if abs(self.pos[0]-player.pos[0]) < 3000 and abs(self.pos[1]-player.pos[1]) < 1000:
            w = self.pic.get_width()
            h = self.pic.get_height()
            screen.blit(self.pic,(self.pos[0]+offx-w//2,self.pos[1]+offy-h//2)) #-w//2 and -h//2 ==> centres referenced

    #OBJECT GRAVITY: pulls planets towards player
    def gravity(self):
        global level,newLevel,page,planPic
        G = 10
        w = self.pic.get_width()
        h = self.pic.get_height()
        m1 = player.size
        dx = self.pos[0]-player.pos[0]
        dy = self.pos[1]-player.pos[1]
        r = hypot(dx,dy)
        if r <= player.size/2.2:
            objects.remove(self)
            player.size += self.size*h/1.4
            if player.size <= 60:
                planPic = objList[0]
            elif player.size <= 75:
                newLevel = 2
                planPic = objList[1]
            elif player.size <= 100:
                newLevel = 3
                planPic = objList[2]
            elif player.size <= 130:
                newLevel = 4
                planPic = objList[3]
            elif player.size <= 170:
                newLevel = 5
                planPic = objList[4]
            elif player.size <= 230:
                newLevel = 6
                planPic = objList[5]
            elif player.size <= 300:
                newLevel = 7
                planPic = objList[6]
            elif player.size <= 400:
                newLevel = 8
                planPic = objList[7]
            elif player.size <= 530:
                newLevel = 9
                planPic = objList[8]
            w = planPic.get_width()
            h = planPic.get_height()
            if 300 < player.size <= 400:
                player.pic = transform.smoothscale(planPic,(int(player.size*2),int(player.size)))
            else:
                player.pic = transform.smoothscale(planPic,(int(player.size),int(player.size)))
            return
        if r <= 300:
            #PHYSICS: Fg = G(m1)(m2)/(r^2) = acc(m2)
            acc = G*m1/(r**2)
            ang = atan2(dy,dx)
            self.speed[0] -= acc*cos(ang)
            self.speed[1] -= acc*sin(ang)

class Bullet:
    def __init__(self,ang,x,y,vx,vy):
        self.ang = ang
        self.x = x
        self.y = y
        self.vx = vx #initial velocity
        self.vy = vy
        self.alive = True

    def move(self):
        oldx = self.x
        oldy = self.y
        self.x += 15*cos(self.ang)+self.vx
        self.y += 15*sin(self.ang)+self.vy
        if hypot(self.x-player.pos[0],self.y-player.pos[1])>600:
            self.alive = False
        self.damage(oldx,oldy)
    
    def draw(self):
        offx = 500-player.pos[0]
        offy = 300-player.pos[1]
        dx = player.pos[0]-self.x
        dy = player.pos[1]-self.y
        dist = player.size/2.3
        ang = atan2(dy,dx)
        draw.circle(screen,(255,0,0),(int(offx+self.x-dist*cos(ang)),int(offy+self.y-dist*sin(ang))),3)

    def damage(self,lastx,lasty):
        dx = self.x-lastx
        dy = self.y-lasty
        dist = hypot(dx,dy)
        ang = atan2(dy,dx)
        dead = []
        end = False
        for a in aliens:
            if end:
                break
            else:
                for i in range(int(dist)):
                    if abs(lastx+i*cos(ang)-a.pos[0]+15)<15 and abs(lasty+i*sin(ang)-a.pos[1]+7.5)<15:
                        a.health -= 50
                        self.alive = False
                        end = True
                        if a.health<=0: #Kill off dead aliens
                            dead.append(a)
                        break
        for ghost in dead:
            aliens.remove(ghost)
            
#========================FUNCTIONS=================================================
#Objects
#Using player position, find where to generate objects
def generateChunks(x,y):
    closeX = int((x+2500)//5000)*5000 #Finds nearest multiple of 5000
    closeY = int((y+2500)//5000)*5000
    for xx in range(closeX-5000,closeX+5001,5000):
        for yy in range(closeY-5000,closeY+5001,5000):
            if (xx,yy) not in spawnedChunks:
                createObjects(xx,yy)

#Spawns a set number of objects in the chunk (rectangle) from (midx-2500,midy-2500) to (midx+2500,midy+2500)
def createObjects(midx,midy):
    spawnedChunks.add((midx,midy)) #Keep track of which chunks were generated, so you don't generate one twice
    for i in range(level*100):
        scale = randint(0,10)
        if scale < 10:
            scale = randint(5,20)
        else:
            scale = randint(21,50)
        if (midx,midy) == (0,0): #If this is the center chunk, don't spawn planets in the middle
                                #so you don't die immediately when game starts
            ex = choice([randint(-5000,-60),randint(60,5000)])
            ey = choice([randint(-5000,-60),randint(60,5000)])
        else:
            ex = randint(midx-2500,midx+2500)
            ey = randint(midy-2500,midy+2500)
        pic = objList[randint(0,10)]
        objects.append(Object([ex,ey],scale/100,[0,0],pic))

def moveObjects():
    for obj in objects:
        obj.move()

def drawObjects():
    for obj in objects:
        obj.draw()

#Aliens
def createAliens():
    ex = randint(int(player.pos[0]-500),int(player.pos[0]+500))
    ey = randint(int(player.pos[1]-300),int(player.pos[1]+300))
    aliens.append(Alien([ex-15,ey-7.5],100,alienPic))       #centred

def moveAliens():
    for a in aliens:
        a.move()
        a.attack()
        
def drawAliens():
    for a in aliens:
        a.draw()

#Bullets
def moveBullets():
    dead = []
    for b in bullets:
        b.move()
        if not b.alive:
            dead.append(b)
    for shell in dead:
        try:
            bullets.remove(shell)   #Get rid of bullets AFTER calling b.move(), so bullets list isn't messed up
        except:
            print("BULLET ERROR")
            break

def drawBullets():
    for b in bullets:
        b.draw()

#Main
def checkLevel():
    global level,health
    if level != newLevel:
        level = newLevel
        health = 100
        return True
    return False

def update(keys):
    global page
    player.move(keys)
    moveObjects()
    moveBullets()
    moveAliens()
    
def drawScene():
    background.back()
    background.stars()
    drawObjects()
    player.draw()
    drawBullets()
    drawAliens()

def reset():
    global level,newLevel,playerPos,planPic,playerSpeed,size,player,objects,spawnedChunks,aliens,background,bullets,health
    level = 1
    newLevel = 1
    playerPos = [0,0]
    planPic = transform.scale(objList[0],(50,50))
    playerSpeed = [0,0]
    size = 50
    health = 100 
    player = Player(playerPos,playerSpeed,size,planPic,health)
    objects = []
    spawnedChunks = set()
    aliens = []
    background = Background(playerPos)
    bullets = []

#===============IMAGES=======================================================================
backPic = image.load("back1.jpg")
backPic = transform.scale(backPic,(2000,1000))
starsPic = image.load("stars.png")
starsPic = transform.scale(starsPic,(1000,600))

objList = []
for i in glob.glob("objList/*.png"):
    objList.append(image.load(i))
#=============VARIABLES==========================================================================
level = 1
newLevel = 1
health = 100
levelTimes = [0,60,60,50,50,40,40,40,30,30,30]

playerPos = [0,0]
planPic = transform.scale(objList[0],(50,50))
alienPic = transform.scale(image.load("alien.png"),(30,15))
playerSpeed = [0,0]
size = 50
player = Player(playerPos,playerSpeed,size,planPic,health)

objects = []
spawnedChunks = set()   #apparently performs faster
aliens = []
bullets = []

background = Background(playerPos)

scrSize = (1000,600)
screen = display.set_mode(scrSize)
screenRect = Rect(0,0,1000,600)
#=================PAGES=======================================================================
def instructions():
    running = True
    inst = image.load("instructions.png")
    screen.blit(inst,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        display.flip()
    if main:
        return "MENU"
    else:
        return "MENU2"
        
def credit():
    running = True
    cred = image.load("credits.png")
    screen.blit(cred,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        display.flip()
    return "MENU"

def menu():
    running = True
    font.init()
    myFont = font.SysFont("impact",20)
    buttons = [Rect(400,y*80+200,200,50) for y in range(3)]
    vals = ["PLAY","INSTRUCTIONS","CREDITS"]
    pos = [500,300]
    background = Background(pos)
    while running:
        click = False
        for e in event.get():          
            if e.type == QUIT:
                return "QUIT"
            if e.type == MOUSEBUTTONDOWN:
                click = True

        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        pos[0] += 10
        pos[1] += 10
        background.back()
        background.stars()
        titleFont = font.SysFont("impact",40)
        title = titleFont.render("Space Colliders",1,(255,50,50))
        screen.blit(title,(390,100))

        for i in range(len(buttons)):
            label = myFont.render((vals[i]),1,(100,100,100))
            offx = (200-len(vals[i])*10)/2
            screen.blit(label,(buttons[i][0]+offx,buttons[i][1]+12))  #in middle of button
            if buttons[i].collidepoint(mpos):
                draw.rect(screen,(255,255,255),buttons[i],3)
                label = myFont.render((vals[i]),1,(255,255,255))
                screen.blit(label,(buttons[i][0]+offx,buttons[i][1]+12))
                if click:
                    return vals[i]
        display.flip()

def menu2():
    running = True
    myFont = font.SysFont("impact",20)
    buttons = [Rect(400,y*80+200,200,50) for y in range(3)]
    vals = ["RESUME","INSTRUCTIONS","QUIT"]
    pos = [500,300]
    background = Background(pos)
    while running:
        click = False
        for e in event.get():          
            if e.type == QUIT:
                return "PLAY"
            if e.type == MOUSEBUTTONDOWN:
                click = True
        
        mpos = mouse.get_pos()
        background.back()
        background.stars()
        
        for i in range(len(buttons)):
            label = myFont.render((vals[i]),1,(100,100,100))
            offx = (200-len(vals[i])*10)/2
            screen.blit(label,(buttons[i][0]+offx,buttons[i][1]+12))  #in middle of button
            if buttons[i].collidepoint(mpos):
                draw.rect(screen,(255,255,255),buttons[i],3)
                label = myFont.render((vals[i]),1,(255,255,255))
                screen.blit(label,(buttons[i][0]+offx,buttons[i][1]+12))
                if click:
                    if vals[i] == "QUIT":
                        reset()
                        return menu()
                    return vals[i] 
        display.flip()

def over():
    reset()
    running = True
    myFont = font.SysFont("impact",20)
    overFont = font.SysFont("impact",40)
    buttons = [Rect(400,y*80+300,200,50) for y in range(2)]
    vals = ["PLAY AGAIN","QUIT"]
    pos = [500,300]
    background = Background(pos)
    while running:
        click = False
        for e in event.get():          
            if e.type == QUIT:
                return "QUIT"
            if e.type == MOUSEBUTTONDOWN:
                click = True
        
        mpos = mouse.get_pos()
        background.back()
        background.stars()
        gameOver = overFont.render("GAME OVER",1,(255,0,0))
        screen.blit(gameOver,(420,200))
        
        for i in range(len(buttons)):
            label = myFont.render((vals[i]),1,(100,100,100))
            offx = (200-len(vals[i])*10)/2
            screen.blit(label,(buttons[i][0]+offx,buttons[i][1]+12))
            if buttons[i].collidepoint(mpos):
                draw.rect(screen,(255,255,255),buttons[i],3)
                label = myFont.render((vals[i]),1,(255,255,255))
                screen.blit(label,(buttons[i][0]+offx,buttons[i][1]+12))
                if click:
                    if vals[i] == "PLAY AGAIN":
                        reset()
                        return "PLAY"
                    return vals[i] 
        display.flip()

def win():
    reset()
    running = True
    mixer.music.load("cheer.mp3")
    mixer.music.play(1,3)
    myFont = font.SysFont("impact",20)
    bigFont = font.SysFont("impact",40)
    congrats = bigFont.render("CONGRATS, you won!",1,(255,0,0))
    congrats2 = bigFont.render("CONGRATS, you won!",1,(200,10,10))
    buttons = [Rect(250+300*y,400,200,50) for y in range(2)]
    vals = ["PLAY AGAIN","QUIT"]
    pos = [500,300]
    frameCnt = 0
    background = Background(pos)
    while running:
        click = False
        for e in event.get():          
            if e.type == QUIT:
                return "QUIT"
            if e.type == MOUSEBUTTONDOWN:
                click = True
        frameCnt += 1
        mpos = mouse.get_pos()
        pos[0] += 10
        pos[1] += 10
        background.back()
        background.stars()
        
        if frameCnt%2==0:
            screen.blit(congrats2,((350,200)))
        else:
            screen.blit(congrats,(350,200))
            
        for i in range(len(buttons)):
            label = myFont.render((vals[i]),1,(100,100,100))
            offx = (200-len(vals[i])*10)/2
            screen.blit(label,(buttons[i][0]+offx,buttons[i][1]+12))
            if buttons[i].collidepoint(mpos):
                draw.rect(screen,(255,255,255),buttons[i],3)
                label = myFont.render((vals[i]),1,(255,255,255))
                screen.blit(label,(buttons[i][0]+offx,buttons[i][1]+12))
                if click:
                    if vals[i] == "PLAY AGAIN":
                        reset()
                        return "PLAY"
                    return vals[i]
            
        display.flip()
#===============GAME========================================================================
def game():
    running = True
    startTime = time.get_ticks()
    frameCnt = 0    #Set counter instead of using time--time changes for each level
    #============LOOP STARTS===============================================================
    while running:
        click = False
        levelChange = checkLevel()
        for e in event.get():
            if e.type == QUIT:
                running = False
                return "QUIT"
            if e.type == MOUSEBUTTONDOWN:
                click = True
        #=============MOVEMENT==============================================================
        keys = key.get_pressed()
        if keys[K_SPACE]:
            return "MENU2"  #Pause
        mb = mouse.get_pressed()
        mx,my = mouse.get_pos()

        update(keys)
        drawScene()
        if player.size>540:
            return "WIN"
        #Shooting
        if click:
            ang = atan2(my-300,mx-500)
            bullets.append(Bullet(ang,player.pos[0],player.pos[1],player.speed[0],player.speed[1]))

        #Reset time
        if levelChange:
            startTime = time.get_ticks()
        timeElapse = time.get_ticks()-startTime

        #Generate aliens
        frameCnt += 1
        if frameCnt % 100 == 0:
            createAliens()
            
        times = levelTimes[level]*1000-(timeElapse) #Time left

        if times < 0 or player.health < 0:
            reset()
            return "GAME OVER"

        myFont = font.SysFont("impact",20)
        timer = myFont.render("Time Left: "+(str(times/1000)),1,(255,10,10))
        levelIcon = myFont.render("Level: "+str(level),1,(255,10,10))
        healthIcon = myFont.render("Health: "+str(int(player.health)),1,(255,10,10))
        screen.blit(levelIcon,(10,10))
        screen.blit(healthIcon,(10,40))
        screen.blit(timer,(10,70))
        display.flip()

#==============PAGES======================================================================
page = "MENU"
while page != "QUIT":
    if page == "MENU":
        main = True
        page = menu()
    if page == "PLAY" or page == "RESUME":
        page = game()
    if page == "INSTRUCTIONS":
        page = instructions()        
    if page == "CREDITS":
        page = credit()
    if page == "MENU2":
        main = False
        page = menu2()
    if page == "GAME OVER":
        page = over()
    if page == "WIN":
        page = win()

quit()
