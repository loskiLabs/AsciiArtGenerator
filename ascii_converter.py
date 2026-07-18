class AsciiConverter:
    """Convert loaded Pillow images into ASCII art strings."""

    ASCII_CHARS = (
        "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/"
        "|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    )

    def _resize_image(self, image, width):
        """Resize the image while preserving aspect ratio."""
        original_width, original_height = image.size
        aspect_ratio = original_height / original_width
        calculated_height = int(aspect_ratio * width * 0.55)
        new_height = max(1, calculated_height)

        return image.resize((width, new_height))

    def _convert_to_grayscale(self, image):
        """Convert the image to grayscale brightness values."""
        return image.convert("L")

    def _map_pixel_to_ascii(self, brightness):
        """Map a 0-255 brightness value to an ASCII character."""
        index = brightness * (len(self.ASCII_CHARS) - 1) // 255
        return self.ASCII_CHARS[index]

    def _pixels_to_ascii(self, image):
        """Convert all grayscale pixels to one ASCII string."""
        return "".join(
            self._map_pixel_to_ascii(brightness)
            for brightness in image.getdata()
        )

    def _format_ascii(self, ascii_string, width):
        """Split a long ASCII string into image-width rows."""
        rows = [
            ascii_string[index:index + width]
            for index in range(0, len(ascii_string), width)
        ]

        return "\n".join(rows) + "\n"

    def convert(self, image, width=100):
        """Convert an already-loaded Pillow image into ASCII art."""
        if width <= 0:
            raise ValueError("width must be greater than zero")

        resized_image = self._resize_image(image, width)
        grayscale_image = self._convert_to_grayscale(resized_image)
        ascii_string = self._pixels_to_ascii(grayscale_image)

        return self._format_ascii(ascii_string, grayscale_image.width)
