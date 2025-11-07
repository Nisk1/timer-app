from .config import TICK_SOUND, ALARM_SOUND
import pygame
from pathlib import Path

class AudioManager:
    def __init__(self, root, settings_manager=None):
        pygame.mixer.init()
        self.root = root
        self.settings = settings_manager

        self.tick_volume = 0.5
        self.alarm_volume = 0.5

        tick_path_str = self.settings.get("tick_sound_path") if self.settings else None
        alarm_path_str = self.settings.get("alarm_sound_path") if self.settings else None

        tick_path = Path(tick_path_str) if tick_path_str and Path(tick_path_str).exists() else TICK_SOUND
        alarm_path = Path(alarm_path_str) if alarm_path_str and Path(alarm_path_str).exists() else ALARM_SOUND

        self.tick_sound = pygame.mixer.Sound(str(tick_path))
        self.alarm_sound = pygame.mixer.Sound(str(alarm_path))

        self.tick_volume = self.settings.get("tick_volume", 0.5) if self.settings else 0.5
        self.alarm_volume = self.settings.get("alarm_volume", 0.5) if self.settings else 0.5

        self._apply_volume()

        self.tick_channel = None
        self.alarm_channel = None

        self._tick_stop_after_id = None

    def _apply_volume(self):
        self.tick_sound.set_volume(self.tick_volume)
        self.alarm_sound.set_volume(self.alarm_volume)

    def _load_sound(self, path, is_tick=True):
        sound = pygame.mixer.Sound(str(path))
        volume = self.tick_volume if is_tick else self.alarm_volume
        sound.set_volume(volume)
        return sound

    def set_tick_volume(self, value):
        self.tick_volume = value
        self.tick_sound.set_volume(value)
        if self.settings:
            self.settings.set("tick_volume", value)

    def set_alarm_volume(self, value):
        self.alarm_volume = value
        self.alarm_sound.set_volume(value)
        if self.settings:
            self.settings.set("alarm_volume", value)

    def play_tick(self):
        if self._tick_stop_after_id is not None:
            self.root.after_cancel(self._tick_stop_after_id)
            self._tick_stop_after_id = None

        if self.tick_channel is None or not self.tick_channel.get_busy():
            self.tick_channel = self.tick_sound.play()
        else:
            self.tick_channel.stop()
            self.tick_channel = self.tick_sound.play()

        def stop_tick():
            if self.tick_channel:
                self.tick_channel.fadeout(300)
                self.tick_channel = None
            self._tick_stop_after_id = None

        self._tick_stop_after_id = self.root.after(1000, stop_tick)

    def play_alarm(self):
        if self.alarm_channel is None or not self.alarm_channel.get_busy():
            self.alarm_channel = self.alarm_sound.play()

    def play_alarm_loop(self):
        if self.alarm_channel is None or not self.alarm_channel.get_busy():
            self.alarm_channel = self.alarm_sound.play(loops=-1)

    def stop_alarm(self):
        if self.alarm_channel:
            self.alarm_channel.stop()
            self.alarm_channel = None

    def change_tick_sound(self, file_path):
        self.tick_sound = self._load_sound(file_path, is_tick=True)
        if self.settings:
            default_path = str(TICK_SOUND.resolve())
            new_path = str(Path(file_path).resolve())
            if new_path != default_path:
                self.settings.set("tick_sound_path", new_path)
            else:
                self.settings.set("tick_sound_path", None)
        self.tick_channel = None

    def change_alarm_sound(self, file_path):
        self.alarm_sound = self._load_sound(file_path, is_tick=False)
        if self.settings:
            default_path = str(ALARM_SOUND.resolve())
            new_path = str(Path(file_path).resolve())
            if new_path != default_path:
                self.settings.set("alarm_sound_path", new_path)
            else:
                self.settings.set("alarm_sound_path", None)
        self.alarm_channel = None
        
    def stop_tick(self):
        if self.tick_channel:
            self.tick_channel.stop()
            self.tick_channel = None
