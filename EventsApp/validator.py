from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


def image_restriction(image):
    image_width, image_height = get_image_dimensions(image)
    # print(image_width, image_height)
    if image_width >= 360 or image_height >= 140:
        raise ValidationError('Image width needs to be less than 360px * 140px')
