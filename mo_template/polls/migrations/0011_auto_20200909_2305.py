# Generated by Django 2.2.4 on 2020-09-09 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_oracleconnection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audittrail',
            name='description',
            field=models.CharField(default='', max_length=2200000),
        ),
        migrations.AlterField(
            model_name='audittrail',
            name='field_changed',
            field=models.CharField(default='', max_length=2000000),
        ),
        migrations.AlterField(
            model_name='audittrail',
            name='new_val',
            field=models.CharField(default='', max_length=2000000),
        ),
        migrations.AlterField(
            model_name='audittrail',
            name='status',
            field=models.CharField(blank=True, choices=[('success', 'Success'), ('failure', 'Failure'), ('either', 'Either')], default='failure', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='audittrail',
            name='user_id',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]
