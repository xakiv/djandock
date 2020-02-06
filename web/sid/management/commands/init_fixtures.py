import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        models_data = [
            ('sid_license', 'data/sid/initial/license.json'),
            ('sid_organisation_type', 'data/sid/initial/organisation_type.json'),
        ]
        for model, data_path in models_data:
            call_command('loaddata', data_path, verbosity=0)
