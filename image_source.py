from PIL import Image


class ImageSource:
    """Load image files as Pillow Image objects."""

    def load(self, path):
        """Load an image file and return None if loading fails."""
        try:
            image = Image.open(path)
            image.load()
            return image
        except FileNotFoundError:
            print(f"Image file not found: {path}")
            return None
        except Exception as error:
            print(f"Error loading image '{path}': {error}")
            return None
