# Generated by Django 2.2.4 on 2020-08-18 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20200818_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='columnsettings',
            name='tmpl_text',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]