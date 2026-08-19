import pygame


class SoundManager:
    def __init__(self):
        # Initialize the audio engine
        pygame.mixer.init()

        # Load Sound Effects (Placeholders)
        self.bounce_wall = self._load_sound("bounce_wall.wav")
        self.bounce_paddle = self._load_sound("bounce_paddle.wav")
        self.freeze_sound = self._load_sound("freeze.wav")

    def _load_sound(self, filename):
        try:
            return pygame.mixer.Sound(filename)
        except FileNotFoundError:
            print(f"Audio placeholder missing: Please add '{filename}' to your folder!")
            return None

    def play_wall_bounce(self):
        if self.bounce_wall:
            self.bounce_wall.play()

    def play_paddle_bounce(self):
        if self.bounce_paddle:
            self.bounce_paddle.play()

    def play_freeze(self):
        if self.freeze_sound:
            self.freeze_sound.play()

    def start_bgm(self):
        try:
            # pygame.mixer.music is specifically optimized for long background tracks
            pygame.mixer.music.load("trockey_bgm.mp3")
            # Passing -1 tells the music to loop infinitely!
            pygame.mixer.music.play(-1)
        except pygame.error:
            print("BGM placeholder missing: Please add 'trockey_bgm.mp3' to your folder!")

    def stop_bgm(self):
        # Stops the music instantly when called
        pygame.mixer.music.stop()