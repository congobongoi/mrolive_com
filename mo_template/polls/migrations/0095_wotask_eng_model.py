# Generated by Django 4.2.4 on 2024-04-17 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0094_wotask_ac_model_wotask_ac_reg_wotask_ac_sn_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wotask',
            name='eng_model',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
