import pygame
import random
import time

run = True
pygame.init()
screen = pygame.display.set_mode((800, 600))
bodyParts = 3
space = 20
speed = .05
snake_color = (0, 255, 255)
direction = "right"
score = 0
string = "Score : {}"
font = pygame.font.Font('freesansbold.ttf', 32)
pygame.display.set_caption('Snake Game')
text = font.render(string.format(score), True, (255, 255, 255))
disabled = False

def draw(ifFoodCollected):
    global snake
    global food
    global space
    global text
    global string
    screen.fill((0, 0 ,0))
    snake.draw()
    text = font.render(string.format(score), True, (255, 255, 255))
    screen.blit(text, (300, 0))
    if ifFoodCollected:
        food = Food()
    else:
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food.cords[0], food.cords[1], space, space))


def collision(snok):
    x, y = snake.cords[0]
    if x < 0 or x >= 800:
        return True
    if y < 0 or y >= 600:
        return True
    for i in snake.cords[1:]:
        if x == i[0] and y == i[1]:
            return True
    return False


class Food:
    def __init__(self):
        x = random.randint(0, int(800/space)-1) * space
        y = random.randint(0, int(600/space)-1) * space
        self.cords = [x, y]
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x, y, space, space))


class Snake:
    def __init__(self):
        self.cords = []
        self.bodyParts = bodyParts
        self.squares = []
        for i in range(0, bodyParts):
            self.cords.append([400, 300])
        for x, y in self.cords:
            square = pygame.draw.rect(screen, snake_color, pygame.Rect(x, y, space, space))
            self.squares.append(square)

    def draw(self):
        for x, y in self.cords:
            square = pygame.draw.rect(screen, snake_color, pygame.Rect(x, y, space, space))
            self.squares.append(square)


def next_turn(snek, foed):
    if not run:
        return
    x, y = snek.cords[0]
    global direction
    global space
    global disabled
    global score
    if direction == "up":
        y -= space
    elif direction == "down":
        y += space
    elif direction == "left":
        x -= space
    elif direction == "right":
        x += space
    disabled = False
    snek.cords.insert(0, (x, y))
    square = pygame.draw.rect(screen, snake_color, pygame.Rect(x, y, space, space))
    snek.squares.insert(0, square)
    if collision(snek):
        game_over()
    else:
        if x == foed.cords[0] and y == foed.cords[1]:
            score += 1
            draw(True)
        else:
            del snek.cords[-1]
            del snek.squares[-1]
            draw(False)


def changeDirection(newDir):
    global direction
    global disabled
    if disabled:
        return
    disabled = True
    if newDir == "left":
        if direction != "right":
            direction = newDir
    if newDir == "right":
        if direction != "left":
            direction = newDir
    if newDir == "up":
        if direction != "down":
            direction = newDir
    if newDir == "down":
        if direction != "up":
            direction = newDir


def game_over():
    global score
    global screen
    global font
    global run
    screen.fill((0, 0, 0))
    xd = "apples."
    if score == 0:
        score = "no"
        xd = "apples N00B!"
    elif score == 1:
        xd = "apple."

    fnt = pygame.font.Font('freesansbold.ttf', 64)
    txt = fnt.render("Game Over!", False, (255, 255, 255))
    screen.blit(txt, (200, 300))
    footer = font.render(f"Your final score was {score}  {xd}", False, (255, 255, 255))
    screen.blit(footer, (130, 250))
    run = False



food = Food()
snake = Snake()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                changeDirection("up")
            if event.key == pygame.K_s:
                changeDirection("down")
            if event.key == pygame.K_a:
                changeDirection("left")
            if event.key == pygame.K_d:
                changeDirection("right")
    time.sleep(speed)
    next_turn(snake, food)
    pygame.display.update()
