# Generated by Django 2.2.4 on 2022-01-03 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0024_sale_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='mlapps',
            name='menu_seq',
            field=models.IntegerField(default=0, verbose_name='Menu sequence'),
        ),
        migrations.AddField(
            model_name='sale',
            name='customer',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='so_status',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='sos_auto_key',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
