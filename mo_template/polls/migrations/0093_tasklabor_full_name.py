# Generated by Django 4.2.4 on 2024-04-01 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0092_companies_session_id_departments_session_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklabor',
            name='full_name',
            field=models.CharField(blank=True, default='None', max_length=200, null=True),
        ),
    ]
