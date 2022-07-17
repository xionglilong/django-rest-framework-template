# Generated by Django 4.0.6 on 2022-07-17 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goodcategorymodel',
            old_name='add_time',
            new_name='create_time',
        ),
        migrations.RenameField(
            model_name='goodmodel',
            old_name='add_time',
            new_name='create_time',
        ),
        migrations.AlterField(
            model_name='goodcategorymodel',
            name='parent_category',
            field=models.ForeignKey(blank=True, help_text='父目录', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_category', to='goods.goodcategorymodel', verbose_name='父目录'),
        ),
        migrations.AlterField(
            model_name='goodmodel',
            name='front_image',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to='goods/images/', verbose_name='封面图'),
        ),
        migrations.AlterField(
            model_name='goodmodel',
            name='good_sn',
            field=models.CharField(default='', max_length=50, unique=True, verbose_name='商品唯一货号'),
        ),
    ]