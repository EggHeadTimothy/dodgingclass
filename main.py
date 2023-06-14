import sys
import pygame
from settings import Settings
from player import Player
from baddie import Baddie

class Dodger:
    '''
    Overall class to manage game assets and behavior.
    '''

    def __init__(self):
        '''
        Initialize the game and create game resources.
        '''
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Dodger')
        self.clock = pygame.time.Clock()

        self.player = Player(self)
        self.baddies = pygame.sprite.Group()
        test_baddie = Baddie(self)
        self.baddies.add(test_baddie)

    def run_game(self):
        while True:
            self._check_events()
            self.player.update()
            self._update_screen()
            self._create_baddie()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.player.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.player.moving_left = True
        elif event.key == pygame.K_UP:
            self.player.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.player.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.player.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.player.moving_left = False
        elif event.key == pygame.K_UP:
            self.player.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.player.moving_down = False

    def _update_screen(self):
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.player.blitme()
        self.baddies.draw(self.screen)


        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _create_baddie(self):
        new_baddie = Baddie(self)
        self.baddies.add(new_baddie)


if __name__ == '__main__':
    # Make a game instance, and run the game.
    dodger = Dodger()
    dodger.run_game()
