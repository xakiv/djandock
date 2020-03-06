import logging

from django.core.management.base import BaseCommand
from django.core.management import call_command

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = """Replacing 'migrate' command;
    Allowng to choose where 'another_one' app will be migrated"""

    def handle(self, *args, **options):

        default_apps = [
            'contenttypes',
            'auth',
            'admin',
            'sessions',
            'sites',
            'api',
            'geocontrib',
        ]

        for app in default_apps:
            call_command('migrate', app, database='default', verbosity=0)
            logger.info("App {} migrated on default's database. ".format(app))

        call_command('migrate', 'another_one', database='switch', verbosity=0)
        logger.info("App {} migrated on switch's database. ".format(app))
