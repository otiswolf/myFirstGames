import pygame, sys, random
from pygame.locals import *

pygame.init()

# set the fps
FPS = 30
fpsClock = pygame.time.Clock()

# set up screen variables
maxX = 500
maxY = 500
tileSize = 20

# set up the window
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption('snake')
pygame.mouse.set_visible(0)

# set the colors/constants
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
RIGHT = "R"
LEFT = "L"
UP = "U"
DOWN = "D"

# set up game variables
moveTicker = 0
gameOver = False
score = 0
snakeX = 0
snakeY = 0
snakeDirection = RIGHT
snakeBody = [(snakeX-1, snakeY), (snakeX-2, snakeY)]


def reset_values():
    global moveTicker, gameOver, score, snakeX, snakeY, snakeDirection, snakeBody
    moveTicker = 0
    gameOver = False
    score = 0
    snakeX = 0
    snakeY = 0
    snakeDirection = RIGHT
    snakeBody = [(snakeX - 1, snakeY), (snakeX - 2, snakeY)]


# create game over window
def create_game_over_screen():
    fontObj = pygame.font.Font('freesansbold.ttf', 46)
    gameOverSurfaceObj = fontObj.render("game over", True, RED, BLACK)
    gameOverRectObj = gameOverSurfaceObj.get_rect()
    gameOverRectObj.center = (maxX // 2, maxY // 2)
    fontObj = pygame.font.Font('freesansbold.ttf', 24)
    scoreSurfaceObj = fontObj.render("score: {}".format(score), True, RED, BLACK)
    scoreRectObj = scoreSurfaceObj.get_rect()
    scoreRectObj.center = (gameOverRectObj.center[0], gameOverRectObj.center[1] + 30)
    restartSurfaceObj = fontObj.render("press space to restart", True, RED, BLACK)
    restartRectObj = restartSurfaceObj.get_rect()
    restartRectObj.center = (scoreRectObj.center[0], scoreRectObj.center[1]+30)
    screen.fill(BLACK)
    screen.blit(gameOverSurfaceObj, gameOverRectObj)
    screen.blit(scoreSurfaceObj, scoreRectObj)
    screen.blit(restartSurfaceObj, restartRectObj)


# draw the game board
def draw_board():
    screen.fill(BLACK)
    for i in range(0, maxX, tileSize):
        pygame.draw.line(screen, WHITE, (0, i), (maxX, i))
        pygame.draw.line(screen, WHITE, (i, 0), (i, maxY))


# draw the snake
def draw_snake(x, y):
    pygame.draw.rect(screen, GREEN, (x, y, tileSize, tileSize))
    for segment in snakeBody:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], tileSize, tileSize))


# move the snake in the designated direction
def move_snake(direction):
    global snakeX, snakeY
    for i in range(len(snakeBody)-1, -1, -1):
        if i == 0:
            snakeBody[i] = (snakeX, snakeY)
        else:
            snakeBody[i] = snakeBody[i-1]
    if direction == UP:
        if snakeY >= tileSize:
            snakeY -= tileSize
    if direction == LEFT:
        if snakeX >= tileSize:
            snakeX -= tileSize
    if direction == DOWN:
        if snakeY < maxY - tileSize:
            snakeY += tileSize
    if direction == RIGHT:
        if snakeX < maxX - tileSize:
            snakeX += tileSize


# create a piece of food on a random tile
def create_food():
    while 1:
        x = random.randint(0, maxX - 1) // tileSize * tileSize
        y = random.randint(0, maxY - 1) // tileSize * tileSize
        if not (x, y) in snakeBody and (x, y) != (snakeX, snakeY):
            return (x, y)


food = create_food()


# draw the food
def draw_food():
    pygame.draw.rect(screen, BLUE, (food[0], food[1], tileSize, tileSize))


def consume_food():
    global food, score
    snakeBody.append(snakeBody[len(snakeBody)-1])
    food = create_food()
    score += 1


def check_if_collided():
    if (snakeX, snakeY) in snakeBody: return True
    if snakeX < 0 or snakeX >= maxX: return True
    if snakeY < 0 or snakeY >= maxY: return True
    return False


# main event loop
while 1:
    if not gameOver:
        draw_board()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    snakeDirection = UP
                if event.key == pygame.K_a:
                    snakeDirection = LEFT
                if event.key == pygame.K_s:
                    snakeDirection = DOWN
                if event.key == pygame.K_d:
                    snakeDirection = RIGHT

        if moveTicker == 0:
            move_snake(snakeDirection)
            moveTicker = 3

        if check_if_collided():
            gameOver = True

        if (snakeX, snakeY) == food:
            consume_food()

        draw_food()
        draw_snake(snakeX, snakeY)

        if moveTicker > 0:
            moveTicker -= 1

    else:
        # you lost
        create_game_over_screen()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_values()

    pygame.display.update()
    fpsClock.tick(FPS)



