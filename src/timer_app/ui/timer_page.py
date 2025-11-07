import customtkinter
import re
from datetime import datetime, timedelta

class TimerPage(customtkinter.CTkFrame):
    def __init__(self, parent, audio_manager, timer_logic, switch_to_settings):
        super().__init__(parent)
        self.audio_manager = audio_manager
        self.timer_logic = timer_logic
        self.switch_to_settings = switch_to_settings
        self._building = False
        self.configure(fg_color="transparent")

        self._build_ui()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _build_ui(self):
        self.timer_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.timer_frame.grid(row=0, column=0)
        self.timer_frame.grid_rowconfigure(3, weight=1)
        self.timer_frame.grid_columnconfigure(0, weight=1)

        self.time_var = customtkinter.StringVar()
        self.time_var.trace_add("write", self._on_time_change)

        self.time_entry = customtkinter.CTkEntry(
            self.timer_frame,
            width=600,
            textvariable=self.time_var,
            font=customtkinter.CTkFont(size=150, weight="bold"),
            fg_color="transparent",
            justify="center",
            text_color=("gray70", "gray70")
        )
        self.time_entry.grid(row=0, column=0, padx=20, pady=20, columnspan=2, sticky="n")
        self.time_var.set("00:00:00")

        self.time_entry.bind("<Return>", lambda event: self._toggle_timer())

        self.end_label_var = customtkinter.StringVar(value="")
        self.end_label = customtkinter.CTkLabel(
            self,
            textvariable=self.end_label_var,
            font=customtkinter.CTkFont(size=16),
            text_color=("gray50", "gray80")
        )
        self.end_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="n")

        self.start_button = customtkinter.CTkButton(
            self.timer_frame,
            height=40,
            corner_radius=10,
            border_spacing=10,
            fg_color="transparent",
            hover_color=("gray70", "gray30"),
            text_color=("gray10", "gray90"),
            text="Start",
            font=customtkinter.CTkFont(size=12, weight="bold"),
            command=self._toggle_timer
        )
        self.start_button.grid(row=1, column=0, padx=20, pady=10, columnspan=2)

        self.settings_button = customtkinter.CTkButton(
            self,
            height=40,
            corner_radius=10,
            border_spacing=10,
            fg_color="transparent",
            hover_color=("gray70", "gray30"),
            text_color=("gray10", "gray90"),
            text="Settings",
            font=customtkinter.CTkFont(size=12, weight="bold"),
            command=self.switch_to_settings
        )
        self.settings_button.grid(row=1, column=0, padx=20, pady=20, sticky="w")

    #----------Dynamic Formatting Handler----------
    def _on_time_change(self, *args):
        if self._building:
            return
        self._building = True

        entry = self.time_entry
        current_text = self.time_var.get()

        # Keep only digits and limit to 6 chars
        raw = re.sub(r"\D", "", current_text)
        raw = raw[:6]

        # Build formatted string HH:MM:SS
        parts = []
        if len(raw) > 0:
            parts.append(raw[:2])
        if len(raw) > 2:
            parts.append(raw[2:4])
        if len(raw) > 4:
            parts.append(raw[4:6])

        formatted = ":".join(parts)
        self.time_var.set(formatted)

        # Fix cursor jump
        cursor = self.time_entry.index("insert")
        if cursor in (3, 6):
            self.after(1, lambda c=cursor: entry.icursor(c + 1))

        self._building = False

    def _toggle_timer(self):
        if not self.timer_logic._is_running:
            if self.start_button.cget("text") == "Reset":
                self.time_var.set("00:00:00")
                self.start_button.configure(text="Start")
                self.time_entry.configure(
                    text_color=("gray30", "gray70"),
                    state="normal"
                )
                self.audio_manager.stop_alarm()
                self._clear_end_label()

            else:
                h, m, s = self._parse_time_entry()
                total_seconds = h * 3600 + m * 60 + s
                if total_seconds > 0:
                    end_dt = datetime.now() + timedelta(seconds=total_seconds)
                    self._set_end_label_for_datetime(end_dt)

                    self.timer_logic.start(total_seconds)
                    self.start_button.configure(text="Stop")
                    self.time_entry.configure(
                        text_color=("white", "white"),
                        state="disabled"
                    )
                    self.focus_set()
        else:
            self.timer_logic.stop()
            self.start_button.configure(text="Reset")
            self.time_entry.configure(
                text_color=("gray50", "gray70"),
                state="normal"
            )
            self._clear_end_label()

    # --- Time Parsing Helper ---
    def _parse_time_entry(self):
        text = self.time_var.get()
        try:
            parts = text.split(":")
            h = int(parts[0]) if len(parts) > 0 and parts[0] != "" else 0
            m = int(parts[1]) if len(parts) > 1 and parts[1] != "" else 0
            s = int(parts[2]) if len(parts) > 2 and parts[2] != "" else 0
            return h, m, s
        except Exception:
            return 0, 0, 0

    def update_display(self, h, m, s):
        self.time_var.set(f"{h:02}:{m:02}:{s:02}")
        self.audio_manager.play_tick()

        total_seconds = h * 3600 + m * 60 + s
        if total_seconds < 60:
            current_color = self.time_entry.cget("text_color")
            new_color = ("red", "red") if current_color != ("red", "red") else ("gray30", "white")
            self.time_entry.configure(text_color=new_color)
        else:
            self.time_entry.configure(text_color=("gray30", "white"))

    def timer_finished(self):
        """Called automatically when the timer ends."""
        self.timer_logic._is_running = False
        self.start_button.configure(text="Reset")
        self.time_entry.configure(state="normal", text_color=("gray30", "white"))
        finish_dt = datetime.now()
        self.end_label_var.set(f"Finished at {finish_dt.strftime('%H:%M:%S')}")

    def _set_end_label_for_datetime(self, dt: datetime):
        self.end_label_var.set(f"Ends at {dt.strftime('%H:%M:%S')}")

    def _clear_end_label(self):
        self.end_label_var.set("")
