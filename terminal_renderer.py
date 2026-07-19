import sys


class TerminalRenderer:
    """Display changing ASCII frames in an ANSI-compatible terminal."""

    def clear(self):
        """Clear the terminal and place the cursor at the top-left."""
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

    def render(self, ascii_art):
        """Draw one ASCII frame from the terminal's top-left corner."""
        sys.stdout.write("\033[H")
        sys.stdout.write(ascii_art)
        sys.stdout.write("\033[J")
        sys.stdout.flush()

    def hide_cursor(self):
        """Hide the terminal cursor."""
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    def show_cursor(self):
        """Restore the terminal cursor."""
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
