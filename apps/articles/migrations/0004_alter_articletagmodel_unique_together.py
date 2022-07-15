# Generated by Django 4.0.6 on 2022-07-15 22:10

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0003_alter_articlemodel_options_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='articletagmodel',
            unique_together={('owner', 'name')},
        ),
    ]
