# ASCII Art Generator

A Python program that converts images and videos into ASCII art. It can print
and save a static image as text, play a video as animated ASCII in the terminal,
or export a video whose frames contain rendered ASCII characters.

## Features

- Convert a Pillow image into ASCII using pixel brightness.
- Print static ASCII art in the terminal and save it as a UTF-8 text file.
- Play every frame of a video as animated terminal ASCII.
- Export an entire video as a new MP4 containing white ASCII characters on a
  black background.
- Keep image loading, conversion, rendering, playback and saving in separate
  classes.

## Requirements

- Python 3
- Pillow
- OpenCV
- NumPy

Install the dependencies from the project folder:

```powershell
py -m pip install -r requirements.txt
```

If the `py` launcher is unavailable, replace `py` with `python` in the install
and usage commands.

## Usage

The first argument after `main.py` is the required **mode**. The available modes
are:

- `image`
- `play-video`
- `export-video`

Running only `py main.py` produces a "mode is required" message because the
program does not know which operation to perform.

View the main help page with:

```powershell
py main.py --help
```

View the options for one mode with:

```powershell
py main.py image --help
py main.py play-video --help
py main.py export-video --help
```

### 1. Convert a static image

```powershell
py main.py image images/test_car.jpg --width 100 --output output/output.txt
```

This command:

1. Loads `images/test_car.jpg`.
2. Resizes it to an ASCII width of 100 characters.
3. Converts it to grayscale and maps each brightness value to an ASCII
   character.
4. Prints the completed ASCII art in the terminal.
5. Saves it to `output/output.txt` using UTF-8.

The image mode has these defaults:

```text
Input:  images/test_car.jpg
Width:  100
Output: output/output.txt
```

Therefore, this shorter command also works:

```powershell
py main.py image
```

### 2. Play a video as terminal ASCII

```powershell
py main.py play-video videos/5_sec_rule.mp4 --width 60
```

The program reads the complete video one frame at a time, converts each frame to
ASCII, and redraws it from the top-left of the terminal. Playback timing uses the
video's FPS. Press `Ctrl+C` to stop playback cleanly.

The playback mode has these defaults:

```text
Input: videos/5_sec_rule.mp4
Width: 60
```

The default command is:

```powershell
py main.py play-video
```

An ANSI-compatible terminal such as Windows Terminal is recommended. A smaller
width improves performance and helps the frames fit inside the terminal window.

### 3. Export a video as an ASCII MP4

```powershell
py main.py export-video videos/5_sec_rule.mp4 --width 60 --output output/ascii_video.mp4
```

Every source frame is converted to ASCII and drawn into a fixed-size OpenCV
frame. The rendered frames are then encoded into a playable MP4.

The export mode has these defaults:

```text
Input:  videos/5_sec_rule.mp4
Width:  60
Output: output/ascii_video.mp4
```

The default command is:

```powershell
py main.py export-video
```

The exported MP4 is currently silent. Audio from the original video is not
preserved in this milestone.

## Project structure

```text
main.py                    Command-line entry point and dependency setup
ascii_converter.py         Pillow Image -> ASCII string
image_source.py            Image path -> loaded Pillow Image
image_saver.py             ASCII string -> UTF-8 text file
video_source.py            Video path -> sequential Pillow frames
terminal_renderer.py       ASCII string -> terminal display
video_player.py             Coordinates complete terminal playback
ascii_frame_renderer.py    ASCII string -> OpenCV BGR image frame
video_saver.py              BGR frames -> encoded MP4
video_exporter.py           Coordinates complete MP4 export
ascii_generator.py          Unused legacy image-only implementation
images/                     Example input images
videos/                     Example input videos
output/                     Generated text and video files
```

The three processing flows are:

```text
Static image:
ImageSource -> AsciiConverter -> terminal output / ImageSaver

Terminal video:
VideoSource -> AsciiConverter -> TerminalRenderer

Exported MP4:
VideoSource -> AsciiConverter -> AsciiFrameRenderer -> VideoSaver
```

## How conversion works

`AsciiConverter` resizes each image while preserving its aspect ratio. A `0.55`
height correction compensates for terminal characters being taller than they are
wide. The resized image is converted to grayscale, and every brightness value
from 0 to 255 is mapped onto a dark-to-light ASCII character palette. The
characters are then grouped into rows to produce the final ASCII string.

Increasing `--width` produces more detail but requires more terminal space and
processing time. The width must be greater than zero.
