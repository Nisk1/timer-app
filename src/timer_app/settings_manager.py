from pathlib import Path
import json

DEFAULT_SETTINGS = {
    "tick_volume": 0.5,
    "alarm_volume": 0.5,
    "tick_sound_path": None,
    "alarm_sound_path": None,
    "appearance_mode": "System"
}

class SettingsManager:
    def __init__(self, settings_path):
        self.settings_path = settings_path
        self.settings = {}
        self.load()
        self._ensure_defaults()

    def load(self):
        if self.settings_path.exists():
            try:
                with open(self.settings_path, "r") as f:
                    self.settings = json.load(f)
            except Exception:
                self.settings = {}
        else:
            self.settings = {}

    def save(self):
        try:
            with open(self.settings_path, "w") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Failed to save settings: {e}")

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save()
    
    def clear(self):
        self.settings = DEFAULT_SETTINGS.copy()
        self.save()

    def _ensure_defaults(self):
        changed = False
        for k, v in DEFAULT_SETTINGS.items():
            if k not in self.settings:
                self.settings[k] = v
                changed = True
        if changed:
            self.save()
