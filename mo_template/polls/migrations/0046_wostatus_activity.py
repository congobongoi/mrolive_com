# Generated by Django 2.2.4 on 2022-05-11 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0045_userdefatts_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='wostatus',
            name='activity',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]