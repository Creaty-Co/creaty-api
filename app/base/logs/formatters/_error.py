from app.base.logs.formatters._wrap import WrapFormatter

__all__ = ['ErrorFormatter']


def _tab(text: str) -> str:
    if text.endswith('\n'):
        return '\t' + text.replace('\n', '\n\t')[:-1]
    return '\t' + text.replace('\n', '\n\t')


class ErrorFormatter(WrapFormatter):
    def formatException(self, ei):
        formatted_exception = super().formatException(ei)
        return _tab(
            f'<<<\n{_tab(formatted_exception)}'
            + ('' if formatted_exception.endswith('\n') else '\n')
            + '>>>'
        )
