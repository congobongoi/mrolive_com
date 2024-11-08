# Generated by Django 2.2.4 on 2022-06-27 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0051_activities_condition_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartConditions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('condition_code', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='activities',
            name='condition_code',
        ),
    ]
