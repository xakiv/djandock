from django.db import models
from django.db.models import Q
from django.apps import apps
from geocontrib.choices import MODERATOR


class AvailableFeaturesManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def availables(self, user, project):
        Authorization = apps.get_model(app_label='geocontrib', model_name='Authorization')
        UserLevelPermission = apps.get_model(app_label='geocontrib', model_name='UserLevelPermission')

        # 0 - si utlisateur anonyme
        if not user.is_authenticated:
            if Authorization.has_permission(user, 'can_view_archived_feature', project):
                queryset = self.get_queryset().filter(
                    project=project
                ).filter(Q(status='published') | Q(status='archived'))
            else:
                queryset = self.get_queryset().filter(
                    project=project, status='published')
        else:
            # 1 - si is_project_administrator on liste toutes les features
            queryset = self.get_queryset().filter(project=project)
            if not Authorization.has_permission(user, 'is_project_administrator', project):
                # Sont exclus les signalement Brouillon des autres utilisateurs
                queryset = queryset.exclude(
                    ~Q(creator=user), status='draft',
                )

                # 2/3/4 - si niveaux d'accés mini superieurs au niveau de l'utilisateur
                # on exclut les signalements mis en attente et archivés
                user_rank = Authorization.get_rank(user, project)
                project_arch_rank = project.access_level_arch_feature.rank
                project_pub_rank = project.access_level_pub_feature.rank
                moderateur_rank = UserLevelPermission.objects.get(user_type_id=MODERATOR).rank
                if project.moderation and user_rank < moderateur_rank:
                    queryset = queryset.exclude(
                        ~Q(creator=user), status='pending',
                    )

                if user_rank < project_arch_rank:
                    queryset = queryset.exclude(
                        status='archived',
                    )

                if user_rank < project_pub_rank:
                    queryset = queryset.exclude(
                        ~Q(creator=user), status='published',
                    )

        return queryset
