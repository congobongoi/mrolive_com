# Generated by Django 2.2.4 on 2022-09-23 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0056_laborbatch_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='wostatus',
            name='str_auto_key',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]