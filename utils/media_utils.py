import os
import ffmpeg
from PIL import Image

from utils.file_utils import remove_extension, num_bmp_files_in_directory

SPACE_CHARS = "  "


def extract_frames(filepath: str):
    frames_directory = f"./media/frames/{remove_extension(filepath)}"
    if not os.path.exists(frames_directory):
        os.makedirs(frames_directory)
        try:
            ffmpeg.input(filepath, ss=0, r=60).output(
                f"{frames_directory}/frame-%04d.bmp", start_number=0
            ).overwrite_output().run(capture_stdout=True, capture_stderr=True)
        except ffmpeg.Error as e:
            print("stdout:", e.stdout.decode("utf8"))
            print("stderr:", e.stderr.decode("utf8"))
            raise e
        # return number of files in directory
    return num_bmp_files_in_directory(frames_directory)


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


def pixel_to_ansi_color(r, g, b):
    return f"\033[48;2;{r};{g};{b}m{SPACE_CHARS}"


def pil_to_ansi_string(image):
    img_rows = []
    width, height = image.size
    for y in range(height):
        row = ""
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            row += pixel_to_ansi_color(r, g, b)
        img_rows.append(row)
    return "\n".join(img_rows) + "\033[0m"
