import pygame
import random

# Sets things up
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
BG_COLOUR = [0, 0, 0]
SCREEN.fill(BG_COLOUR)
ICON = pygame.image.load("snake.ico")
CAPTION = "Snake!"
pygame.display.set_caption(CAPTION)
pygame.display.set_icon(ICON)
GAME_OVER_IMAGE = pygame.image.load("GameOver.png")

speed = 5
score = 0
SNAKE_IMAGE = "snake.png"  # 30 x 30
FOOD_IMAGE = "food.png"  # 30 x 30


class Snake(pygame.sprite.Sprite):
    """Snake class"""
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.direction = "right"
        self.dimentions = self.height, self.width = [30, 30]
        self.dead = False
        self.locations = []

    def move(self, new_location):
        """moves the snake to a new location"""
        pygame.draw.rect(SCREEN, BG_COLOUR, self.rect)  # "Erases" the current snake
        self.rect.left, self.rect.top = new_location
        SCREEN.blit(self.image, self.rect)


class Food(pygame.sprite.Sprite):
    """food class"""
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.dimentions = self.height, self.width = [30, 30]
        self.eaten = False

    def move(self, new_location):
        """moves the food to a new location"""
        # You don't need to erase the food because the snake draws over it for you, creating a smoother eat process
        self.rect.left, self.rect.top = new_location
        SCREEN.blit(self.image, self.rect)


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
    x = random.randint(0, 800 - 30)
    y = random.randint(0, 600 - 30)
    
    # Makes it a multiple of 30
    x = x - (x % 30)  
    y = y - (y % 30)
    
    return x, y

snake = Snake(SNAKE_IMAGE, [180, 180])
snakes = [snake]
food = Food(FOOD_IMAGE, get_random_pos())

# Pygame event loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Checks for any keyboard input
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and snake.direction != "up":  # Move down
                snake.direction = "down"
            elif event.key == pygame.K_UP and snake.direction != "down":  # Move up
                snake.direction = "up"
            elif event.key == pygame.K_LEFT and snake.direction != "right":  # Move left
                snake.direction = "left"
            elif event.key == pygame.K_RIGHT and snake.direction != "left":  # Move right
                snake.direction = "right"
            elif event.key == pygame.K_p:
                pause()

    # Moves the snake according to the direction
    if snake.direction == "right":
        snake.locations.insert(0, [snake.rect.left + snake.width, snake.rect.top])  # Adds the location
    elif snake.direction == "left":
        snake.locations.insert(0, [snake.rect.left - snake.width, snake.rect.top])  # Adds the location
    elif snake.direction == "up":
        snake.locations.insert(0, [snake.rect.left, snake.rect.top - snake.height])  # Adds the location
    elif snake.direction == "down":
        snake.locations.insert(0, [snake.rect.left, snake.rect.top + snake.height])  # Adds the location

    # Moves the individual snake parts
    for part in snakes:
        part_number = snakes.index(part)
        part.move(snake.locations[part_number])

    if pygame.sprite.collide_rect(snake, food):  # If food is eaten
        food.move(get_random_pos())
        part_number = len(snakes) + 1
        snakes.append(Snake(SNAKE_IMAGE, snake.locations[part_number]))
        score += 1  # Increments score
        speed += 1  # Increments the snake's speed

    SCREEN.blit(food.image, food.rect)  # Shows food 

    # Checks if snake should die
    # If touching walls...
    if snake.rect.left < 0:
        snake.dead = True
    elif snake.rect.left + snake.width > SCREEN_WIDTH:
        snake.dead = True
    elif snake.rect.top < 0:
        snake.dead = True
    elif snake.rect.top + snake.height > SCREEN_HEIGHT:
        snake.dead = True
    """
    for rest_of_snake in snakes[1:]:
        if pygame.sprite.spritecollide(snake, rest_of_snake):
            snake.dead = True
    """
    if snake.dead:  # If snake is dead...
        SCREEN.blit(GAME_OVER_IMAGE, [800, 600, 0, 0])
        pygame.time.delay(1000)
        running = False

    pygame.time.delay(int(100 - speed))  # Delays the snake 'cause otherwise, it would go waaay too fast

    pygame.display.flip()

pygame.quit()
