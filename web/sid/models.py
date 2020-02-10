import logging
from urllib.parse import urljoin
import uuid

# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from django.utils.text import slugify
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone


logger = logging.getLogger(__name__)


class Profile(models.Model):

    class Meta(object):
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils des utilisateurs"

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    organisation = models.ForeignKey(
        to='Organisation',
        verbose_name="Organisation d'appartenance",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    referents = models.ManyToManyField(
        to='Organisation',
        through='LiaisonsReferents',
        related_name='profile_referents',
        verbose_name="Organisation dont l'utilisateur est réferent",
    )

    contributions = models.ManyToManyField(
        to='Organisation',
        through='LiaisonsContributeurs',
        related_name='profile_contributions',
        verbose_name="Organisation dont l'utilisateur est contributeur",
    )

    phone = models.CharField(
        verbose_name="Téléphone",
        max_length=10,
        blank=True,
        null=True,
        )

    is_active = models.BooleanField(
        verbose_name="Validation suite à confirmation par e-mail",
        default=False,
        )

    membership = models.BooleanField(
        verbose_name="Utilisateur rattaché à une organisation",
        default=False,
        )

    crige_membership = models.BooleanField(
        verbose_name="Utilisateur partenaire IDGO",
        default=False,
        )

    is_admin = models.BooleanField(
        verbose_name="Administrateur métier",
        default=False,
        )

    sftp_password = models.CharField(
        verbose_name="Mot de passe sFTP",
        max_length=10,
        blank=True,
        null=True,
        )

    def __str__(self):
        return "{} ({})".format(self.user.get_full_name(), self.user.username)


class LiaisonsReferents(models.Model):

    class Meta(object):
        verbose_name = "Statut de référent"
        verbose_name_plural = "Statuts de référent"
        unique_together = (
            ('profile', 'organisation'),
            )

    profile = models.ForeignKey(
        to='Profile',
        verbose_name='Profil utilisateur',
        on_delete=models.CASCADE,
        )

    organisation = models.ForeignKey(
        to='Organisation',
        verbose_name='Organisation',
        on_delete=models.CASCADE,
        )

    created_on = models.DateField(
        verbose_name="Date de la demande de statut de référent",
        auto_now_add=True,
        )

    validated_on = models.DateField(
        verbose_name="Date de la confirmation par un administrateur",
        blank=True,
        null=True,
        default=timezone.now,
        )

    def __str__(self):
        return '{full_name} ({username})--{organisation}'.format(
            full_name=self.profile.user.get_full_name(),
            username=self.profile.user.username,
            organisation=self.organisation.legal_name,
            )

    # Méthodes de classe
    # ==================

    @classmethod
    def get_subordinated_organisations(cls, profile):

        # TODO: Sortir le rôle 'admin' (Attention à l'impact que cela peut avoir sur le code)
        if profile.is_admin:
            Organisation = apps.get_model(app_label='sid', model_name='Organisation')
            return Organisation.objects.filter(is_active=True)

        kwargs = {'profile': profile, 'validated_on__isnull': False}
        return [e.organisation for e in LiaisonsReferents.objects.filter(**kwargs)]

    @classmethod
    def get_pending(cls, profile):
        kwargs = {'profile': profile, 'validated_on': None}
        return [e.organisation for e in LiaisonsReferents.objects.filter(**kwargs)]


class LiaisonsContributeurs(models.Model):

    class Meta(object):
        verbose_name = "Statut de contributeur"
        verbose_name_plural = "Statuts de contributeur"
        unique_together = (
            ('profile', 'organisation'),
            )

    profile = models.ForeignKey(
        to='Profile',
        verbose_name="Profil utilisateur",
        on_delete=models.CASCADE,
        )

    organisation = models.ForeignKey(
        to='Organisation',
        verbose_name="Organisation",
        on_delete=models.CASCADE,
        )

    created_on = models.DateField(
        verbose_name="Date de la demande de statut de contributeur",
        auto_now_add=True,
        )

    validated_on = models.DateField(
        verbose_name="Date de la confirmation par un administrateur",
        blank=True,
        null=True,
        )

    def __str__(self):
        return '{full_name} ({username})--{organisation}'.format(
            full_name=self.profile.user.get_full_name(),
            username=self.profile.user.username,
            organisation=self.organisation.legal_name,
            )

    # Méthodes de classe
    # ==================

    @classmethod
    def get_contribs(cls, profile):
        kwargs = {'profile': profile, 'validated_on__isnull': False}
        return [e.organisation for e in LiaisonsContributeurs.objects.filter(**kwargs)]

    @classmethod
    def get_contributors(cls, organisation):
        kwargs = {'organisation': organisation, 'validated_on__isnull': False}
        return [e.profile for e in LiaisonsContributeurs.objects.filter(**kwargs)]

    @classmethod
    def get_pending(cls, profile):
        kwargs = {'profile': profile, 'validated_on': None}
        return [e.organisation for e in LiaisonsContributeurs.objects.filter(**kwargs)]


class OrganisationType(models.Model):

    class Meta(object):
        verbose_name = "Type d'organisation"
        verbose_name_plural = "Types d'organisations"
        ordering = ('name',)

    code = models.CharField(
        verbose_name="Code",
        max_length=100,
        primary_key=True,
        )

    name = models.TextField(
        verbose_name="Type d'organisation",
        )

    def __str__(self):
        return self.name


class License(models.Model):

    class Meta(object):
        verbose_name = "Licence"
        verbose_name_plural = "Licences"

    slug = models.SlugField(
        verbose_name="Slug",
        max_length=100,
        blank=True,
        unique=True,
        db_index=True,
        primary_key=True,
        )

    title = models.TextField(
        verbose_name="Titre",
        )

    alternate_titles = ArrayField(
        models.TextField(),
        verbose_name="Autres titres",
        blank=True,
        null=True,
        size=None,
        )

    url = models.URLField(
        verbose_name="URL",
        blank=True,
        null=True,
        )

    alternate_urls = ArrayField(
        models.URLField(),
        verbose_name="Autres URLs",
        null=True,
        blank=True,
        size=None,
        )

    domain_content = models.BooleanField(
        verbose_name="Domain Content",
        default=False,
        )

    domain_data = models.BooleanField(
        default=False,
        verbose_name="Domain Data",
        )

    domain_software = models.BooleanField(
        default=False,
        verbose_name="Domain Software",
        )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('deleted', 'Deleted'),
        )

    status = models.CharField(
        verbose_name="Status",
        max_length=7,
        choices=STATUS_CHOICES,
        default='active',
        )

    maintainer = models.TextField(
        verbose_name="Maintainer",
        null=True,
        blank=True,
        )

    CONFORMANCE_CHOICES = (
        ('approved', 'Approved'),
        ('not reviewed', 'Not reviewed'),
        ('rejected', 'Rejected'),
        )

    od_conformance = models.CharField(
        verbose_name="Open Definition Conformance",
        max_length=30,
        choices=CONFORMANCE_CHOICES,
        default='not reviewed',
        )

    osd_conformance = models.CharField(
        verbose_name="Open Source Definition Conformance",
        max_length=30,
        choices=CONFORMANCE_CHOICES,
        default='not reviewed',
        )

    def __str__(self):
        return self.title

    @property
    def ckan_id(self):
        return self.slug


class Organisation(models.Model):

    class Meta(object):
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"
        ordering = ('slug',)

    legal_name = models.CharField(
        verbose_name="Dénomination sociale",
        max_length=255,
        unique=True,
        db_index=True,
        )

    organisation_type = models.ForeignKey(
        to='OrganisationType',
        verbose_name="Type d'organisation",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        )

    # jurisdiction = models.ForeignKey(
    #     to='Jurisdiction',
    #     verbose_name="Territoire de compétence",
    #     blank=True,
    #     null=True,
    #     )

    slug = models.SlugField(
        verbose_name="Slug",
        max_length=255,
        unique=True,
        db_index=True,
        )

    ckan_id = models.UUIDField(
        verbose_name="Ckan UUID",
        default=uuid.uuid4,
        editable=False,
        )

    website = models.URLField(
        verbose_name="Site internet",
        blank=True,
        null=True,
        )

    email = models.EmailField(
        verbose_name="Adresse e-mail",
        blank=True,
        null=True,
        )

    description = models.TextField(
        verbose_name='Description',
        blank=True,
        null=True,
        )

    logo = models.ImageField(
        verbose_name="Logo",
        blank=True,
        null=True,
        upload_to='logos/',
        )

    address = models.TextField(
        verbose_name="Adresse",
        blank=True,
        null=True,
        )

    postcode = models.CharField(
        verbose_name="Code postal",
        max_length=100,
        blank=True,
        null=True,
        )

    city = models.CharField(
        verbose_name="Ville",
        max_length=100,
        blank=True,
        null=True,
        )

    phone = models.CharField(
        verbose_name="Téléphone",
        max_length=10,
        blank=True,
        null=True,
        )

    license = models.ForeignKey(
        to='License',
        verbose_name="Licence",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        )

    is_active = models.BooleanField(
        verbose_name="Organisation active",
        default=False,
        )

    is_crige_partner = models.BooleanField(
        verbose_name="Organisation partenaire IDGO",
        default=False,
        )

    geonet_id = models.TextField(
        verbose_name="UUID de la métadonnées",
        unique=True,
        db_index=True,
        blank=True,
        null=True,
        )

    def __str__(self):
        return self.legal_name

    @property
    def logo_url(self):
        try:
            return urljoin(settings.DOMAIN_NAME, self.logo.url)
        except (ValueError, Exception):
            return None

    @property
    def full_address(self):
        return "{} - {} {}".format(self.address, self.postcode, self.city)


# Triggers


# @receiver(pre_save, sender=Organisation)
# def pre_save_organisation(sender, instance, **kwargs):
#     instance.slug = slugify(instance.legal_name)
