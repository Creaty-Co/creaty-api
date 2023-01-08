from app.base.logs.configs.formatters import *

__all__ = ['web_console', 'web_file', 'api_console', 'api_file', 'email_admins']

_level = 'DEBUG'
_file_encoding = 'utf-8'
_file_mode = 'a'
_log_filename = 'logs/logs.log'

web_console = {
    '__name__': 'web_console_handler',
    'level': _level,
    'class': 'logging.StreamHandler',
    'formatter': web,
    'stream': 'ext://sys.stdout',
}

web_file = {
    '__name__': 'web_file_handler',
    'level': _level,
    'class': 'app.base.logs.handlers.FileHandler',
    'formatter': web,
    'filename': _log_filename,
    'mode': _file_mode,
    'encoding': _file_encoding,
}

api_console = {
    '__name__': 'api_console_handler',
    'level': _level,
    'class': 'app.base.logs.handlers.StdHandler',
    'formatter': api,
}

api_file = {
    '__name__': 'api_file_handler',
    'level': _level,
    'class': 'app.base.logs.handlers.FileHandler',
    'formatter': api,
    'filename': _log_filename,
    'mode': _file_mode,
    'encoding': _file_encoding,
}

email_admins = {
    '__name__': 'email_admins_handler',
    'level': 'ERROR',
    'class': 'app.base.logs.handlers.AdminEmailHandler',
    'formatter': api,
    'include_html': True,
}
