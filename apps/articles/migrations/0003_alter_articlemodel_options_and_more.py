# Generated by Django 4.0.6 on 2022-07-18 18:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlemodel',
            options={'ordering': ('-create_time',), 'verbose_name': '文章管理', 'verbose_name_plural': '文章管理'},
        ),
        migrations.AlterModelOptions(
            name='articletagmodel',
            options={'ordering': ('-create_time',), 'verbose_name': '文章标签表', 'verbose_name_plural': '文章标签表'},
        ),
        migrations.AlterField(
            model_name='articlemodel',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='article', to=settings.AUTH_USER_MODEL, verbose_name='创建人'),
        ),
        migrations.AlterField(
            model_name='articletagmodel',
            name='owner',
            field=models.ForeignKey(help_text='创建人自动填充', on_delete=django.db.models.deletion.CASCADE, related_name='article_tag', to=settings.AUTH_USER_MODEL, verbose_name='创建人'),
        ),
    ]
