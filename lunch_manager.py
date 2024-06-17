# lunch_manager.py
import time
from datetime import datetime, timedelta

from audio_manager import play_sound
from config_manager import save_config
from menu import Menu


def lunch_notification_menu():
    while True:
        print("\nLunch Time Notification")
        print("[1] Accept lunch time")
        print("[2] Postpone lunch time")
        choice = input("Choose an option: ")

        if choice == '1':
            return True
        elif choice == '2':
            return False
        else:
            print("Invalid choice. Please try again.")


def is_lunch_time(lunch_time):
    current_time = datetime.now().strftime("%H:%M")
    return current_time == lunch_time


def lunch_notification_menu():
    while True:
        print("\nLunch Time Notification")
        print("[1] Accept lunch time")
        print("[2] Postpone lunch time")
        choice = input("Choose an option: ")

        if choice == '1':
            return True
        elif choice == '2':
            return False
        else:
            print("Invalid choice. Please try again.")


def postpone_lunch(config):
    postpone_minutes = int(input("Enter postponement time in minutes: "))
    new_lunch_time = (datetime.now() + timedelta(minutes=postpone_minutes)).strftime("%H:%M")
    config['lunch_time'] = new_lunch_time
    print(f"Lunch time postponed. New lunch time set to {new_lunch_time}")
    save_config(config)


def check_end_of_lunch_time(config, processes):
    lunch_time = datetime.strptime(config['lunch_time'], "%H:%M")
    end_lunch = (lunch_time + timedelta(minutes=config["lunch_duration"])).strftime("%H:%M")
    while True:
        time.sleep(1)
        if is_lunch_time(end_lunch):
            play_sound('LUNCH_OVER_MESSAGE')
            print("\nLunch time is over!")
            break
        print(
            f"\rLunch duration: {config['lunch_duration']} minutes | End lunch time: {end_lunch} | Current time: {datetime.now().strftime('%H:%M:%S')}",
            end="")
    Menu().pause_menu(config, processes)


def lunch_checker(config, processes):
    if config['lunch_time'] and is_lunch_time(config['lunch_time']):
        play_sound('LUNCH_MESSAGE')

        if lunch_notification_menu():
            check_end_of_lunch_time(config, processes)
        else:
            postpone_lunch(config)
