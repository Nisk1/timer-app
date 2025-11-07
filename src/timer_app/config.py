from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = ROOT_DIR / "assets"
AUDIO_DIR = ASSETS_DIR / "audio"

TICK_SOUND = AUDIO_DIR / "tick_sounds" / "DefaultTickSound.mp3"
ALARM_SOUND = AUDIO_DIR / "alarm_sounds" / "DefaultAlarmSound.mp3"
