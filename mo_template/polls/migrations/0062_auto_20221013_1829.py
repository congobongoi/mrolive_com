# Generated by Django 2.2.4 on 2022-10-13 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0061_remove_partconditions_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='wotask',
            name='sysur_signoff',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='wotask',
            name='sysur_signoff2',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
