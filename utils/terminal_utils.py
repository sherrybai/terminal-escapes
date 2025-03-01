import sys
import shutil


def clear_screen():
    sys.stdout.write("\033[2J\033[H")


def get_terminal_size():
    """Gets the current terminal size."""
    try:
        columns, rows = shutil.get_terminal_size(
            fallback=(80, 24)
        )  # Default if detection fails
        return columns, rows
    except (AttributeError, OSError):  # Older systems or non-terminals
        return 80, 24  # Default values
