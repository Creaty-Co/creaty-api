from logging import FileHandler as _FileHandler
from pathlib import Path

__all__ = ['FileHandler']


class FileHandler(_FileHandler):
    def _open(self):
        Path(self.baseFilename).parent.mkdir(parents=True, exist_ok=True)
        # noinspection PyProtectedMember
        return super()._open()
