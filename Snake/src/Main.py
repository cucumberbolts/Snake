import random
import pygame

from snake import Snake
from food import Food
from direction import Direction

# Initialize pygame
pygame.init()
pygame.font.init()

# Sets things up
width, height = 960, 540
SCREEN = pygame.display.set_mode((width, height))
ICON = pygame.image.load("../assets/snake.ico")
CAPTION = "Snake!"
pygame.display.set_caption(CAPTION)
pygame.display.set_icon(ICON)
GAME_OVER_IMAGE = pygame.image.load("../assets/GameOver.png")

font = pygame.font.SysFont("Comic Sans MS", 24, 1)

score = 0
SNAKE_IMAGE = "../assets/snake.png"  # 30 x 30
FOOD_IMAGE = "../assets/food.png"  # 30 x 30


def pause():
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False

        pygame.time.delay(5)


def get_random_pos():
    """Gets random locations on the screen that are multiples of 30"""

    # Chooses random coordinates
    x = random.randint(0, width - 30)
    y = random.randint(0, height - 30)

    # Makes it a multiple of 30
    x = x - (x % 30)
    y = y - (y % 30)

    return x, y


snake = Snake(SCREEN, SNAKE_IMAGE, [180, 180])
snakes = [snake]
food = Food(SCREEN, FOOD_IMAGE, get_random_pos())

# Pygame event loop
running = True

while running:
    SCREEN.fill([0, 0, 0])  # Clears the screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Checks for any keyboard input
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and snake.direction != Direction.UP:  # Move down
                snake.direction = Direction.DOWN
                break
            elif event.key == pygame.K_UP and snake.direction != Direction.DOWN:  # Move up
                snake.direction = Direction.UP
                break
            elif event.key == pygame.K_LEFT and snake.direction != Direction.RIGHT:  # Move left
                snake.direction = Direction.LEFT
                break
            elif event.key == pygame.K_RIGHT and snake.direction != Direction.LEFT:  # Move right
                snake.direction = Direction.RIGHT
                break
            elif event.key == pygame.K_p:
                pause()

    # Moves the snake according to the direction
    if snake.direction == Direction.RIGHT:
        snake.locations.insert(0, [snake.rect.left + snake.width, snake.rect.top])  # Adds the location
    elif snake.direction == Direction.LEFT:
        snake.locations.insert(0, [snake.rect.left - snake.width, snake.rect.top])  # Adds the location
    elif snake.direction == Direction.UP:
        snake.locations.insert(0, [snake.rect.left, snake.rect.top - snake.height])  # Adds the location
    elif snake.direction == Direction.DOWN:
        snake.locations.insert(0, [snake.rect.left, snake.rect.top + snake.height])  # Adds the location

    if pygame.sprite.collide_rect(snake, food):  # If food is eaten
        food.move(get_random_pos())
        part_number = len(snakes) + 1
        snakes.append(Snake(SCREEN, SNAKE_IMAGE, snake.locations[part_number]))
        score += 1  # Increments score

    # Moves the individual snake parts
    for part in snakes:
        part_number = snakes.index(part)
        part.move(snake.locations[part_number])

    SCREEN.blit(food.image, food.rect)  # Shows food

    score_display = font.render("Score: " + str(score), False, (255, 255, 255))
    SCREEN.blit(score_display, (10, 10))

    # Checks if snake should die
    # If touching walls...
    if snake.rect.left < 0:
        snake.dead = True
    elif snake.rect.right > width:
        snake.dead = True
    elif snake.rect.top < 0:
        snake.dead = True
    elif snake.rect.bottom > height:
        snake.dead = True

    for rest_of_snake in snakes[1:]:
        if pygame.sprite.collide_rect(snake, rest_of_snake):
            snake.dead = True

    if snake.dead:
        running = False

    pygame.time.delay(80)  # Pauses

    pygame.display.flip()

pygame.quit()
