# Generated by Django 2.2 on 2019-04-25 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0005_auto_20190425_0429'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='total_value',
            field=models.FloatField(default=0, verbose_name='Total value'),
            preserve_default=False,
        ),
    ]
