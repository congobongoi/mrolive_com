# Generated by Django 2.2.4 on 2022-02-08 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0032_auto_20220202_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='laborbatch',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='laborbatch',
            name='stop_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
