import sys
import signal
import threading
import time

from utils.media_utils import bmp_to_pil, extract_frames, pil_to_ansi_string
from utils.terminal_utils import clear_screen, get_terminal_size

DEFAULT_VIDEO_PATH = "./media/gentle_waves_at_sunrise.mp4"


def increment_counter():
    global counter, num_frames
    for _ in range(num_frames):
        counter += 1
        redraw_content()
        time.sleep(0.1)


def handle_resize(signum, frame):
    """Handles terminal resize signals."""
    global terminal_width, terminal_height
    terminal_width, terminal_height = get_terminal_size()

    # Re-render your output here based on the new dimensions
    redraw_content()


def redraw_content():
    """Example function to redraw content based on terminal size."""
    global terminal_width, terminal_height, counter
    clear_screen()

    # display the photo with spaces of different background colors
    bmp_path = f"./media/frames/gentle_waves_at_sunrise/frame-{counter:04}.bmp"
    image = bmp_to_pil(bmp_path, terminal_width, terminal_height)
    print(pil_to_ansi_string(image))


if __name__ == "__main__":
    terminal_width, terminal_height = get_terminal_size()

    video_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_VIDEO_PATH
    # read the mp4 file from media directory
    num_frames = extract_frames(video_path)

    # Register the signal handler for terminal resize
    signal.signal(
        signal.SIGWINCH, handle_resize
    )  # SIGWINCH is the signal sent when the terminal is resized.

    # Start a thread to increment the global counter
    counter = 0
    counter_thread = threading.Thread(target=increment_counter)
    counter_thread.daemon = True
    counter_thread.start()
    redraw_content()

    # Keep the program running to receive resize signals
    while True:
        try:
            pass
        except KeyboardInterrupt:
            break
