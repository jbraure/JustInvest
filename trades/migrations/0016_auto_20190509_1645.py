# Generated by Django 2.2 on 2019-05-09 16:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0015_auto_20190509_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='trade_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date'),
        ),
    ]