# Generated by Django 2.2.4 on 2023-08-01 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0088_wostatus_exp_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklabor',
            name='batch_id',
            field=models.CharField(blank=True, default='None', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tasklabor',
            name='dept_name',
            field=models.CharField(blank=True, default='None', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tasklabor',
            name='skill_desc',
            field=models.CharField(blank=True, default='None', max_length=200, null=True),
        ),
    ]