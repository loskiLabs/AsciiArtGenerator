from PIL import Image

class AsciiGenerator:
# all the processing functions to be used in main

    #ASCII_CHARS = "@%#*+=-:. "

    ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# input
    def loadImage(self, path):
        try:
            image = Image.open(path)
            return image
        except Exception as e:
            print(f"Oops. Error loading image: {e}")
            return None
        

    # Resize image
    def resizeImage(self, image, width=100):
       
        original_width, original_height = image.size
        aspect_ratio = original_height / original_width
        new_height = int(aspect_ratio * width * 0.55)
        resized_image = image.resize((width, new_height))

        return resized_image

    # Grayify image (convert image to greyscale)
    def grayifyImage(self, image):
        return image.convert("L")


    # Map pixel to Ascii character
    def mapPixelToAscii(self, brightness):
        
        index = brightness * (len(self.ASCII_CHARS) - 1) // 255

        return self.ASCII_CHARS[index]

    def pixelToAscii(self, image):
        
        pixels = image.getdata()
        ascii_str = ""

        for pixel in pixels:
            ascii_str += self.mapPixelToAscii(pixel)

        return ascii_str

    # function which uses helper functions to generate the actual ascii image (text)
    def generateAsciiArt(self, path):
        image = self.loadImage(path)
        image = self.resizeImage(image)
        image = self.grayifyImage(image)

        ascii_str = self.pixelToAscii(image)

        width = image.width

        ascii_art = ""

        for i in range(0, len(ascii_str), width):
            ascii_art += ascii_str[i:i+width] + "\n"

        self.__saveArt(ascii_art, "output.txt")

        return ascii_art

    # Saves image(text) to a new file
    def __saveArt(self, ascii_art, filename):
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(ascii_art)

            print(f"ASCII art saved to {filename}")

        except Exception as e:
            print(f"Error saving ASCII art: {e}")
