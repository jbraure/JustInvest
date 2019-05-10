# Generated by Django 2.2 on 2019-04-23 20:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trades', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trade',
            name='owner',
        ),
        migrations.AddField(
            model_name='trade',
            name='user',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='trade',
            name='purchase_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date purchased'),
        ),
    ]
