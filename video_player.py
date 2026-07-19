import time


class VideoPlayer:
    """Coordinate full-video ASCII playback in the terminal."""

    def __init__(self, video_source, ascii_converter, terminal_renderer):
        self.video_source = video_source
        self.ascii_converter = ascii_converter
        self.terminal_renderer = terminal_renderer

    def play(self, path, width=60):
        """Play every available video frame as timed terminal ASCII."""
        video = self.video_source.open_video(path)
        if video is None:
            return False

        interrupted = False

        try:
            fps = self.video_source.get_fps(video)
            frame_duration = 1 / fps
            self.terminal_renderer.hide_cursor()
            self.terminal_renderer.clear()

            while True:
                frame_start = time.perf_counter()
                frame = self.video_source.read_frame(video)

                if frame is None:
                    break

                try:
                    ascii_art = self.ascii_converter.convert(frame, width)
                finally:
                    frame.close()

                self.terminal_renderer.render(ascii_art)
                processing_time = time.perf_counter() - frame_start
                remaining_time = frame_duration - processing_time

                if remaining_time > 0:
                    time.sleep(remaining_time)
        except KeyboardInterrupt:
            interrupted = True
        finally:
            try:
                self.video_source.close(video)
            finally:
                self.terminal_renderer.show_cursor()

        if interrupted:
            print("\nPlayback stopped.")

        return True
