import pygame
from sys import exit 

pygame.init()

screen = pygame.display.set_mode((900,700))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

YELLOW = '#FFFF00'
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

cord_x = 400 
cord_y = 200
speed_x = 3
count = 0

font = pygame.font.Font('freesansbold.ttf', 32)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    if(cord_x>=820):
        count += 1
        speed_x = -count+2
    if(cord_x==0):
        count += 1
        speed_x = +count+2
    
    cord_x += speed_x
    screen.fill('Red')
    pygame.draw.rect(screen, YELLOW, (cord_x, cord_y, 80, 80))
    text = font.render(str(count), True, GREEN, BLUE)
    textRect = text.get_rect()
    textRect.center = (200//2, 200//2)
    screen.blit(text, textRect)
    pygame.display.flip()
    print(cord_x)
    clock.tick(60)
