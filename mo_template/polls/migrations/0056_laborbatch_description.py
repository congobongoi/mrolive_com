# Generated by Django 2.2.4 on 2022-09-13 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0055_auto_20220831_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='laborbatch',
            name='description',
            field=models.CharField(blank=True, default='None', max_length=200, null=True),
        ),
    ]
