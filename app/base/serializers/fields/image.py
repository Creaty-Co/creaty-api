from drf_base64.fields import Base64ImageField as _Base64ImageField
from rest_framework.fields import SkipField

from app.base.forms.fields.image import ImageFormField


# TODO: add OpenApiSerializerFieldExtension for this
class Base64ImageField(_Base64ImageField):
    def __init__(self, allowed_extensions=None, **kwargs):
        """
        :param allowed_extensions: None means default ImageFormField allowed_extensions
        """
        if allowed_extensions is None:
            kwargs['_DjangoImageField'] = ImageFormField
        else:
            kwargs['_DjangoImageField'] = lambda: ImageFormField(
                allowed_extensions=allowed_extensions
            )
        super().__init__(**kwargs)

    def _decode(self, data):
        try:
            value = super()._decode(data)
        except SkipField:
            if self.required:
                self.fail('invalid_image')
            raise
        except (ValueError, UnicodeDecodeError):
            self.fail('invalid_image')
        return value
