import base64
from io import BytesIO

import imagehash
import PIL
import requests


class Image:
    """
    An image class to calculate the dhash value and create preview images.
    """

    def __init__(self, img_url: str):
        """Constructor

        Args:
            img_url (str): The image to load.
        """

        self.img = None

        if "http" in img_url:
            response = requests.get(img_url)
            self.img = PIL.Image.open(BytesIO(response.content))
        else:
            self.img = PIL.Image.open(img_url)

    def dhash(self) -> imagehash.ImageHash:
        """Calcualtes the image dhash.

        Returns:
            imagehash.ImageHash: The image hash.
        """
        return imagehash.dhash(self.img)

    def is_big(self) -> bool:
        """Checks if the image is considered big.

        Returns:
            bool: True if the image is big, otherwise False.
        """
        return self.img.width > 50 and self.img.height > 50

    def scale_down(self, size: int) -> PIL.Image:
        """Creates a scaled down version of the image.

        Args:
            size (int): The new image width.

        Returns:
            PIL.Image: The scaled down version.
        """

        rgb = self.img.convert('RGB')

        width, height = self.img.size

        if width <= size:
            return rgb

        new_width = size
        new_height = int(height * (new_width / width))

        return rgb.resize((new_width, new_height), PIL.Image.LANCZOS)

    def store_preview(self, preview_url: str, size: int):
        """Stores an preview image at the given location.

        Args:
            preview_url (str): The preview image location.
            size (int): The preview image width.
        """
        self.scale_down(size).save(preview_url, "JPEG")

    def jpeg_base64(self, size: int) -> bytes:
        """Returns the Base64 encoded JPEG image.

        Args:
            size (int): The width of the encode image.

        Returns:
            bytes: Base64 encoded JPEG image.
        """

        buffered = BytesIO()
        self.scale_down(size).save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
