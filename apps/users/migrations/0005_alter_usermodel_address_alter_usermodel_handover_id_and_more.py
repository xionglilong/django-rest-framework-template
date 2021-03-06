# Generated by Django 4.0.6 on 2022-07-20 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_departmentmodel_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='address',
            field=models.CharField(blank=True, default='', help_text='住址', max_length=100, verbose_name='住址'),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='handover_id',
            field=models.IntegerField(blank=True, default=0, verbose_name='数据交接人'),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='icon',
            field=models.ImageField(blank=True, default='head/default.png', help_text='头像路径', upload_to='head/%Y/%m', verbose_name='头像路径'),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='sex',
            field=models.BooleanField(blank=True, choices=[(1, '男'), (0, '女')], default=1, help_text='性别', verbose_name='性别'),
        ),
    ]
