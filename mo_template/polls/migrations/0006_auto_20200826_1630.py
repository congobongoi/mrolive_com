# Generated by Django 2.2.4 on 2020-08-26 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20200824_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='wostatus',
            name='account_company',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='wostatus',
            name='department',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]