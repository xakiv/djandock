from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from django.utils.timezone import now

from api.serializers import ProjectDetailedSerializer
from api.serializers import StackedEventSerializer

from geocontrib.emails import notif_suscriber_grouped_events
from geocontrib.models import Project
from geocontrib.models import StackedEvent
from geocontrib.models import Subscription

import logging
logger = logging.getLogger('django')

User = get_user_model()


class Command(BaseCommand):
    help = """Commande pouvant etre associé à une tache CRON et notifiant les utilisateurs,
        des evenements les concernant."""

    def handle(self, *args, **options):

        frequency_setted = settings.DEFAULT_SENDING_FREQUENCY
        if frequency_setted not in ['instantly', 'daily', 'weekly']:
            logger.error('The default frequency setting is incorrect')
            return

        users = User.objects.filter(is_active=True)
        for user in users:

            # Pour chaque utilisateur on filtre les abonnements projets
            project_slugs = Subscription.objects.filter(
                users=user
            ).values_list('project__slug', flat=True)
            stacked_events = []
            context = {}
            for slug in project_slugs:

                pending_stack = StackedEvent.objects.filter(
                    project_slug=slug, state='pending',
                    schedualed_delivery_on__lte=now()
                )

                if pending_stack.exists():
                    serialized_project = ProjectDetailedSerializer(Project.objects.get(slug=slug))
                    # On ne peut avoir qu'une pile en attente pour un projet donnée
                    serialized_stack = StackedEventSerializer(pending_stack.first())

                    stacked_events.append(
                        {
                            'project_data': serialized_project.data,
                            'stack_data': serialized_stack.data,
                        }
                    )

            context['stacked_events'] = stacked_events
            if len(context['stacked_events']) > 0:
                try:
                    notif_suscriber_grouped_events(emails=[user.email, ], context=context)
                except Exception:
                    logger.exception('Error on notif_suscriber_grouped_events: {0}'.format(user.email))
                else:
                    logger.info('Batch sent to {0}'.format(user.email))

        # TODO @cbenhabib: revoir la gestion des stack en erreur
        for row in StackedEvent.objects.filter(state='pending', schedualed_delivery_on__lte=now()):
            row.state = 'successful'
            row.save()

        logger.info('Command succeeded! ')
