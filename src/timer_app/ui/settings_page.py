import customtkinter
from tkinter import filedialog, messagebox
from pathlib import Path
from ..config import AUDIO_DIR, TICK_SOUND, ALARM_SOUND
import threading


class SettingsPage(customtkinter.CTkFrame):
    def __init__(self, parent, audio_manager, settings_manager, switch_to_timer):
        super().__init__(parent)
        self.audio_manager = audio_manager
        self.settings_manager = settings_manager
        self.switch_to_timer = switch_to_timer
        self._build_ui()
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


    def _build_ui(self):
        self.settings_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.settings_frame.grid(row=0, column=1)
        self.settings_frame.grid_rowconfigure(9, weight=1)
        self.settings_frame.grid_columnconfigure(3, weight=1)

        self.tick_label = customtkinter.CTkLabel(
            self.settings_frame,
            text="Tick Sound Volume",
            corner_radius=10,
            font=customtkinter.CTkFont(size=12, weight="bold"),
            fg_color=("gray50", "gray30")
        )
        self.tick_label.grid(row=0, column=0, padx=20, pady=(20, 0), columnspan=2)

        self.tick_slider = customtkinter.CTkSlider(
            self.settings_frame, from_=0, to=1, command=self._set_tick_volume, border_width=5
        )
        self.tick_slider.grid(row=1, column=0, padx=20, pady=10, sticky="we")
        self.tick_slider.set(self.audio_manager.tick_volume)

        self.tick_test_button = customtkinter.CTkButton(
            self.settings_frame,
            height=40,
            text="Test",
            font=customtkinter.CTkFont(size=12, weight="bold"),
            fg_color=("gray70", "gray10"),
            hover_color=("gray50", "gray30"),
            text_color=("gray10", "gray90"),
            command=self._test_tick_sound
        )
        self.tick_test_button.grid(row=1, column=1, padx=20, pady=10)

        self.tick_select_button = customtkinter.CTkButton(
            self.settings_frame,
            text="Select Tick Sound",
            font=customtkinter.CTkFont(size=12, weight="bold"),
            command=self._select_tick_sound
        )
        self.tick_select_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="we")

        self.alarm_label = customtkinter.CTkLabel(
            self.settings_frame,
            text="Alarm Sound Volume",
            corner_radius=10,
            font=customtkinter.CTkFont(size=12, weight="bold"),
            fg_color=("gray50", "gray30")
        )
        self.alarm_label.grid(row=3, column=0, padx=20, pady=(30, 0), columnspan=2)

        self.alarm_slider = customtkinter.CTkSlider(
            self.settings_frame, from_=0, to=1, command=self._set_alarm_volume, border_width=5
        )
        self.alarm_slider.grid(row=4, column=0, padx=20, pady=10, sticky="we")
        self.alarm_slider.set(self.audio_manager.alarm_volume)

        self.alarm_test_button = customtkinter.CTkButton(
            self.settings_frame,
            height=40,
            text="Test",
            font=customtkinter.CTkFont(size=12, weight="bold"),
            fg_color=("gray70", "gray10"),
            hover_color=("gray50", "gray30"),
            text_color=("gray10", "gray90"),
            command=self._test_alarm_sound
        )
        self.alarm_test_button.grid(row=4, column=1, padx=20, pady=10)

        self.alarm_select_button = customtkinter.CTkButton(
            self.settings_frame,
            text="Select Alarm Sound",
            font=customtkinter.CTkFont(size=12, weight="bold"),
            command=self._select_alarm_sound
        )
        self.alarm_select_button.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="we")

        self.appearance_option = customtkinter.CTkOptionMenu(
            self,
            values=["Light", "Dark", "System"],
            command=self._change_appearance_mode,
            font=customtkinter.CTkFont(size=12, weight="bold")
        )
        self.appearance_option.grid(row=1, column=2, padx=20, pady=20, columnspan=2, sticky="e")

        current_mode = self.settings_manager.get("appearance_mode", "System")
        if current_mode not in ["Light", "Dark", "System"]:
            current_mode = "System"
        self.appearance_option.set(current_mode)
        
        self.reset_button = customtkinter.CTkButton(
            self.settings_frame,
            text="Reset to Default Settings",
            font=customtkinter.CTkFont(size=12, weight="bold"),
            fg_color=("gray50", "gray30"),
            hover_color=("red", "red"),
            command=self._reset_to_defaults
        )
        self.reset_button.grid(row=8, column=0, columnspan=2, padx=20, pady=(30, 10))

        self.back_button = customtkinter.CTkButton(
            self,
            height=40,
            corner_radius=10,
            border_spacing=10,
            text="Back to Timer",
            font=customtkinter.CTkFont(size=12, weight="bold"),
            fg_color="transparent",
            hover_color=("gray70", "gray30"),
            text_color=("gray10", "gray90"),
            command=self.switch_to_timer
        )
        self.back_button.grid(row=1, column=0, padx=20, pady=20, sticky="w")

    def _set_tick_volume(self, value):
        self.audio_manager.set_tick_volume(value)
        self.settings_manager.set("tick_volume", value)
        self.settings_manager.save()

    def _set_alarm_volume(self, value):
        self.audio_manager.set_alarm_volume(value)
        self.settings_manager.set("alarm_volume", value)
        self.settings_manager.save()

    def _test_tick_sound(self):
        self.audio_manager.play_tick()
        threading.Timer(1.0, self.audio_manager.stop_tick).start()

    def _test_alarm_sound(self):
        self.audio_manager.play_alarm()
        threading.Timer(1.0, self.audio_manager.stop_alarm).start()

    def _select_tick_sound(self):
        initial_dir = (AUDIO_DIR / "tick_sounds").resolve()
        file_path = filedialog.askopenfilename(
            title="Select Tick Sound",
            initialdir=initial_dir,
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                self.audio_manager.change_tick_sound(file_path)
                self.settings_manager.set("tick_sound_path", str(Path(file_path).resolve()))
                self.settings_manager.save()
                messagebox.showinfo("Tick Sound Changed", f"Tick sound set to:\n{Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load tick sound:\n{e}")

    def _select_alarm_sound(self):
        initial_dir = (AUDIO_DIR / "alarm_sounds").resolve()
        file_path = filedialog.askopenfilename(
            title="Select Alarm Sound",
            initialdir=initial_dir,
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                self.audio_manager.change_alarm_sound(file_path)
                self.settings_manager.set("alarm_sound_path", str(Path(file_path).resolve()))
                self.settings_manager.save()
                messagebox.showinfo("Alarm Sound Changed", f"Alarm sound set to:\n{Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load alarm sound:\n{e}")

    def _change_appearance_mode(self, mode):
        """Update and save appearance mode globally."""
        if mode not in ["Light", "Dark", "System"]:
            mode = "System"
        customtkinter.set_appearance_mode(mode)
        self.settings_manager.set("appearance_mode", mode)

    def _reset_to_defaults(self):
        if messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to defaults?"):
            self.settings_manager.clear()
            self.settings_manager.save()

            default_tick_volume = 0.5
            default_alarm_volume = 0.5
            self.audio_manager.tick_volume = default_tick_volume
            self.audio_manager.alarm_volume = default_alarm_volume
            self.audio_manager._apply_volume()

            from ..config import TICK_SOUND, ALARM_SOUND
            self.audio_manager.change_tick_sound(TICK_SOUND)
            self.audio_manager.change_alarm_sound(ALARM_SOUND)

            self.tick_slider.set(default_tick_volume)
            self.alarm_slider.set(default_alarm_volume)

            self.appearance_option.set("System")
            customtkinter.set_appearance_mode("System")
            self.settings_manager.set("appearance_mode", "System")

            messagebox.showinfo("Settings Reset", "Settings have been reset to defaults.")
