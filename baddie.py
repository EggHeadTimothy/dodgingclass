import pygame
import random
from pygame.sprite import Sprite

class Baddie(Sprite):

    def __init__(self, dodger):
        super().__init__()
        self.screen = dodger.screen
        self.settings = dodger.settings
        self.screen_rect = dodger.screen.get_rect()

        baddie_size = random.randint(self.settings.baddie_min_size, self.settings.baddie_max_size)
        baddie_speed = random.randint(self.settings.baddie_min_speed, self.settings.baddie_max_speed)

        # Load the image
        self.image = pygame.image.load('baddie.png')
        self.rect = self.image.get_rect()

        # Initialize attributes randomly
        self.size = baddie_size
        self.speed = baddie_speed

        # Initialize position randomly
        self.rect.x = random.randint(0, self.settings.screen_width - self.size)
        self.rect.y = 0
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        # Draw the player at its current location
        self.screen.blit(self.image)

    def update(self):
        self.y -= baddie_speed
        self.rect.y = self.y