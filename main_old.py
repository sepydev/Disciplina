import json
import os
import sys
import time
from datetime import datetime

from pydub import AudioSegment
import simpleaudio as sa

CONFIG_FILE = 'config.json'
WORK_PERIOD = 30 * 60  # 30 minutes in seconds
REST_PERIOD = 5 * 60  # 5 minutes in seconds
SOUND_FILE = 'notification.mp3'

# Define time ranges for different messages in milliseconds
AUDIO_SEGMENTS = {
    'START_WORK_MESSAGE': {'start': 15000, 'end': 16300},
    'START_REST_MESSAGE': {'start': 16300, 'end': 19800},
    'LUNCH_MESSAGE': {'start': 20000, 'end': 23000},
    # Add more as needed
}


# Load configuration from file
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    else:
        return {
            "lunch_time": "",
            "check_internet": False,
            "check_proxy": False,
            "idle_alert": False,
            "idle_alert_level_1": 0,
            "idle_alert_level_2": 0,
            "total_seconds": 0,
            "total_time_elapsed": 0,
            "periods": 0,
            "period_type": "work",
        }


# Save configuration to file
def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)


def play_sound(segment_name):
    if segment_name in AUDIO_SEGMENTS:
        start_ms = AUDIO_SEGMENTS[segment_name]['start']
        end_ms = AUDIO_SEGMENTS[segment_name]['end']
        audio = AudioSegment.from_mp3(SOUND_FILE)
        segment = audio[start_ms:end_ms]
        play_obj = sa.play_buffer(segment.raw_data, num_channels=segment.channels,
                                  bytes_per_sample=segment.sample_width,
                                  sample_rate=segment.frame_rate)
        play_obj.wait_done()


def main_menu(config):
    while True:
        print("\nMain Menu")
        print("[1] Start")
        print("[2] Config")
        print("[0] Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            if config['total_seconds'] == 0:
                start(config)
            else:
                resume(config)
        elif choice == '2':
            config_menu(config)
        elif choice == '0':
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")


def start(config):
    work_hours = int(input("Enter the number of hours you want to work: "))
    total_seconds = work_hours * 3600
    config['total_seconds'] = total_seconds
    config['total_time_elapsed'] = 0
    config['periods'] = total_seconds // (WORK_PERIOD + REST_PERIOD)
    config['period_type'] = "work"
    save_config(config)
    work_timer(config)


def resume(config):
    work_timer(config)


def work_timer(config):
    total_seconds = config['total_seconds']
    total_time_elapsed = config['total_time_elapsed']
    periods = config['periods']
    period_type = config['period_type']

    try:
        while total_seconds > 0:
            period_time = WORK_PERIOD if period_type == "work" else REST_PERIOD
            period_elapsed = 0

            if period_type == "work":
                play_sound('START_WORK_MESSAGE')  # Play start work sound
            else:
                play_sound('START_REST_MESSAGE')  # Play start rest sound

            while period_elapsed < period_time and total_seconds > 0:
                time.sleep(1)
                total_time_elapsed += 1
                period_elapsed += 1
                total_seconds -= 1

                # Check for lunch time
                if config['lunch_time'] and is_lunch_time(config['lunch_time']):
                    play_sound('LUNCH_MESSAGE')  # Play lunch message sound

                total_time_str = format_time(total_time_elapsed)
                period_time_str = format_time(period_elapsed)
                period_left_str = format_time(period_time - period_elapsed)
                print(
                    f"\rTotal time: {total_time_str} | Period timer: {period_time_str} | Left: {period_left_str} | Period type: {period_type} | Periods left: {periods}",
                    end="")

                config['total_seconds'] = total_seconds
                config['total_time_elapsed'] = total_time_elapsed
                config['periods'] = periods
                config['period_type'] = period_type
                save_config(config)

            periods -= 1
            period_type = "rest" if period_type == "work" else "work"

        print("\nWork session completed!")
        config['total_seconds'] = 0  # Reset total seconds after completion
        save_config(config)

    except KeyboardInterrupt:
        print("\nTimer paused.")
        pause_menu(config)


def pause_menu(config):
    while True:
        print("\nPause Menu")
        print("[1] Resume")
        print("[2] Go to main menu")
        print("[3] Stop and go to main menu")
        choice = input("Choose an option: ")

        if choice == '1':
            work_timer(config)
            break
        elif choice == '2':
            main_menu(config)
            break
        elif choice == '3':
            config['total_seconds'] = 0  # Reset total seconds when stopped
            save_config(config)
            main_menu(config)
            break
        else:
            print("Invalid choice. Please try again.")


def format_time(seconds):
    hrs, secs = divmod(seconds, 3600)
    mins, secs = divmod(secs, 60)
    return f"{hrs:02}:{mins:02}:{secs:02}"


def config_menu(config):
    while True:
        print("\nConfig Menu")
        print("[1] Set lunch time")
        print("[2] Activate/Deactivate check internet connection")
        print("[3] Activate/Deactivate check proxy connection")
        print("[4] Activate/Deactivate idle alert")
        print("[5] Config idle alert")
        print("[0] Back to main menu")
        choice = input("Choose an option: ")

        if choice == '1':
            set_lunch_time(config)
        elif choice == '2':
            toggle_check(config, "check_internet")
        elif choice == '3':
            toggle_check(config, "check_proxy")
        elif choice == '4':
            toggle_check(config, "idle_alert")
        elif choice == '5':
            idle_alert_config_menu(config)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

        save_config(config)


def set_lunch_time(config):
    lunch_time = input("Enter lunch time (HH:MM): ")
    config['lunch_time'] = lunch_time
    print(f"Lunch time set to {lunch_time}")


def toggle_check(config, option):
    status = input(f"Do you want to activate or deactivate the {option.replace('_', ' ')}? (a/d): ")
    if status.lower() == 'a':
        config[option] = True
        print(f"{option.replace('_', ' ').capitalize()} activated.")
    elif status.lower() == 'd':
        config[option] = False
        print(f"{option.replace('_', ' ').capitalize()} deactivated.")
    else:
        print("Invalid choice. Please enter 'a' to activate or 'd' to deactivate.")


def idle_alert_config_menu(config):
    while True:
        print("\nIdle Alert Config Menu")
        print("[1] Set time level 1 in seconds (warn after x seconds)")
        print("[2] Set time level 2 in seconds (0 to disable)")
        print("[0] Back to config menu")
        choice = input("Choose an option: ")

        if choice == '1':
            set_time_level(config, 1)
        elif choice == '2':
            set_time_level(config, 2)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

        save_config(config)


def set_time_level(config, level):
    time = int(input(f"Enter time level {level} in seconds: "))
    if level == 1:
        config['idle_alert_level_1'] = time
        print(f"Time level 1 set to {time} seconds.")
    elif level == 2:
        config['idle_alert_level_2'] = time
        print(f"Time level 2 set to {time} seconds.")


# Function to check if current time matches lunch time
def is_lunch_time(lunch_time):
    current_time = datetime.now().strftime("%H:%M")
    return current_time == lunch_time

if __name__ == "__main__":
    config = load_config()
    main_menu(config)
