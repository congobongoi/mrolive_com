# Generated by Django 2.2.4 on 2022-10-13 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0062_auto_20221013_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wotask',
            name='sysur_signoff',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='wotask',
            name='sysur_signoff2',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
