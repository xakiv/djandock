from django.contrib.gis.db import models
from django.conf import settings

USER_MODEL = settings.AUTH_USER_MODEL


class Transfer(models.Model):

    rank = models.PositiveSmallIntegerField(
        "Rang", unique=True)

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    project_from = models.ForeignKey(
        to="geocontrib.Project", on_delete=models.CASCADE, related_name="switch_projects_from")

    project_to = models.ForeignKey(
        to="geocontrib.Project", on_delete=models.CASCADE, related_name="switch_projects_to")

    # class Meta:
        # db_table = 'switch\".\"another_one_transfer'
        # db_schema = "switch"
