# Generated by Django 2.2.4 on 2023-04-11 22:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0081_userappperms_default_repair'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opm_auto_key', models.IntegerField(default='', verbose_name='OPM Key')),
                ('version', models.CharField(default='', max_length=200)),
                ('operation_id', models.CharField(default='', max_length=200)),
                ('exp_date', models.DateField(blank=True, default=datetime.date.today, null=True)),
            ],
        ),
    ]
