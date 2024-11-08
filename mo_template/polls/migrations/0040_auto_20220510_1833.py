# Generated by Django 2.2.4 on 2022-05-10 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0039_auto_20220504_1558'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDefAtts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('att_value', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('att_name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('att_type', models.CharField(blank=True, default='', max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='wostatus',
            name='att_name',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='wostatus',
            name='att_value',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
