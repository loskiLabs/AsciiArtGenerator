import math

import cv2 as cv
from PIL import Image


class VideoSource:
    """Open videos and return their frames as Pillow images."""

    def open_video(self, path):
        """Open a video file and return the video capture object."""
        video = cv.VideoCapture(path)

        if not video.isOpened():
            video.release()
            print(f"Error: Cannot open video at {path}")
            return None

        return video

    def read_frame(self, video):
        """Read and return the next video frame as a Pillow image."""
        success, frame = video.read()

        if not success:
            return None

        return self._convert_to_pillow(frame)

    def _convert_to_pillow(self, frame):
        """Converts an OpenCV BGR frame into a Pillow RGB image."""
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        return Image.fromarray(rgb_frame)

    def get_fps(self, video):
        """Return the video's frames per second."""
        fps = video.get(cv.CAP_PROP_FPS)

        if not math.isfinite(fps) or fps <= 0:
            return 30.0

        return fps

    def get_video_info(self, video):
        """Return useful metadata about the opened video."""
        width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(video.get(cv.CAP_PROP_FRAME_COUNT))
        fps = self.get_fps(video)

        return {
            "width": width,
            "height": height,
            "frame_count": frame_count,
            "fps": fps,
        }

    def close(self, video):
        """Release the video resource."""
        if video is not None:
            video.release()
