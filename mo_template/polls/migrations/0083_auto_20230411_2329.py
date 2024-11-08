# Generated by Django 2.2.4 on 2023-04-11 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0082_operation'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='default_repair',
            field=models.BooleanField(default=False, verbose_name='Default Repair'),
        ),
        migrations.AddField(
            model_name='operation',
            name='session_id',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
