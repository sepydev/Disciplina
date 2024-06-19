import sys

from config_manager import save_config, set_lunch_time, toggle_check, idle_alert_config_menu


class Menu:
    def main_menu(self, config):
        from work_timer import start, resume
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
                self.config_menu(config)
            elif choice == '0':
                print("Exiting...")
                sys.exit()
            else:
                print("Invalid choice. Please try again.")


    def pause_menu(self, config):
        while True:
            print("\nPause Menu")
            print("[1] Resume")
            print("[2] Go to main menu")
            print("[3] Stop and go to main menu")
            choice = input("Choose an option: ")

            if choice == '1':
                resume(config)
                break
            elif choice == '2':
                self.main_menu(config)
                break
            elif choice == '3':
                config['total_seconds'] = 0
                save_config(config)
                self.main_menu(config)
                break
            else:
                print("Invalid choice. Please try again.")

    def config_menu(self,config):
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
                config['total_seconds'] = 0  # Reset total seconds when stopped
                save_config(config)
                sys.exit()
            else:
                print("Invalid choice. Please try again.")

            save_config(config)



