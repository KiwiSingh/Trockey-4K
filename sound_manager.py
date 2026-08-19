import os
import sys
import pygame #type: ignore

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.bgm_muted = False

        self.bounce_wall = self._load_sound("bounce_wall.wav")
        self.bounce_paddle = self._load_sound("bounce_paddle.wav")
        self.freeze_sound = self._load_sound("freeze.wav")

    def _load_sound(self, filename):
        safe_path = resource_path(filename)
        try:
            return pygame.mixer.Sound(safe_path)
        except FileNotFoundError:
            print(f"Audio missing: Please add '{filename}' to your folder!")
            return None

    def play_wall_bounce(self):
        if self.bounce_wall: self.bounce_wall.play()

    def play_paddle_bounce(self):
        if self.bounce_paddle: self.bounce_paddle.play()

    def play_freeze(self):
        if self.freeze_sound: self.freeze_sound.play()

    def start_bgm(self):
        safe_path = resource_path("trockey_bgm.mp3")
        try:
            pygame.mixer.music.load(safe_path)
            pygame.mixer.music.play(-1)
            if self.bgm_muted:
                pygame.mixer.music.pause()
        except pygame.error:
            print("BGM missing: Please add 'trockey_bgm.mp3' to your folder!")

    def toggle_bgm(self):
        self.bgm_muted = not self.bgm_muted
        if self.bgm_muted:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def stop_bgm(self):
        pygame.mixer.music.stop()