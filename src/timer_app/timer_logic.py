import time
import threading

class TimerLogic:
    def __init__(self, on_tick=None, on_finish=None):
        self.on_tick = on_tick or (lambda h, m, s: None)
        self.on_finish = on_finish or (lambda: None)
        self._is_running = False
        self._thread = None

    def start(self, total_seconds):
        if self._is_running:
            return
        self._is_running = True
        self._thread = threading.Thread(target=self._run, args=(total_seconds,), daemon=True)
        self._thread.start()

    def stop(self):
        self._is_running = False

    def _run(self, total_seconds):
        for remaining in range(total_seconds, -1, -1):
            if not self._is_running:
                break
            hours, remainder = divmod(remaining, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.on_tick(hours, minutes, seconds)
            time.sleep(1)
        if self._is_running:
            self.on_finish()
        self._is_running = False
