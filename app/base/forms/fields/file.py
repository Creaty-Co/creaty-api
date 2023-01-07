from django.core.validators import FileExtensionValidator
from django.forms import FileField


class FileFormField(FileField):
    def __init__(
        self,
        *,
        allowed_extensions=None,
        max_length=None,
        allow_empty_file=False,
        **kwargs,
    ):
        """
        :param allowed_extensions: None means that all extensions are allowed
        """
        if allowed_extensions is not None:
            kwargs['validators'] = [
                *kwargs['validators'],
                FileExtensionValidator(allowed_extensions),
            ]
        super().__init__(
            max_length=max_length, allow_empty_file=allow_empty_file, **kwargs
        )
