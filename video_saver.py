import math
from pathlib import Path

import cv2 as cv


class VideoSaver:
    """Encode consistently sized BGR frames as an MP4 video."""

    def __init__(self):
        self._writer = None
        self._frame_size = None

    def open(self, filename, fps, frame_size):
        """Open an MP4 writer for frames of the supplied size."""
        if not math.isfinite(fps) or fps <= 0:
            raise ValueError("fps must be a positive, finite number")
        if len(frame_size) != 2:
            raise ValueError("frame_size must contain width and height")

        width, height = frame_size
        if not isinstance(width, int) or not isinstance(height, int):
            raise ValueError("frame dimensions must be integers")
        if width <= 0 or height <= 0:
            raise ValueError("frame dimensions must be greater than zero")
        if self._writer is not None:
            raise RuntimeError("Video writer is already open.")

        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fourcc = cv.VideoWriter_fourcc(*"mp4v")

        self._writer = cv.VideoWriter(
            str(output_path),
            fourcc,
            fps,
            (width, height),
        )

        if not self._writer.isOpened():
            self._writer.release()
            self._writer = None
            raise RuntimeError(f"Could not create video file: {output_path}")

        self._frame_size = (width, height)

    def write_frame(self, frame):
        """Write one BGR frame after validating its dimensions."""
        if self._writer is None:
            raise RuntimeError("Video writer has not been opened.")
        if frame.ndim != 3 or frame.shape[2] != 3:
            raise ValueError("frame must be a three-channel BGR image")

        height, width = frame.shape[:2]
        if (width, height) != self._frame_size:
            raise ValueError(
                "frame size does not match the configured writer size: "
                f"expected {self._frame_size}, got {(width, height)}"
            )

        self._writer.write(frame)

    def close(self):
        """Release the video writer and reset its state."""
        if self._writer is not None:
            self._writer.release()
            self._writer = None

        self._frame_size = None

