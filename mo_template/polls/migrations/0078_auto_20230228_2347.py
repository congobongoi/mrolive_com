# Generated by Django 2.2.4 on 2023-02-28 23:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0077_auto_20230228_2321'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PrintSettings',
            new_name='PrintSetting',
        ),
    ]
