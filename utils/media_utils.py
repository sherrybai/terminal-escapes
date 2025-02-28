import os
import ffmpeg

def remove_extension(filepath):
    return os.path.splitext(filepath)[0]

def extract_frames(filepath: str):
    frames_directory = f'../media/frames/{remove_extension(filepath)}'
    if not os.path.exists(frames_directory):
        ffmpeg.input(filepath, ss=0, r=1) \
            .filter('fps', fps='1/60') \
            .output(f'{frames_directory}/frame-%d.jpg', start_number=0) \
            .overwrite_output() \
            .run(quiet=True)