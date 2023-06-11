class Settings:
    '''
    A class to store all settings for the Dodger game.
    '''

    def __init__(self):
        '''
        Initialize the game's settings.
        '''

        # Screen settings
        self.screen_width = 600
        self.screen_height = 600
        self.bg_color = (255, 255, 255)
        self.text_color = (0, 0, 0)
        self.player_speed = 5
