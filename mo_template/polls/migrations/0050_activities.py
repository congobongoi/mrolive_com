# Generated by Django 2.2.4 on 2022-06-27 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0049_wostatus_alt_avail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('activity', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]