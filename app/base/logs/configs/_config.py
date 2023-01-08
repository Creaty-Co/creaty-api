from copy import deepcopy
from typing import Any, TypedDict, Union

from app.base.logs.configs.base import base_config

__all__ = ['LogConfig']


class _TypeLoggerConfig(TypedDict):
    handlers: list[dict[str, Any]]
    level: Union[int, str]
    propagate: bool


class LogConfig:
    DEFAULT_LEVEL = 'DEBUG'

    def __init__(self, loggers: dict[str, _TypeLoggerConfig]):
        self.loggers = deepcopy(loggers)
        self.__dict_config: dict

    def to_dict(self) -> dict[str, Any]:
        self._setup_dict_config()
        return self.__dict_config

    def _setup_dict_config(self) -> None:
        self.__dict_config = deepcopy(base_config)
        self._setup_loggers()

    def _setup_loggers(self):
        dict_config = self.__dict_config
        for logger, config in self.loggers.items():
            self._setup_logger_config(config)
            dict_config['loggers'][logger] = config | {'handlers': []}
            for handler in config['handlers']:
                dict_config['loggers'][logger]['handlers'].append(
                    self._setup_handler(handler)
                )

    def _setup_logger_config(self, logger_config: _TypeLoggerConfig) -> None:
        logger_config['propagate'] = False
        logger_config['level'] = logger_config.get('level', self.DEFAULT_LEVEL)

    def _setup_handler(self, handler: dict[str, Any]) -> str:
        handler = deepcopy(handler)
        handler_name = handler.pop('__name__')
        try:
            handler['formatter'] = self._setup_formatter(handler['formatter'])
        except KeyError:
            pass
        self.__dict_config['handlers'][handler_name] = handler
        return handler_name

    def _setup_formatter(self, formatter: dict[str, Any]) -> str:
        formatter = deepcopy(formatter)
        formatter_name = formatter.pop('__name__')
        self.__dict_config['formatters'][formatter_name] = formatter
        return formatter_name
