# Generated by Django 4.0.6 on 2022-07-19 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0003_alter_familymodel_options_alter_personmodel_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familymodel',
            name='person',
            field=models.ForeignKey(help_text='所属人', on_delete=django.db.models.deletion.CASCADE, related_name='families', to='persons.personmodel', verbose_name='所属人'),
        ),
    ]
