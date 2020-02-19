import logging
from decouple import config
from django.core.management.color import color_style

LOGGER_LEVEL = config('LOGGER_LEVEL', default='INFO')


class DjangoColorsFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super(DjangoColorsFormatter, self).__init__(*args, **kwargs)
        self.style = self.configure_style(color_style())

    def configure_style(self, style):
        style.DEBUG = style.HTTP_NOT_MODIFIED
        style.INFO = style.HTTP_INFO
        style.WARNING = style.HTTP_NOT_FOUND
        style.ERROR = style.ERROR
        style.CRITICAL = style.HTTP_SERVER_ERROR
        return style

    def format(self, record):
        message = logging.Formatter.format(self, record)
        colorizer = getattr(self.style, record.levelname, self.style.HTTP_SUCCESS)
        return colorizer(message)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            # 'formatter': 'verbose_colored'
            'formatter': 'verbose'
        },
    },
    'formatters': {
        'verbose_colored': {
            '()': DjangoColorsFormatter,
            'format': '{levelname} {asctime} {pathname}, @{lineno} :\n{message} \n',
            'style': '{',
        },
        'verbose': {
            'format': '{levelname} {asctime} {pathname}, @{lineno} :\n {message} \n',
            'style': '{',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': LOGGER_LEVEL,
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': LOGGER_LEVEL,
            'propagate': True,
        },
        'sid': {
            'handlers': ['console'],
            'level': LOGGER_LEVEL,
            'propagate': True,
        },
        'plugin_ideo_bfc': {
            'handlers': ['console'],
            'level': LOGGER_LEVEL,
            'propagate': True,
        },
        'test': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
