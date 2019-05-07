# Generated by Django 2.2 on 2019-05-03 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0008_auto_20190503_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='asset_class',
            field=models.CharField(default='Stock', max_length=50, verbose_name='Asset Class'),
        ),
        migrations.AlterField(
            model_name='trade',
            name='name',
            field=models.CharField(default='Apple', max_length=50, verbose_name='Name'),
        ),
    ]