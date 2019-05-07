# Generated by Django 2.2 on 2019-05-03 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0007_auto_20190428_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='name',
            field=models.CharField(default='Apple', max_length=50, verbose_name='Ticker'),
        ),
        migrations.AlterField(
            model_name='trade',
            name='ticker',
            field=models.CharField(default='AAPL', max_length=20, verbose_name='Ticker'),
        ),
    ]