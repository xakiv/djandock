# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-11-07 14:30
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LiaisonsContributeurs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Date de la demande de statut de contributeur')),
                ('validated_on', models.DateField(blank=True, null=True, verbose_name='Date de la confirmation par un administrateur')),
            ],
            options={
                'verbose_name': 'Statut de contributeur',
                'verbose_name_plural': 'Statuts de contributeur',
            },
        ),
        migrations.CreateModel(
            name='LiaisonsReferents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True, verbose_name='Date de la demande de statut de référent')),
                ('validated_on', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date de la confirmation par un administrateur')),
            ],
            options={
                'verbose_name': 'Statut de référent',
                'verbose_name_plural': 'Statuts de référent',
            },
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('slug', models.SlugField(blank=True, max_length=100, primary_key=True, serialize=False, unique=True, verbose_name='Slug')),
                ('title', models.TextField(verbose_name='Titre')),
                ('alternate_titles', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None, verbose_name='Autres titres')),
                ('url', models.URLField(blank=True, null=True, verbose_name='URL')),
                ('alternate_urls', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), blank=True, null=True, size=None, verbose_name='Autres URLs')),
                ('domain_content', models.BooleanField(default=False, verbose_name='Domain Content')),
                ('domain_data', models.BooleanField(default=False, verbose_name='Domain Data')),
                ('domain_software', models.BooleanField(default=False, verbose_name='Domain Software')),
                ('status', models.CharField(choices=[('active', 'Active'), ('deleted', 'Deleted')], default='active', max_length=7, verbose_name='Status')),
                ('maintainer', models.TextField(blank=True, null=True, verbose_name='Maintainer')),
                ('od_conformance', models.CharField(choices=[('approved', 'Approved'), ('not reviewed', 'Not reviewed'), ('rejected', 'Rejected')], default='not reviewed', max_length=30, verbose_name='Open Definition Conformance')),
                ('osd_conformance', models.CharField(choices=[('approved', 'Approved'), ('not reviewed', 'Not reviewed'), ('rejected', 'Rejected')], default='not reviewed', max_length=30, verbose_name='Open Source Definition Conformance')),
            ],
            options={
                'verbose_name': 'Licence',
                'verbose_name_plural': 'Licences',
            },
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legal_name', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Dénomination sociale')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
                ('ckan_id', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Ckan UUID')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Site internet')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Adresse e-mail')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/', verbose_name='Logo')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Adresse')),
                ('postcode', models.CharField(blank=True, max_length=100, null=True, verbose_name='Code postal')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ville')),
                ('phone', models.CharField(blank=True, max_length=10, null=True, verbose_name='Téléphone')),
                ('is_active', models.BooleanField(default=False, verbose_name='Organisation active')),
                ('is_crige_partner', models.BooleanField(default=False, verbose_name='Organisation partenaire IDGO')),
                ('geonet_id', models.TextField(blank=True, db_index=True, null=True, unique=True, verbose_name='UUID de la métadonnées')),
                ('sid_id', models.TextField(blank=True, db_index=True, null=True, unique=True, verbose_name='Référence du socle identité')),
                ('license', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sid.License', verbose_name='Licence')),
            ],
            options={
                'verbose_name': 'Organisation',
                'verbose_name_plural': 'Organisations',
                'ordering': ('slug',),
            },
        ),
        migrations.CreateModel(
            name='OrganisationType',
            fields=[
                ('code', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Code')),
                ('name', models.TextField(verbose_name="Type d'organisation")),
            ],
            options={
                'verbose_name': "Type d'organisation",
                'verbose_name_plural': "Types d'organisations",
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=10, null=True, verbose_name='Téléphone')),
                ('is_active', models.BooleanField(default=False, verbose_name='Validation suite à confirmation par e-mail')),
                ('membership', models.BooleanField(default=False, verbose_name='Utilisateur rattaché à une organisation')),
                ('crige_membership', models.BooleanField(default=False, verbose_name='Utilisateur partenaire IDGO')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Administrateur métier')),
                ('sftp_password', models.CharField(blank=True, max_length=10, null=True, verbose_name='Mot de passe sFTP')),
                ('sid_id', models.TextField(blank=True, db_index=True, null=True, unique=True, verbose_name='Référence du socle identité')),
                ('contributions', models.ManyToManyField(related_name='profile_contributions', through='sid.LiaisonsContributeurs', to='sid.Organisation', verbose_name="Organisation dont l'utilisateur est contributeur")),
                ('organisation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sid.Organisation', verbose_name="Organisation d'appartenance")),
                ('referents', models.ManyToManyField(related_name='profile_referents', through='sid.LiaisonsReferents', to='sid.Organisation', verbose_name="Organisation dont l'utilisateur est réferent")),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profil utilisateur',
                'verbose_name_plural': 'Profils des utilisateurs',
            },
        ),
        migrations.AddField(
            model_name='organisation',
            name='organisation_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sid.OrganisationType', verbose_name="Type d'organisation"),
        ),
        migrations.AddField(
            model_name='liaisonsreferents',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sid.Organisation', verbose_name='Organisation'),
        ),
        migrations.AddField(
            model_name='liaisonsreferents',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sid.Profile', verbose_name='Profil utilisateur'),
        ),
        migrations.AddField(
            model_name='liaisonscontributeurs',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sid.Organisation', verbose_name='Organisation'),
        ),
        migrations.AddField(
            model_name='liaisonscontributeurs',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sid.Profile', verbose_name='Profil utilisateur'),
        ),
        migrations.AlterUniqueTogether(
            name='liaisonsreferents',
            unique_together=set([('profile', 'organisation')]),
        ),
        migrations.AlterUniqueTogether(
            name='liaisonscontributeurs',
            unique_together=set([('profile', 'organisation')]),
        ),
    ]
