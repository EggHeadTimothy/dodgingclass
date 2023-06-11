import pygame

class Player:

    def __init__(self, dodger):
        # Initialize the player and set its starting position.
        self.screen = dodger.screen
        self.settings = dodger.settings
        self.screen_rect = dodger.screen.get_rect()

        # Load the image
        self.image = pygame.image.load('player.png')
        self.rect = self.image.get_rect()

        # Start player at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # floats for horizontal (x) position and vertical (y) position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # movement flags
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False


    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.player_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.player_speed
        self.rect.x = self.x
        self.rect.y = self.y


    def blitme(self):
        # Draw the player at its current location
        self.screen.blit(self.image, self.rect)
