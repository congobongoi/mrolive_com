# Generated by Django 2.2.4 on 2022-02-02 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0031_auto_20220202_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wotask',
            name='wot_labor_hours',
            field=models.FloatField(blank=True, default='0', max_length=200, null=True),
        ),
    ]
