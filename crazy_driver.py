## CRAZY DRIVER (simplified) ##

#Modules
import pygame
import random
pygame.init()

#Variables
score = 0
level = 0

road_speed = 12
speed = 10

#Display
infoObject = pygame.display.Info()
correction = 90
screen_height = infoObject.current_h-correction
screen_width = int(((infoObject.current_h-correction)*9)/16)

win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("CRAZY ML")

carwidth = int((60*screen_width)/((990*9)/16))
carheight = int((120*screen_height)/990)

t1 = int((55*screen_height)/990)
t2 = int((32*screen_height)/990)
t3 = int((22*screen_height)/990)
t4 = int((38*screen_height)/990)
t5 = int((42*screen_height)/990)

big_font = pygame.font.Font("texture/font.ttf", t1)
small_font = pygame.font.Font("texture/font.ttf",t2) #menus and score
credits_font = pygame.font.Font("texture/font.ttf",t3)
bonus_font = pygame.font.Font("texture/font.ttf",t4)
level_font = pygame.font.Font("texture/font.ttf",t5)

#Textures
road = pygame.image.load("texture/road.png").convert()
road = pygame.transform.scale(road, (screen_width, int((screen_width*road.get_height())/road.get_width())))
roads=[i*road.get_height() for i in range(int(screen_height/road.get_height())+2)]

car = pygame.image.load('texture/red.png').convert_alpha()
car.set_colorkey((255,255,255))
car = pygame.transform.scale(car, (carwidth, carheight))

explo = pygame.image.load('texture/explosionn.png').convert_alpha()
explo = pygame.transform.scale(explo, (380, 400))
explo.set_colorkey((255,255,255))

green = pygame.image.load('texture/green.png').convert_alpha()
green.set_colorkey((255,255,255))
green = pygame.transform.scale(green, (carwidth, carheight))

blue = pygame.image.load('texture/blue.png').convert_alpha()
blue.set_colorkey((255,255,255))
blue = pygame.transform.scale(blue, (carwidth, carheight))

orange = pygame.image.load('texture/orange.png').convert_alpha()
orange.set_colorkey((255,255,255))
orange = pygame.transform.scale(orange, (carwidth, carheight))

yellow = pygame.image.load('texture/yellow.png').convert_alpha()
yellow.set_colorkey((255,255,255))
yellow = pygame.transform.scale(yellow, (carwidth, carheight))

grey = pygame.image.load('texture/grey.png').convert_alpha()
grey.set_colorkey((255,255,255))
grey = pygame.transform.scale(grey, (carwidth, carheight))

black = pygame.image.load('texture/black.png').convert_alpha()
black.set_colorkey((255,255,255))
black = pygame.transform.scale(black, (carwidth, carheight))

dblue = pygame.image.load('texture/dblue.png').convert_alpha()
dblue.set_colorkey((255,255,255))
dblue = pygame.transform.scale(dblue, (carwidth, carheight))

obs_color=[green,blue,orange,yellow,grey,black,dblue]

#Class
class Car(object):

    def __init__(self, x, y, vel, color):
        self.x = x
        self.y = y
        self.width = carwidth
        self.height = carheight
        self.vel = vel
        self.color = color
        self.hitbox=(self.x, self.y, self.width, self.height)
        self.accounted=False

    def draw_(self,win):
        if self.__class__.__name__ == "Player":
            win.blit(car,(self.x,self.y))
            #self.hitbox=(self.x, self.y, self.width-1, self.height-1)
            #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        elif self.__class__.__name__ == "Obstacle":
            win.blit(obs_color[self.color],(self.x,self.y))
            #self.hitbox=(self.x, self.y, self.width-1, self.height-1)
            #pygame.draw.rect(win,(255,0,0),self.hitbox,2)

    def set_y(self,y):
        self.y = y

    def set_vel(self,v):
        self.vel = v

    def get_vel(self):
        return self.vel

class Player(Car):

    def mvt(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and p.x>p.vel:
            p.x -= p.vel
        if keys[pygame.K_RIGHT] and p.x<screen_width-p.width-p.vel:
            p.x += p.vel

class Obstacle(Car):

    def set_color(self):
        self.color = color_()

    def set_x(self):
        self.x = random.randint(0,screen_width-self.width)

    def is_accounted(self):
        self.accounted = True

    def not_accounted(self):
        self.accounted = False

    def mvt(self):
        global speed
        if self.y >= screen_height:
            self.set_x()
            self.set_y(-self.height)
            self.set_color()
            self.set_vel(speed)
            self.not_accounted()
        else:
            self.y += self.vel

class Explosion(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 28

    def mvt(self):
        global speed
        self.timer -= 1
        if self.y < screen_height and self.timer > 0:
            self.y += speed
        else:
            explosions.pop(explosions.index(self))

    def draw_(self,win):
        global explo
        win.blit(explo,(self.x,self.y))

p=Player((screen_width-carwidth)/2,screen_height-180,5,(255,0,0))
p.set_vel(5)

obstacles=[]

explosions=[]

level_up_text=[]

def color_():
    a=random.randint(0,len(obs_color)-1)
    return(a)

def explosion_(p,o):
    global explosions
    explosion_sound = pygame.mixer.Sound("sound/explosion.wav")
    if p.__class__.__name__=="Player":
        explosion_sound.play()
        x=(p.x+o.x)*0.5-explo.get_width()/2
        y=(max(p.y,o.y)+min(p.y+p.height,o.y+o.height))*0.5-explo.get_height()/2
        explosions.append(Explosion(x,y))
    else:
        explosion_sound.set_volume(0.25)
        explosion_sound.play()
        x=(p.x+o.x)*0.5-explo.get_width()/2
        y=(max(p.y,o.y)+min(p.y+p.height,o.y+o.height))*0.5-explo.get_height()/2
        explosions.append(Explosion(x,y))
        obstacles.pop(obstacles.index(p))
        obstacles.pop(obstacles.index(o))

def obstacle_collision(obstacle,obstacles):
    for o in obstacles:
        if obstacle!=o:
            if obstacle.x + obstacle.width >= o.x and obstacle.x <= o.x + o.width and obstacle.y + obstacle.height >= o.y and obstacle.y< o.y + o.height:
                if o.y==-obstacle.height:
                    o.set_x()
                else:
                    explosion_(obstacle,o)
                    obstacles.append(Obstacle(random.randint(0,screen_width-carwidth), -carheight, speed, color_()))
                    obstacles.append(Obstacle(random.randint(0,screen_width-carwidth), -8*carheight, speed, color_()))


def road_mvt():
    global roads,road_speed
    l=len(roads)
    for i in range(l):
        if roads[i]>screen_height:
            roads[i]=-road.get_height()
            win.blit(road,(0,roads[i]))
        else:
            roads[i]+=road_speed
            win.blit(road,(0,roads[i]))

def redrawGameWindow():
    global d,e
    road_mvt()
    p.draw_(win)
    for obstacle in obstacles:
        obstacle.draw_(win)
    for explosion in explosions:
        explosion.draw_(win)
    for text in level_up_text:
        text.draw_(win)
        text.timer-=1
    text_score=small_font.render("Score: "+str(score), 1, (255,0,0))
    #pygame.draw.rect(win,(0,0,0),(0,0,text_score.get_width()+4,text_score.get_height()+2))
    win.blit(text_score,(screen_width/2 - text_score.get_width()/2,2))

    pygame.display.update()

def mainLoop():
    global score, speed, road, roads, road_speed, obstacles, explosions
    score=0
    speed=1
    roads=[i*road.get_height() for i in range(int(screen_height/road.get_height())+2)]
    road_speed=3
    obstacles=[]
    obstacles.append(Obstacle(random.randint(0,screen_width-carwidth), -carheight, speed, color_()))
    obstacles.append(Obstacle(random.randint(0,screen_width-carwidth), -4*carheight, speed, color_()))
    obstacles.append(Obstacle(random.randint(0,screen_width-carwidth), -8*carheight, speed, color_()))
    explosions=[]

    level=0
    level_score=[0.4*((i+1)**2) for i in range(1,100)]

    timer=80

    run = True
    crash = False
    while run and not crash:
        pygame.time.delay(int(100/6)-1)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        for obstacle in obstacles:
            obstacle_collision(obstacle,obstacles)
            if obstacle.x + obstacle.width >= p.x and obstacle.x <= p.x + p.width and obstacle.y + obstacle.height >= p.y and obstacle.y< p.y + p.height:
                crash = True
                explosion_(p,obstacle)
            else:
                obstacle.mvt()
                if obstacle.y>p.y+p.height and not obstacle.accounted:
                    obstacle.is_accounted()
                    score+=1
        for explosion in explosions:
            explosion.mvt()
        if score>=level_score[level]:
            level+=1
            if level%2==0:
                road_speed+=1
                speed=road_speed-2
                p.set_vel(p.get_vel()+0.2)
            else:
                obstacles.append(Obstacle(random.randint(0,screen_width-carwidth), -(2*speed)*carheight, speed, color_()))

        p.mvt()
        redrawGameWindow()

    while run and crash and timer>0:
        pygame.time.delay(int(100/6))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        timer-=1
        redrawGameWindow()
    pygame.quit()
    return 1

mainLoop()