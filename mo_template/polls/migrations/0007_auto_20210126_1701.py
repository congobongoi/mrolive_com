# Generated by Django 2.2.4 on 2021-01-26 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20201223_1948'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='visible_portal',
            new_name='iq_enable',
        ),
    ]
