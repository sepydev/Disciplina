from audio_manager import play_sound
from config_manager import load_config
from menu import Menu

if __name__ == "__main__":
    config = load_config()
    Menu().main_menu(config)
