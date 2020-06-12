import pygame

from direction import Direction

class Snake(pygame.sprite.Sprite):
    """Snake class"""
    def __init__(self, screen, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.direction = Direction.RIGHT
        self.height, self.width = [30, 30]
        self.dead = False
        self.locations = []

    def move(self, new_location):
        """moves the snake to a new location"""
        #pygame.draw.rect(SCREEN, BG_COLOUR, self.rect)  # "Erases" the current snake
        self.rect.left, self.rect.top = new_location
        self.screen.blit(self.image, self.rect)
