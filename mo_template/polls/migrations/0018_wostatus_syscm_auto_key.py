# Generated by Django 2.2.4 on 2020-09-22 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0017_wostatus_dpt_auto_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='wostatus',
            name='syscm_auto_key',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
