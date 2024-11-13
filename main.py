import pygame,math
from sys import exit 
import random
import time

pygame.init()

kills = 0
life = 3

pos = 'right'

zombie_timer = pygame.USEREVENT+1
pygame.time.set_timer(zombie_timer,2300)
screen = pygame.display.set_mode((900,700))
pygame.display.set_caption('DuckyFlappy')
clock = pygame.time.Clock()

click = False
gamplay = False
lose = False 

font = pygame.font.Font('fonts/Peace Sans Webfont.ttf', 32)

duck_img = pygame.image.load('img/ducky.png')
duck_img = pygame.transform.scale(duck_img, (100, 100))
duck_img2 = pygame.image.load('img/ducky2.png')
duck_img2 = pygame.transform.scale(duck_img2, (100, 100))

guns_img = ['img/gun.png', 'img/gun1.png']

zombie_arr = ['img/zombie1.png','img/zombie1.png','img/zombie1.png']

aim_img = pygame.image.load('img/aim.png')
grass_img = pygame.image.load('img/grass.png')
grassbg_lose_img = pygame.image.load('img/losebg.png')
lose_img = pygame.image.load('img/aim.png')
restart_img = pygame.image.load('img/restart.png')

startbg_img = pygame.image.load('img/startbg.png')
start_button_img = pygame.image.load('img/start-button.png')

start_img = pygame.transform.scale(start_button_img, (100, 100))

flowers_img = ['img/flower1.png','img/flower2.png',
               'img/flower3.png','img/flower4.png',
               'img/flower1.png','img/flower2.png',
               'img/flower3.png','img/flower4.png',
               'img/flower4.png']

bullet_img = pygame.image.load('img/bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (70, 70))

text_lose_img = pygame.image.load('img/gameover.png')
text_start_img = pygame.image.load('img/welcome.png')

text_lose = font.render("YOU LOSE! ", True, "#A4A4AB")
text_start = font.render("WELCOME TO DUCKY FLUPPY!", True, "#FFFFFF")
text_restart = font.render("Restart! ", True, "#50C878")

restart_label_rect = restart_img.get_rect(topleft=(380, 330))
start_label_rect = start_button_img.get_rect(topleft=(300, 280))

cord_x = 200 
cord_y = 200

speed_x = 3
speed_y = 3
count = 0

end_time = 0

class Duck():
    def ducky_print(x, y):
        if pos == 'left':
            screen.blit(duck_img, (x,y))
        else:
            screen.blit(duck_img2, (x,y))  

    def moves(keys):
        global cord_x
        global cord_y
        global pos
        if keys[pygame.K_a]:
            pos = 'right'
            cord_x -= speed_x
        if keys[pygame.K_d]:
            pos = 'left'
            cord_x += speed_x
        if keys[pygame.K_w]:
            cord_y -= speed_y
        if keys[pygame.K_s]:
            cord_y += speed_y

class PlayerBullet:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y 
        self.mouse_x = mouse_x 
        self.mouse_y = mouse_y
        self.speed = 15
        self.angle = math.atan2(y - mouse_y,x - mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
        self.rect = bullet_img.get_rect(topleft=(self.x, self.y), width=70, height=70)
    def main(self, screen):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)
        self.rect.x -= int(self.x_vel)
        self.rect.y -= int(self.y_vel)
        dx, dy = get_coordination(cord_x, cord_y, mx, my)
        angle = math.atan2(dx,dy)
        bullet_img2 = pygame.transform.rotate(bullet_img, angle*60)
        screen.blit(bullet_img2, (self.x, self.y))


class Zombie:
    def __init__(self):
        self.x = random.randint(0, 800)
        self.y = random.randint(650, 750)
        self.zombie_img = pygame.image.load(zombie_arr[random.randint(0,2)])
        self.zombie_img = pygame.transform.scale(self.zombie_img, (80, 80))
        self.rect = self.zombie_img.get_rect(topleft=(self.x,self.y),width=80,height=80)

    def main(self,screen,cord_x,cord_y):
        dx,dy = get_coordination(cord_x,cord_y,self.x,self.y)
        angle = math.atan2(dx,dy)
        mvx = math.sin(angle)
        mvy = math.cos(angle)
        self.x+=mvx
        self.y+=mvy
        self.rect.x+=mvx
        self.rect.y+=mvy
        
        screen.blit(self.zombie_img, (self.x,self.y))
        
class Gun():
    def gun_print(x,y):
        
        gun_img = pygame.image.load(guns_img[1])
        gun_img = pygame.transform.scale(gun_img, (90, 90))
        
        gun_img2 = pygame.image.load(guns_img[0])
        gun_img2 = pygame.transform.scale(gun_img2, (90, 90))
        
        dx,dy = get_coordination(cord_x,cord_y,mx,my)
        angle = math.atan2(dx,dy)
        
        if angle<0:
            gun_img3 = pygame.transform.rotate(gun_img, angle*60)
        else:
            gun_img3 = pygame.transform.rotate(gun_img2, angle*60)
            
        screen.blit(gun_img3, (x,y))
    
    def gun_vector():
        dx,dy = get_coordination(cord_x,cord_y,mx,my)
        angle = math.atan2(dx,dy)
        mvx = math.sin(angle) * -(90)
        mvy = math.cos(angle) * -(90)
        return mvx,mvy

def aim_print(x,y):
    screen.blit(aim_img, (x,y))

def pos_generator(count):
    positions = []
    for i in range(count):
        positions.append(random.randint(100, 800))
    return positions
    
def spawn_object(img,x,y):
    img = pygame.image.load(img)
    img = pygame.transform.scale(img, (50, 50))
    screen.blit(img, (x,y))

def get_coordination(x1,y1,x2,y2):
    dx = x1-x2
    dy = y1-y2
    return dx,dy

player_bullets = []
zombie = []

pos_arr = pos_generator(40)

player_bullets.append(PlayerBullet(0,0,0,0))

flow = 0

while True:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                
    keys = pygame.key.get_pressed()
    mx,my=pygame.mouse.get_pos()   
             
    if gamplay:

        player_rect = duck_img.get_rect(topleft=(cord_x,cord_y),width=60, height=60)
        
        if zombie:
            for (i, zombies) in enumerate(zombie):
                if player_rect.colliderect(zombies):
                    if life == 1:
                        gamplay = False
                        lose = True
                        player_bullets.clear()
                        zombie.clear()
                        kills = 0 
                        cord_x = 200
                        cord_y = 200
                        lifes = 3
                    else:
                        zombie.pop(i)
                        life-=1
                    
        screen.fill((24,164,86))
        screen.blit(grass_img,(0,0))
        
        for flower_i in range(9):
            spawn_object(flowers_img[flower_i], pos_arr[flower_i], pos_arr[flower_i+1])
        for flower_i in range(9):
            spawn_object(flowers_img[flower_i], pos_arr[flower_i], pos_arr[flower_i+10])
        for flower_i in range(9):
            spawn_object(flowers_img[flower_i], pos_arr[flower_i], pos_arr[flower_i+23])

        if event.type == zombie_timer:
            zombie.append(Zombie())

        aimy = my-20
        aimx = mx-20

        aim_print(aimx,aimy)

        mvx, mvy = Gun.gun_vector()

        Duck.moves(keys)
        Duck.ducky_print(cord_x,cord_y)
        Gun.gun_print(cord_x+mvx/1.2,cord_y+10+mvy/1.2)

        if event.type == pygame.MOUSEBUTTONDOWN and click == False:
            player_bullets.append(PlayerBullet(cord_x+mvx/1.2,cord_y+10+mvy/1.2,mx, my))
            end_time = pygame.time.get_ticks() + 100

        if current_time < end_time:
            click = True
        else: 
            click = False

        if zombie and player_bullets:
                for (i, zombies) in enumerate(zombie):
                    if player_bullets[-1].rect.colliderect(zombies):
                            zombie.pop(i)
                            player_bullets.pop(-1)
                            kills+=1
                       
                           
        life_text = font.render("Lifes: "+str(life)+"/3 | ", True, "#E1DD00")                 
        kills_text = font.render("KILLS: "+str(kills), True, "#E1DD00")
        life_rect = life_text.get_rect().center = (25,25)
        kills_rect = kills_text.get_rect().center = (200, 25)
        screen.blit(life_text, life_rect)
        screen.blit(kills_text, kills_rect)

        for bullet in player_bullets:
            bullet.main(screen)

        for zombie1 in zombie:
            zombie1.main(screen,cord_x,cord_y)
            
    elif lose:
        
        screen.blit(grassbg_lose_img,(0,0))
        screen.blit(text_lose_img, (175,200))
        screen.blit(restart_img, (restart_label_rect))
        
        if restart_label_rect.collidepoint(mx,my) and event.type == pygame.MOUSEBUTTONDOWN:
            gamplay = True
    
    else: 
        screen.blit(startbg_img,(0,0))
        screen.blit(text_start_img, (45,200))
        screen.blit(start_button_img, (start_label_rect))

        if start_label_rect.collidepoint(mx,my) and event.type == pygame.MOUSEBUTTONDOWN:
            gamplay = True

            
    pygame.display.update()
    clock.tick(60)