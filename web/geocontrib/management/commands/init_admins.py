import json
import logging
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True, is_active=True).exists():
            admins_data = os.getenv('ADMINS_CREDENTIALS', '{}')
            for data in json.loads(admins_data):
                user = User.objects.create_superuser(**data)
                logger.info("Superuser created: {}".format(user.username))
