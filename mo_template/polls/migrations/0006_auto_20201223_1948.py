# Generated by Django 2.2.4 on 2020-12-23 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_document_session_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wostatus',
            name='wot_sequence',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='wotask',
            name='wot_sequence',
            field=models.CharField(blank=True, default='0', max_length=200, null=True),
        ),
    ]