# Generated by Django 2.2 on 2019-04-28 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0006_trade_total_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='currency',
            field=models.CharField(default='USD', max_length=5, verbose_name='Currency'),
        ),
        migrations.AlterField(
            model_name='trade',
            name='current_price',
            field=models.FloatField(default=0, verbose_name='Last close value'),
        ),
        migrations.AlterField(
            model_name='trade',
            name='total_value',
            field=models.FloatField(default=0, verbose_name='Total value'),
        ),
    ]
