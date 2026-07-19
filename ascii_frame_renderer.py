import cv2 as cv
import numpy as np


class AsciiFrameRenderer:
    """Render an ASCII character grid as an OpenCV BGR frame."""

    def __init__(
        self,
        font_scale=0.7,
        cell_width=9,
        line_height=14,
        margin=10,
        thickness=1,
    ):
        if font_scale <= 0:
            raise ValueError("font_scale must be greater than zero")
        if cell_width <= 0 or line_height <= 0:
            raise ValueError("character cell dimensions must be greater than zero")
        if margin < 0:
            raise ValueError("margin cannot be negative")
        if thickness <= 0:
            raise ValueError("thickness must be greater than zero")

        self.font_scale = font_scale
        self.cell_width = cell_width
        self.line_height = line_height
        self.margin = margin
        self.thickness = thickness
        self.font = cv.FONT_HERSHEY_PLAIN

    def _get_rows(self, ascii_art):
        """Return display rows without creating a trailing empty row."""
        rows = ascii_art.splitlines()
        return rows or [""]

    def get_frame_size(self, ascii_art):
        """Return the rendered frame size as an OpenCV (width, height) tuple."""
        rows = self._get_rows(ascii_art)
        column_count = max(1, max(len(row) for row in rows))
        row_count = max(1, len(rows))
        width = (2 * self.margin) + (column_count * self.cell_width)
        height = (2 * self.margin) + (row_count * self.line_height)
        return width, height

    def render(self, ascii_art):
        """Render ASCII text onto a black, fixed-cell BGR image."""
        rows = self._get_rows(ascii_art)
        width, height = self.get_frame_size(ascii_art)
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        baseline_offset = int(self.line_height * 0.8)

        for row_index, row in enumerate(rows):
            y_position = (
                self.margin
                + (row_index * self.line_height)
                + baseline_offset
            )

            for column_index, character in enumerate(row):
                if character == " ":
                    continue

                x_position = self.margin + (column_index * self.cell_width)
                cv.putText(
                    frame,
                    character,
                    (x_position, y_position),
                    self.font,
                    self.font_scale,
                    (255, 255, 255),
                    self.thickness,
                    cv.LINE_AA,
                )

        return frame
