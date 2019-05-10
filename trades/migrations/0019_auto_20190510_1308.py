# Generated by Django 2.2 on 2019-05-10 13:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0018_auto_20190510_1239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trade',
            name='purchase_date',
        ),
        migrations.AddField(
            model_name='trade',
            name='trade_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date'),
        ),
    ]