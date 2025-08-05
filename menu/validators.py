from django.core.exceptions import ValidationError
from PIL import Image

def validate_square_image(image):
    try:
        img = Image.open(image)
        width, height = img.size
        if width != height:
            raise ValidationError("Image must be square (1:1 aspect ratio).")
        if width < 600 or height < 600:
            raise ValidationError("Image must be at least 600x600 pixels.")
    except Exception:
        raise ValidationError("Invalid image file.")