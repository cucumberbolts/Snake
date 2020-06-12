import pygame
import random

from snake import Snake
from food import Food
from direction import Direction

# Sets things up
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 960, 540
SCREEN = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
BG_COLOUR = [0, 0, 0]
SCREEN.fill(BG_COLOUR)
ICON = pygame.image.load("assets/snake.ico")
CAPTION = "Snake!"
pygame.display.set_caption(CAPTION)
pygame.display.set_icon(ICON)
GAME_OVER_IMAGE = pygame.image.load("assets/GameOver.png")

speed = 5
score = 0
SNAKE_IMAGE = "assets/snake.png"  # 30 x 30
FOOD_IMAGE = "assets/food.png"  # 30 x 30


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
    x = random.randint(0, SCREEN_WIDTH - 30)
    y = random.randint(0, SCREEN_HEIGHT - 30)

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
    SCREEN.fill(BG_COLOUR)  # Clears the screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Checks for any keyboard input
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and snake.direction != Direction.UP:  # Move down
                snake.direction = Direction.DOWN
            elif event.key == pygame.K_UP and snake.direction != Direction.DOWN:  # Move up
                snake.direction = Direction.UP
            elif event.key == pygame.K_LEFT and snake.direction != Direction.RIGHT:  # Move left
                snake.direction = Direction.LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != Direction.LEFT:  # Move right
                snake.direction = Direction.RIGHT
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
        speed += 1  # Increments the snake's speed

    # Moves the individual snake parts
    for part in snakes:
        part_number = snakes.index(part)
        part.move(snake.locations[part_number])

    SCREEN.blit(food.image, food.rect)  # Shows food

    # Checks if snake should die
    # If touching walls...
    if snake.rect.left < 0:
        snake.dead = True
    elif snake.rect.right > SCREEN_WIDTH:
        snake.dead = True
    elif snake.rect.top < 0:
        snake.dead = True
    elif snake.rect.bottom > SCREEN_HEIGHT:
        snake.dead = True

    for rest_of_snake in snakes[1:]:
        if pygame.sprite.collide_rect(snake, rest_of_snake):
            snake.dead = True

    if snake.dead:
        break

    pygame.time.delay(int(100 - speed))  # Pauses

    pygame.display.flip()

pygame.quit()
