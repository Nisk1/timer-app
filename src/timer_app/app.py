import customtkinter
from .audio_manager import AudioManager
from .timer_logic import TimerLogic
from .ui.timer_page import TimerPage
from .ui.settings_page import SettingsPage
from pathlib import Path
from .settings_manager import SettingsManager

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Timer")
        self.geometry("1280x720")

        settings_path = Path(__file__).resolve().parents[2] / "user_settings.json"
        self.settings_manager = SettingsManager(settings_path)

        appearance_mode = self.settings_manager.get("appearance_mode", "System")
        if appearance_mode not in ["Light", "Dark", "System"]:
            appearance_mode = "System"
        customtkinter.set_appearance_mode(appearance_mode)

        self.audio_manager = AudioManager(self, settings_manager=self.settings_manager)
        self.timer_logic = TimerLogic(
            on_tick=self.on_tick_update,
            on_finish=self.on_timer_finished
        )

        self.timer_page = TimerPage(self, self.audio_manager, self.timer_logic, self.show_settings)
        self.settings_page = SettingsPage(self, self.audio_manager, self.settings_manager, self.show_timer)
        self.timer_page.pack(expand=True, fill="both")

    def show_timer(self):
        self.settings_page.pack_forget()
        self.timer_page.pack(expand=True, fill="both")
        self.audio_manager.stop_alarm()

    def show_settings(self):
        self.timer_page.pack_forget()
        self.settings_page.pack(expand=True, fill="both")

    def on_tick_update(self, h, m, s):
        self.after(0, lambda: self.timer_page.update_display(h, m, s))
        
    def on_timer_finished(self):
        def handle_finish():
            self.audio_manager.play_alarm_loop()
            self.timer_page.timer_finished()
        self.after(0, handle_finish)

