from ascii_converter import AsciiConverter
from file_saver import FileSaver
from image_source import ImageSource


def main():
    iSource = ImageSource()
    converter = AsciiConverter()
    saver = FileSaver()

    image = iSource.load("images/test_car.jpg")

    if image is None:
        return

    try:
        ascii_art = converter.convert(image, width=100)
        print(ascii_art)
        saver.save(ascii_art, "output/output.txt")
    finally:
        image.close()


if __name__ == "__main__":
    main()
