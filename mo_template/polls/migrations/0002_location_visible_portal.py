# Generated by Django 2.2.4 on 2020-11-12 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='visible_portal',
            field=models.BooleanField(default=1, verbose_name='IQ Enable (sets cart null)'),
        ),
    ]
