# Generated by Django 2.2.4 on 2022-02-01 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0029_auto_20220121_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='wotask',
            name='si_number',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='wotask',
            name='sysur_auto_key',
            field=models.IntegerField(blank=True, default='0', null=True, verbose_name='sysur_auto_key from Quantum'),
        ),
        migrations.AddField(
            model_name='wotask',
            name='task_master_desc',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
