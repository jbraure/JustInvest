# Generated by Django 2.2 on 2019-04-23 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=20, verbose_name='Ticker')),
                ('currency', models.CharField(max_length=5, verbose_name='Currency')),
                ('purchase_date', models.DateTimeField(auto_now=True, verbose_name='Date purchased')),
                ('sell_date', models.DateTimeField(verbose_name='Date sold')),
                ('number_of_shares', models.IntegerField(default=1, verbose_name='Number of shares')),
                ('owner', models.EmailField(max_length=254)),
                ('price', models.FloatField()),
            ],
        ),
    ]