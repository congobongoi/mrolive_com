# Generated by Django 2.2.4 on 2023-02-09 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0075_tasklabor_wot_auto_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklabor',
            name='sysur_auto_key',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
    ]
