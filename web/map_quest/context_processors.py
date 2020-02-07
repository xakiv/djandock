import logging
import json

from django.conf import settings

logger = logging.getLogger(__name__)


def custom_contexts(request):

    return {
        'APPLICATION_NAME': settings.APPLICATION_NAME,
        'APPLICATION_ABSTRACT': settings.APPLICATION_ABSTRACT,
        'DATASETS_VERBOSE_NAME_PLURAL': settings.DATASETS_VERBOSE_NAME_PLURAL,
        'DATASETS_VERBOSE_NAME': settings.DATASETS_VERBOSE_NAME,
        'LOGO_PATH': settings.LOGO_PATH,
        'IMAGE_FORMAT': settings.IMAGE_FORMAT,
        'FILE_MAX_SIZE': settings.FILE_MAX_SIZE,

        'SERVICE': settings.DEFAULT_BASE_MAP.get('SERVICE'),
        'OPTIONS': json.dumps(settings.DEFAULT_BASE_MAP.get('OPTIONS')),
        'DEFAULT_MAP_VIEW': settings.DEFAULT_MAP_VIEW
    }
