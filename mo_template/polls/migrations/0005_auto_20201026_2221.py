# Generated by Django 2.2.4 on 2020-10-26 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_warehouselocation_session_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warehouselocation',
            name='loc_id',
        ),
        migrations.RemoveField(
            model_name='warehouselocation',
            name='whs_id',
        ),
    ]