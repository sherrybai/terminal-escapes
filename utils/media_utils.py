import os
import sys
import ffmpeg
from PIL import Image

SPACE_CHARS = "  "

def remove_extension(filepath):
    basename = os.path.basename(filepath)
    return os.path.splitext(basename)[0]

def extract_frames(filepath: str):
    frames_directory = f'./media/frames/{remove_extension(filepath)}'
    if not os.path.exists(frames_directory):
        os.makedirs(frames_directory)
        try:
            ffmpeg.input(filepath, ss=0, r=60) \
                        .output(f'{frames_directory}/frame-%04d.bmp', start_number=0) \
                        .overwrite_output() \
                        .run(capture_stdout=True, capture_stderr=True)
        except ffmpeg.Error as e:
            print('stdout:', e.stdout.decode('utf8'))
            print('stderr:', e.stderr.decode('utf8'))
            raise e
        
def bmp_to_pil(bmp_path, width, height):
    try:
        img = Image.open(bmp_path).convert("RGB")
        old_width, old_height = img.size
        scale_factor = min(width / (old_width * len(SPACE_CHARS)), height / old_height)
        new_size = (int(old_width * scale_factor), int(old_height * scale_factor))
        resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
        return resized_img
    except FileNotFoundError:
        print(f"Error: BMP file not found at {bmp_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def print_pixel(r, g, b):
    sys.stdout.write(f"\033[48;2;{r};{g};{b}m{SPACE_CHARS}\033[0m")

def display_pil_with_ansi_colors(image):
    width, height = image.size
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            print_pixel(r, g, b)
        sys.stdout.write("\n")