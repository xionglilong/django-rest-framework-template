# Generated by Django 4.0.6 on 2022-07-18 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0003_alter_familymodel_options_familymodel_create_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='familymodel',
            options={'ordering': ('-create_time',), 'verbose_name': '家庭成员', 'verbose_name_plural': '家庭成员'},
        ),
        migrations.AlterModelOptions(
            name='personmodel',
            options={'ordering': ('-create_time',), 'verbose_name': '人员信息表', 'verbose_name_plural': '人员信息表'},
        ),
    ]
