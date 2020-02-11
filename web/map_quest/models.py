from django.contrib.gis.db import models


class Dataset(models.Model):

    def logo_dir(instance, filename):
        return "dataset_{0}/logo/{1}".format(instance.pk, filename)

    label = models.CharField('Label', max_length=2048)

    description = models.TextField('Description')

    logo = models.ImageField('Logo', upload_to=logo_dir, blank=True, null=True)

    created_on = models.DateTimeField('Crée le', auto_now_add=True)

    @property
    def nb_subsets(self):
        return self.subsets.count()

    @property
    def attachments(self):
        return [subset.attachement for subset in self.subsets.all()]


class ContextualGeom(models.Model):

    label = models.CharField('Label', max_length=2048)

    color = models.CharField(
        verbose_name='Couleur', max_length=7, blank=True, null=True
    )

    is_active = models.BooleanField('Est valide', default=True)

    class Meta:
        abstract = True


class Node(ContextualGeom):

    geom = models.PointField('POI', srid=4326)


class Edge(ContextualGeom):

    geom = models.MultiLineStringField('Ligne', srid=4326)


class Polygon(ContextualGeom):

    geom = models.MultiPolygonField('Zones', srid=4326)


class Subset(models.Model):

    def attachement_dir(instance, filename):
        return "dataset_{0}/subseet_{1}/attachement/{2}".format(instance.dataset.pk, instance.pk, filename)

    dataset = models.ForeignKey('map_quest.Dataset', on_delete=models.CASCADE, related_name='subsets')

    nodes = models.ManyToManyField('map_quest.Node')

    edges = models.ManyToManyField('map_quest.Edge')

    polygones = models.ManyToManyField('map_quest.Polygon')

    color = models.CharField(
        verbose_name='Couleur par défaut', max_length=7, blank=True, null=True
    )

    context = models.TextField('Contexte')

    attachement = models.FileField(
        'Fichier joint', upload_to=attachement_dir, blank=True, null=True
    )
