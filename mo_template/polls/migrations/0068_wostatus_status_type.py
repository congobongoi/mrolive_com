# Generated by Django 2.2.4 on 2022-12-12 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0067_auto_20221107_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='wostatus',
            name='status_type',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
