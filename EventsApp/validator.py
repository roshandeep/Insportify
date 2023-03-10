from django.core.exceptions import ValidationError


def image_restriction(value):
    print(value)
    image_width = 1600
    image_height = 1600
    if image_width >= 360 or image_height >= 140:
        raise ValidationError('Image width needs to be less than 360px * 140px')
