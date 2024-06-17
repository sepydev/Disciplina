from pydub import AudioSegment
import simpleaudio as sa

SOUND_FILE = 'notification.mp3'

AUDIO_SEGMENTS = {
    'START_WORK_MESSAGE': {'start': 15000, 'end': 16300},
    'START_REST_MESSAGE': {'start': 16300, 'end': 19800},
    'LUNCH_MESSAGE': {'start': 20000, 'end': 23000},
    'LUNCH_OVER_MESSAGE': {'start': 23000, 'end': 28000},
    'IDLE_ALERT_LEVEL_1': {'start': 6300, 'end': 9000},
    'IDLE_ALERT_LEVEL_2': {'start': 9100, 'end': 12000},
}

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
