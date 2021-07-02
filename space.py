import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_SPACE, K_c
from random import randint
import math
import sys
pygame.init()
screen = pygame.display.set_mode((800,600))
#title
icon = pygame.image.load('launch.png')
pygame.display.set_caption("Space Invader")
pygame.display.set_icon(icon)
#background
background = pygame.image.load('background.jpeg')

WHITE = (255,255,255)
BLACK = (0,0,0)
#player
player_img = pygame.transform.scale(pygame.image.load("battleship.png"),(60,60))
player_X = 370
player_Y = 430 
playerX_change = 0
#enemy
enemy_img = []
enemy_X = []
enemy_Y = []
enemyX_change = []
enemyY_change = []
enemy_amount = 6
for i in range (enemy_amount):
    enemy_img.append(pygame.transform.scale(pygame.image.load("alien.png"),(60,60)))
    enemy_X.append(randint(0,740))
    enemy_Y.append(randint(50,150))
    enemyX_change.append( 0.7)
    enemyY_change.append(40)
#bullet
bullet_img = pygame.image.load("bullet.png")
bullet_X = 0
bullet_Y = 430
bulletX_change = 0
bulletY_change = 1.5
bullet_state = "ready"
def player(x,y):
    screen.blit(player_img,(x,y))
def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))
def bullet_fire(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img,(x + 14.9,y))
#collision
def is_collision(bullet_X,bullet_Y,enemy_X,enemy_Y):
    distance = math.sqrt((math.pow(bullet_X-enemy_X,2))+(math.pow(bullet_Y-enemy_Y,2)))
    if distance < 27:
        return True
    else:
        return False
#score
score = 0
def show_score():
    font = pygame.font.Font('freesansbold.ttf', 32)
    score_screen = font.render('Score: ' + str(score) , True , (255,255,255))
    screen.blit(score_screen,(10,10)) 
#game_over
def game_over():
    over_font = pygame.font.Font('freesansbold.ttf',70)
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,200))

while True:
    screen.fill((BLACK))
    #background
    screen.blit(background,(0,0))
    #line
    pygame.draw.rect(screen,WHITE,(0,400,800,10))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #player keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == K_c:
                pass
            if event.key == K_LEFT:
                playerX_change = -0.8
            if event.key == K_RIGHT:
                playerX_change = 0.8
            #bullet keystroke
            if event.key == K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = pygame.mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_X = player_X
                    bullet_fire(bullet_X,bullet_Y)
        #player keyup
        if event.type == pygame.KEYUP:
            if event.key == K_RIGHT or event.key == K_LEFT:
                playerX_change = 0
    #player movement
    player_X += playerX_change
    #boundaries
    if player_X <= 0 :
        player_X =0
    elif player_X >= 740:
        player_X = 740
    #enemy movement
    for i in range (enemy_amount):
        enemy_X[i] += enemyX_change[i]
        #boundaries
        if enemy_X[i] <= 0 :
            enemyX_change[i] = 0.7
            enemy_Y[i] += enemyY_change[i]
        elif enemy_X[i] >= 740:
            enemyX_change[i] = -0.7
            enemy_Y[i] += enemyY_change[i]
        
        #collision
        collision = is_collision(bullet_X,bullet_Y,enemy_X[i],enemy_Y[i])
        if(collision):
            bullet_Y = 430
            bullet_state = "ready"
            enemy_X[i] = randint(0,740)
            enemy_Y[i] = randint(50,150) 
            score += 1
            explosion_sound = pygame.mixer.Sound("explosion.wav")
            explosion_sound.play()
        if enemy_Y[i] >= 350:
            for j in range (enemy_amount):
                enemy_Y[j] = 2000
            game_over()
            lose_sound = pygame.mixer.Sound("lose.wav")
            lose_sound.play()
            break
        enemy(enemy_X[i],enemy_Y[i],i)
    #bullet movement
    if bullet_state == "fire":
        bullet_fire(bullet_X,bullet_Y)
        bullet_Y -= bulletY_change 
    if bullet_Y <= 0:
        bullet_state = "ready"
        bullet_Y = 430
    
    player(player_X,player_Y)
    
    show_score()
    pygame.display.update()
