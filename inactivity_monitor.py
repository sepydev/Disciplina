# inactivity_monitor.py
from multiprocessing import Process

from pynput import mouse, keyboard
from datetime import datetime, timedelta
import time

from audio_manager import play_sound


class InactivityMonitor:
    def __init__(self, timeout_seconds, idle_alert_callback):
        self.timeout_seconds = timeout_seconds
        self.idle_alert_callback = idle_alert_callback
        self.last_active = datetime.now()
        self.running = True

        # Set up listeners
        self.mouse_listener = mouse.Listener(on_move=self.on_activity, on_click=self.on_activity, on_scroll=self.on_activity)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_activity)

    def on_activity(self, *args):
        self.last_active = datetime.now()

    def start(self):
        self.mouse_listener.start()
        self.keyboard_listener.start()

        while self.running:
            if (datetime.now() - self.last_active) > timedelta(seconds=self.timeout_seconds):
                self.idle_alert_callback()
                self.last_active = datetime.now()  # Reset the last active time after the alert
            time.sleep(1)

    def stop(self):
        self.running = False
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        self.process.terminate()

def start_monitoring(config):
    idle_alert_level_1 = config['idle_alert_level_1']
    inactivity_monitor = InactivityMonitor(idle_alert_level_1, on_idle_alert_level_1)
    inactivity_monitor.start()


def on_idle_alert_level_1():
    play_sound("IDLE_ALERT_LEVEL_1")