# Generated by Django 2.2.4 on 2023-02-28 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0076_tasklabor_sysur_auto_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrintSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('printer_name', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Printer')),
                ('computer_name', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Computer ID')),
                ('printnode_auth_key', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Print Node Auth Key')),
                ('print_width', models.FloatField(blank=True, default=8.5, max_length=200, null=True, verbose_name='Print Width')),
                ('print_length', models.FloatField(blank=True, default=11, max_length=200, null=True, verbose_name='Print Length')),
                ('print_tray', models.CharField(blank=True, default='1', max_length=200, null=True, verbose_name='Print Tray')),
            ],
        ),
        migrations.AddField(
            model_name='userappperms',
            name='printset_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.PrintSettings'),
        ),
    ]
