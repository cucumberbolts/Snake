import pygame

class Food(pygame.sprite.Sprite):
    """food class"""
    def __init__(self, screen, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.height, self.width = [30, 30]
        self.eaten = False

    def move(self, new_location):
        """moves the food to a new location"""
        # You don't need to erase the food because the snake draws over it for you, creating a smoother eat process
        self.rect.left, self.rect.top = new_location
        self.screen.blit(self.image, self.rect)
