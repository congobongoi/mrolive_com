# Generated by Django 2.2.4 on 2020-09-23 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0018_wostatus_syscm_auto_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='wostatus',
            name='next_num',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
