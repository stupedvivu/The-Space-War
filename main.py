## flaticon.com
## freepik.com
import pygame
import random
import math

# initialize pygame
pygame.init()

SCREEN_X = 800
SCREEN_Y = 600

# player
PLAYER_SIZE = 64
DELTA_MOVEMENT_PLAYER = 0.4
playerImg = pygame.image.load('player.png')
playerDeltaX = 0
playerDeltaY = 0
playerX = 370
playerY = 500

# enemies
N_ENIMIES = 5
ENEMY_SIZE = 64
DELTA_MOVEMENT_ENEMY = [0.4] * N_ENIMIES
enemyImg = pygame.image.load('enemy.png')
enemyDeltaX = 0
enemyDeltaY = 10
enemyX = []
enemyY = []

# bullet
# Ready = you can't see a bullet
# Fire = bullet is currently moving
BULLET_SIZE = 64
BULLET_FIRE_POSITION = PLAYER_SIZE // 4
DELTA_MOVEMENT_BULLET = 0.4
bulletImg = pygame.image.load('bullet.png')
bulletDeltaX = 0
bulletDeltaY = 3
bulletX = 0
bulletY = playerY
bulletState = 'Ready'

# collision
COLLISION_THRESH = ENEMY_SIZE // 4

# score
SCORE_VALUE = 0
FONT = pygame.font.Font('freesansbold.ttf', 32)

# set pygame screen size
screen = pygame.display.set_mode((800, 600))

# background
backgroundImg = pygame.image.load('background.png')
pygame.display.set_icon(backgroundImg)

# title and icon
pygame.display.set_caption("The Space War")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)


def DrawPlayer(x, y):
    # to draw img on the screen
    screen.blit(playerImg, (x, y))
   
# draws a single enemy
def DrawEnemy(x, y):
    screen.blit(enemyImg, (x, y))
    
def InitializeEnemies():
    for i in range(N_ENIMIES):
        enemyX.append(random.randint(0, SCREEN_X))
        enemyY.append(random.randint(50, 150))
    
def FireBullet(x, y):
    global bulletState
    bulletState = 'Fire'
    screen.blit(bulletImg, (x + BULLET_FIRE_POSITION, y + 10))
    
def IsCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    
    if distance < COLLISION_THRESH:
        return True
    return False

def ShowScore():
    score = FONT.render('SCORE: ' + str(SCORE_VALUE), True, (255, 255, 255))
    screen.blit(score, (10, 10))

    
InitializeEnemies()

running = True
while running:
    # screen.fill((0, 0, 0))
    screen.blit(backgroundImg, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerDeltaX -= DELTA_MOVEMENT_PLAYER
            elif event.key == pygame.K_RIGHT:
                playerDeltaX += DELTA_MOVEMENT_PLAYER
            elif event.key == pygame.K_SPACE and bulletState is 'Ready':
                bulletX = playerX
                FireBullet(bulletX, bulletY)        
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerDeltaX = 0
    
    # check for enemy boundry
    for i in range(N_ENIMIES):
        enemyX[i] += DELTA_MOVEMENT_ENEMY[i]
        if enemyX[i] < 0:
            DELTA_MOVEMENT_ENEMY[i] = abs(DELTA_MOVEMENT_ENEMY[i])
            enemyY[i] += enemyDeltaY
        elif enemyX[i] >= SCREEN_X - ENEMY_SIZE:
            DELTA_MOVEMENT_ENEMY[i] = -DELTA_MOVEMENT_ENEMY[i]
            enemyY[i] += enemyDeltaY
    
    # check for player boundry
    playerX += playerDeltaX
    if playerX < 0:
        playerX = 0
    elif playerX >= SCREEN_X - PLAYER_SIZE:
        playerX = SCREEN_X - PLAYER_SIZE
        
    # bullet movement
    if bulletY < 0:
        bulletState = 'Ready'
        bulletY = playerY # reset bullet position
    if bulletState is 'Fire':
        FireBullet(bulletX, bulletY)
        bulletY -= bulletDeltaY
        
    # collision
    # bullet and enemy collision detecttion
    for i in range(N_ENIMIES):
        if IsCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            bulletY = playerY
            bulletState = 'Ready'
            SCORE_VALUE += 1
            print(SCORE_VALUE)
            enemyX[i] = random.randint(0, SCREEN_X)
            enemyY[i] = random.randint(50, 150)
    
    DrawPlayer(playerX, playerY)
    for i in range(N_ENIMIES):
        DrawEnemy(enemyX[i], enemyY[i])
    ShowScore()
    pygame.display.update() # update is necessary to reflect the changes