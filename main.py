import sys
import pygame
from settings import Settings
from player import Player
from baddie import Baddie
from pathlib import Path
import csv


class Dodger:
    """
    Overall class to manage game assets and behavior.
    """

    def __init__(self):
        """
        Initialize the game and create game resources.
        """
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Dodger')
        self.clock = pygame.time.Clock()

        self.player = Player(self)
        self.baddies = pygame.sprite.Group()
        self.add_baddie_counter = 0
        reader = self._get_reader()
        first_row = next(reader)
        self.high_score = int(first_row[2])
        self.score = 0
        self.game_active = False

        # Set up sounds.
        self.gameOverSound = pygame.mixer.Sound('gameover.wav')
        pygame.mixer.music.load('background.mid')

        # noinspection PyTypeChecker
        self.font = pygame.font.SysFont(None, 48)
        # noinspection PyTypeChecker
        self.bigfont = pygame.font.SysFont(None, 96)
        self.screen.fill(self.settings.bg_color)
        self._start_game()

    def run_game(self):
        while self.game_active:
            self.add_baddie_counter += 1
            self._check_events()
            self.player.update()
            self._update_screen()
            if self.add_baddie_counter == self.settings.add_new_baddie_rate:
                self._create_baddies()
                self.add_baddie_counter = 0
            self._update_baddies()
            self._check_collisions()
            self.clock.tick(60)

    def _start_game(self):
        self.screen.fill(self.settings.bg_color)
        self._draw_text('Score: {}'.format(self.score), self.font, self.screen, 10, 0)
        self._draw_text('High Score: {}'.format(self.high_score), self.font, self.screen, 10, 40)
        self._draw_text('Dodger', self.font, self.screen, (self.settings.screen_width / 3),
                        (self.settings.screen_height / 3))
        self._draw_text('Press a key to start.', self.font, self.screen, (self.settings.screen_width / 3) - 30,
                        (self.settings.screen_height / 3) + 50)
        pygame.display.update()
        self._wait_for_player_to_press_key()
        pygame.mixer.music.play(-1, 0.0)

    def _draw_text(self, text, font, surface, x, y):
        textobj = font.render(text, 1, self.settings.text_color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def _wait_for_player_to_press_key(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Pressing ESC quits.
                        sys.exit()
                    else:
                        self._restart_game()
                        self.game_active = True
                    return

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

    def _check_collisions(self):
        if pygame.sprite.spritecollideany(self.player, self.baddies):
            pygame.mixer.music.stop()
            self.gameOverSound.play()
            if self.score > self.high_score:
                self.high_score = self.score
            self.game_active = False
            with open('high_scores.csv','w',newline='') as f:
                w = csv.writer(f)
                w.writerow(['1', '', str(self.high_score)])
            self._wait_for_player_to_press_key()

    def _update_screen(self):
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.player.blitme()
        self.baddies.draw(self.screen)
        self._draw_text('Score: {}'.format(self.score), self.font, self.screen, 10, 0)
        self._draw_text('High Score: {}'.format(self.high_score), self.font, self.screen, 10, 40)

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _create_baddies(self):
        new_baddie = Baddie(self)
        self.baddies.add(new_baddie)

    def _update_baddies(self):
        self.baddies.update()
        # get rid of baddies that have disappeared
        for baddie in self.baddies.copy():
            if baddie.rect.top > self.settings.screen_height:
                self.baddies.remove(baddie)
                self.score += 1
                if self.score > self.high_score:
                    self.high_score += 1

    def _restart_game(self):
        for baddie in self.baddies:
            self.baddies.remove(baddie)
        self.score = 0
        self.player = Player(self)
        self.gameOverSound.stop()
        pygame.mixer.music.play(-1, 0.0)

    '''
    def _high_score_screen(self):
        self.game_active = False
        self.hss_active = True
        self.screen.fill(self.settings.bg_color)
        reader = self._get_reader()
        while True:
            self._draw_text('High Scores', self.bigfont, self.screen, (self.settings.screen_width / 6),
                            (self.settings.screen_height / 10))
            ah = 0
            sp = ' '
            for row in reader:
                place = row[0]
                name = row[1]
                score = row[2]
                self._draw_text(str(place + sp + name + sp + score), self.font, self.screen,
                                (self.settings.screen_width / 6), ((self.settings.screen_height / 4) + ah))
                ah += 40
            pygame.display.flip()
            self._wait_for_key_2()
    '''

    def _get_reader(self):
        path = Path('high_scores.csv')
        lines = path.read_text().splitlines()
        reader = csv.reader(lines)
        return reader


if __name__ == '__main__':
    # Make a game instance, and run the game.
    dodger = Dodger()
    dodger.run_game()
