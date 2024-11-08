# Generated by Django 2.2.4 on 2023-03-01 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0078_auto_20230228_2347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userappperms',
            name='computer_name',
        ),
        migrations.RemoveField(
            model_name='userappperms',
            name='print_length',
        ),
        migrations.RemoveField(
            model_name='userappperms',
            name='print_tray',
        ),
        migrations.RemoveField(
            model_name='userappperms',
            name='print_width',
        ),
        migrations.RemoveField(
            model_name='userappperms',
            name='printer_name',
        ),
        migrations.RemoveField(
            model_name='userappperms',
            name='printnode_auth_key',
        ),
        migrations.AddField(
            model_name='mlapps',
            name='print_enabled',
            field=models.BooleanField(default=True, verbose_name='Print Enabled'),
        ),
    ]
