# Generated by Django 4.0.6 on 2022-07-20 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_usermodel_address_alter_usermodel_handover_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='handover_id',
            field=models.IntegerField(default=0, verbose_name='数据交接人'),
        ),
    ]
