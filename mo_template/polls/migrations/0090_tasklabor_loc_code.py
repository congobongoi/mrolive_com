# Generated by Django 2.2.4 on 2023-08-02 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0089_auto_20230801_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklabor',
            name='loc_code',
            field=models.CharField(blank=True, default='None', max_length=200, null=True),
        ),
    ]
