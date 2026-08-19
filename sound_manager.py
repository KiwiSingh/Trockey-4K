import os
import sys
import pygame #type: ignore

def resource_path(relative_path):
    """Get the absolute path to a resource, works for dev and for PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class SoundManager:
    def __init__(self):
        # Initialize the audio engine
        pygame.mixer.init()

        # Load Sound Effects using the safe path resolver
        self.bounce_wall = self._load_sound("bounce_wall.wav")
        self.bounce_paddle = self._load_sound("bounce_paddle.wav")
        self.freeze_sound = self._load_sound("freeze.wav")

    def _load_sound(self, filename):
        safe_path = resource_path(filename)
        try:
            return pygame.mixer.Sound(safe_path)
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
        safe_path = resource_path("trockey_bgm.mp3")
        try:
            pygame.mixer.music.load(safe_path)
            pygame.mixer.music.play(-1)
        except pygame.error:
            print("BGM placeholder missing: Please add 'trockey_bgm.mp3' to your folder!")

    def stop_bgm(self):
        pygame.mixer.music.stop()