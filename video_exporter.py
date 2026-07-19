class VideoExporter:
    """Coordinate conversion of a complete video into an ASCII MP4."""

    def __init__(
        self,
        video_source,
        ascii_converter,
        ascii_frame_renderer,
        video_saver,
    ):
        self.video_source = video_source
        self.ascii_converter = ascii_converter
        self.ascii_frame_renderer = ascii_frame_renderer
        self.video_saver = video_saver

    def _convert_frame(self, frame, width):
        """Convert one Pillow frame to a rendered BGR frame."""
        try:
            ascii_art = self.ascii_converter.convert(frame, width)
        finally:
            frame.close()

        return self.ascii_frame_renderer.render(ascii_art)

    def export(self, input_path, output_path, width=60):
        """Export all source frames, including the first, to a silent MP4."""
        video = self.video_source.open_video(input_path)
        if video is None:
            return False

        frame_count = 0

        try:
            fps = self.video_source.get_fps(video)
            first_frame = self.video_source.read_frame(video)

            if first_frame is None:
                print(f"Error: No readable frames found in '{input_path}'.")
                return False

            rendered_frame = self._convert_frame(first_frame, width)
            frame_size = (rendered_frame.shape[1], rendered_frame.shape[0])
            self.video_saver.open(output_path, fps, frame_size)
            self.video_saver.write_frame(rendered_frame)
            frame_count = 1

            while True:
                frame = self.video_source.read_frame(video)
                if frame is None:
                    break

                rendered_frame = self._convert_frame(frame, width)
                self.video_saver.write_frame(rendered_frame)
                frame_count += 1
        finally:
            try:
                self.video_source.close(video)
            finally:
                self.video_saver.close()

        print(f"ASCII video saved to {output_path} ({frame_count} frames).")
        return True
