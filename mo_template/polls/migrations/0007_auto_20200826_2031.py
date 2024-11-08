# Generated by Django 2.2.4 on 2020-08-26 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20200826_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='companies',
            name='is_acc_co',
            field=models.BooleanField(default=0, verbose_name='Is Account Company'),
        ),
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dpt_auto_key', models.IntegerField(default=0)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('dj_user_id', models.IntegerField(default=0, verbose_name='Django auth user id.')),
                ('quapi_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.QueryApi')),
            ],
        ),
    ]
