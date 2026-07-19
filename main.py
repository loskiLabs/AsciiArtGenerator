from ascii_converter import AsciiConverter
from file_saver import FileSaver
from image_source import ImageSource
from video_source import VideoSource


def main():
    iSource = ImageSource()
    converter = AsciiConverter()
    saver = FileSaver()
    vSource = VideoSource()

    image = iSource.load("images/test_car.jpg")
    video = vSource.openVid("videos/5_sec_rule.mp4")

    vSource.read_frame(video)

    """
    if image is None:
        return

    try:
        ascii_art = converter.convert(image, width=100)
        print(ascii_art)
        saver.save(ascii_art, "output/output.txt")
    finally:
        image.close()
    """

if __name__ == "__main__":
    main()
