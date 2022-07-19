# Generated by Django 4.0.6 on 2022-07-20 00:48

import articles.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0003_alter_articletagmodel_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articletagmodel',
            options={'ordering': ('-update_time',), 'verbose_name': '文章标签', 'verbose_name_plural': '文章标签'},
        ),
        migrations.AlterField(
            model_name='articlemodel',
            name='owner',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='articles', to=settings.AUTH_USER_MODEL, verbose_name='创建人'),
        ),
        migrations.AlterField(
            model_name='articletagmodel',
            name='owner',
            field=models.ForeignKey(db_constraint=False, help_text='创建人自动填充', on_delete=models.SET(articles.models.get_sentinel_user), related_name='tags', to=settings.AUTH_USER_MODEL, verbose_name='创建人'),
        ),
    ]