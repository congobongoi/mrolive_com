# Generated by Django 2.2.4 on 2023-08-01 17:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0087_statusselection_session_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='wostatus',
            name='exp_date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
    ]
