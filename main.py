import argparse
import sys

from ascii_converter import AsciiConverter
from ascii_frame_renderer import AsciiFrameRenderer
from image_saver import ImageSaver
from image_source import ImageSource
from terminal_renderer import TerminalRenderer
from video_exporter import VideoExporter
from video_player import VideoPlayer
from video_saver import VideoSaver
from video_source import VideoSource


def positive_width(value):
    """Parse a strictly positive ASCII output width."""
    width = int(value)
    if width <= 0:
        raise argparse.ArgumentTypeError("width must be greater than zero")
    return width


def build_parser():
    """Build the command-line parser for all supported modes."""
    parser = argparse.ArgumentParser(
        description="Convert images and videos into ASCII art."
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)

    image_parser = subparsers.add_parser(
        "image", help="convert an image to terminal and text-file ASCII"
    )
    image_parser.add_argument(
        "path", nargs="?", default="images/test_car.jpg", help="input image path"
    )
    image_parser.add_argument("--width", type=positive_width, default=100)
    image_parser.add_argument("--output", default="output/output.txt")

    play_parser = subparsers.add_parser(
        "play-video", help="play a video as animated terminal ASCII"
    )
    play_parser.add_argument(
        "path", nargs="?", default="videos/5_sec_rule.mp4", help="input video path"
    )
    play_parser.add_argument("--width", type=positive_width, default=60)

    export_parser = subparsers.add_parser(
        "export-video", help="export a silent video containing rendered ASCII"
    )
    export_parser.add_argument(
        "path", nargs="?", default="videos/5_sec_rule.mp4", help="input video path"
    )
    export_parser.add_argument("--width", type=positive_width, default=60)
    export_parser.add_argument("--output", default="output/ascii_video.mp4")

    return parser


def run_image_mode(args):
    """Load, convert, print and save one static image."""
    image = ImageSource().load(args.path)
    if image is None:
        return False

    try:
        ascii_art = AsciiConverter().convert(image, args.width)
        print(ascii_art, end="")
        ImageSaver().save(ascii_art, args.output)
    finally:
        image.close()

    return True


def run_video_playback(args):
    """Create and run the terminal video playback pipeline."""
    player = VideoPlayer(VideoSource(), AsciiConverter(), TerminalRenderer())
    return player.play(args.path, args.width)


def run_video_export(args):
    """Create and run the ASCII MP4 export pipeline."""
    exporter = VideoExporter(
        VideoSource(),
        AsciiConverter(),
        AsciiFrameRenderer(),
        VideoSaver(),
    )
    return exporter.export(args.path, args.output, args.width)


def main():
    """Run the selected command and return a process status code."""
    args = build_parser().parse_args()

    try:
        if args.mode == "image":
            succeeded = run_image_mode(args)
        elif args.mode == "play-video":
            succeeded = run_video_playback(args)
        else:
            succeeded = run_video_export(args)
    except (OSError, RuntimeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0 if succeeded else 1


if __name__ == "__main__":
    raise SystemExit(main())
