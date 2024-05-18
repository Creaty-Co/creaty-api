import re

from django.core.files.storage import FileSystemStorage as _FileSystemStorage


class FileSystemStorage(_FileSystemStorage):
    def url(self, name: str) -> str:
        if re.match(r'(.+)-\d+', name):
            name = f"{name.split('-')[0]}.jpg"
        return super().url(name)
