# Generated by Django 2.2.4 on 2022-07-01 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0052_auto_20220627_2302'),
    ]

    operations = [
        migrations.AddField(
            model_name='wostatus',
            name='po_number',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='wostatus',
            name='ro_number',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
