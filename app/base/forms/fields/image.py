from django.core.validators import (
    FileExtensionValidator,
    get_available_image_extensions,
)
from django_svg_image_form_field import SvgAndImageFormField


class ImageFormField(SvgAndImageFormField):
    default_validators = []

    def __init__(
        self,
        *,
        allowed_extensions=tuple(get_available_image_extensions() + ['svg']),
        max_length=None,
        allow_empty_file=False,
        **kwargs,
    ):
        kwargs['validators'] = [
            *kwargs['validators'],
            FileExtensionValidator(allowed_extensions),
        ]
        super().__init__(
            max_length=max_length, allow_empty_file=allow_empty_file, **kwargs
        )
