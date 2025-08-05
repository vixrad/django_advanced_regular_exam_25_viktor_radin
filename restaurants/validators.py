from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError
import os

def validate_1920x1080_image(image):
    if not image or not hasattr(image, 'name'):
        return
    if image.size == 0:
        return
    if image.size > 2 * 1024 * 1024:
        raise ValidationError("Image file size must not exceed 2MB.")
    valid_extensions = ['.jpg', '.jpeg', '.png']
    ext = os.path.splitext(image.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError("Only PNG or JPG images are allowed.")
    try:
        image.seek(0)
        img = Image.open(image)
        width, height = img.size
        if width != 1920 or height != 1080:
            raise ValidationError("Image must be exactly 1920 x 1080 pixels.")
    except UnidentifiedImageError:
        raise ValidationError("Invalid image file.")
    finally:
        image.seek(0)