# Generated by Django 3.1.2 on 2020-11-13 19:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0008_auto_20201112_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(default='', max_length=120, verbose_name='ناشر'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publish_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='تاریخ انتشار'),
        ),
    ]