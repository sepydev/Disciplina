# config_manager.py

import json
import os

CONFIG_FILE = 'config.json'
WORK_PERIOD = 30 * 60  # 30 minutes in seconds
REST_PERIOD = 5 * 60   # 5 minutes in seconds

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

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)


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
