import time
from multiprocessing import Process

from audio_manager import play_sound
from config_manager import save_config, WORK_PERIOD, REST_PERIOD
from inactivity_monitor import start_monitoring
from lunch_manager import lunch_checker
from menu import Menu


def start(config):
    work_hours = float(input("Enter the number of hours you want to work: "))
    total_seconds = int(work_hours * 3600)
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

    process = Process(target=start_monitoring, kwargs={'config': config})
    process.start()
    processes = [process, ]

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

                lunch_checker(config, processes)

            periods -= 1
            period_type = "rest" if period_type == "work" else "work"

        print("\nWork session completed!")
        config['total_seconds'] = 0
        save_config(config)

    except KeyboardInterrupt:
        print("\nTimer paused.")
        Menu().pause_menu(config, processes)


def format_time(seconds):
    hrs, secs = divmod(seconds, 3600)
    mins, secs = divmod(secs, 60)
    return f"{hrs:02}:{mins:02}:{secs:02}"
