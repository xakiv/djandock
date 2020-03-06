# Generated by Django 2.2.9 on 2020-03-06 14:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geocontrib', '0002_auto_20200218_1343'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.PositiveSmallIntegerField(unique=True, verbose_name='Rang')),
                ('project_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='switch_projects_from', to='geocontrib.Project')),
                ('project_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='switch_projects_to', to='geocontrib.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
