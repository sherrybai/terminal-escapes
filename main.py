import sys
import signal

from utils.media_utils import bmp_to_pil, extract_frames, display_pil_with_ansi_colors
from utils.terminal_utils import clear_screen, get_terminal_size

DEFAULT_VIDEO_PATH = "./media/gentle_waves_at_sunrise.mp4"

def handle_resize(signum, frame):
    """Handles terminal resize signals."""
    global terminal_width, terminal_height
    terminal_width, terminal_height = get_terminal_size()

    # Re-render your output here based on the new dimensions
    redraw_content()

def redraw_content():
    """Example function to redraw content based on terminal size."""
    global terminal_width, terminal_height
    clear_screen()
    
    # display the photo with spaces of different background colors
    bmp_path = "./media/frames/gentle_waves_at_sunrise/frame-0000.bmp"
    image = bmp_to_pil(bmp_path, terminal_width, terminal_height)
    display_pil_with_ansi_colors(image)
    

if __name__ == "__main__":
    video_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_VIDEO_PATH
    # read the mp4 file from media directory
    extract_frames(video_path)

    terminal_width, terminal_height = get_terminal_size()

    # Register the signal handler for terminal resize
    signal.signal(signal.SIGWINCH, handle_resize) #SIGWINCH is the signal sent when the terminal is resized.
    redraw_content()

    # Keep the program running to receive resize signals
    while True:
        try:
            pass
        except KeyboardInterrupt:
            break
