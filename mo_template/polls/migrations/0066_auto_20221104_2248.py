# Generated by Django 2.2.4 on 2022-11-04 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0065_auto_20221101_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='wostatus',
            name='cond_level',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='User Logo'),
        ),
    ]
