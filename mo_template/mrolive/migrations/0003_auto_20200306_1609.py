# Generated by Django 2.2.4 on 2020-03-06 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mrolive', '0002_auto_20200306_1559'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueryApi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('conn_str', models.CharField(blank=True, max_length=200, null=True)),
                ('schema', models.CharField(blank=True, max_length=200, null=True)),
                ('url', models.CharField(blank=True, max_length=2000, null=True)),
                ('key', models.CharField(blank=True, max_length=200, null=True)),
                ('secret', models.CharField(blank=True, max_length=200, null=True)),
                ('host', models.CharField(max_length=200)),
                ('port', models.IntegerField(default=1521)),
                ('sid', models.CharField(max_length=200)),
                ('db_user', models.CharField(max_length=200)),
                ('db_pwd', models.CharField(max_length=200)),
                ('dj_user_id', models.IntegerField(default=0, verbose_name='Django auth user id.')),
                ('orcl_conn_id', models.IntegerField(default=0, verbose_name='Oracle connect remote API connection id.(schema)')),
            ],
        ),
        migrations.CreateModel(
            name='UserQuapiRel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dj_user_id', models.IntegerField(blank=True, default=0, null=True, verbose_name='Django admin user id.')),
                ('dj_username', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('global_access', models.BooleanField(default=True, verbose_name='Global Access')),
                ('quapi_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mrolive.QueryApi')),
            ],
        ),
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.DeleteModel(
            name='WOStatusConnect',
        ),
        migrations.RemoveField(
            model_name='userappperms',
            name='reg_user_id',
        ),
        migrations.AddField(
            model_name='pilogs',
            name='batch',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='pilogs',
            name='qty',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='pilogs',
            name='session_id',
            field=models.CharField(blank=True, default='', max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='statusselection',
            name='dj_user_id',
            field=models.IntegerField(default=0, verbose_name='Django auth user id.'),
        ),
        migrations.AddField(
            model_name='userappperms',
            name='dj_group_id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='userappperms',
            name='dj_user_id',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Django admin user id.'),
        ),
        migrations.AddField(
            model_name='userappperms',
            name='dj_username',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='wostatus',
            name='reg_user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mrolive.QuantumUser'),
        ),
        migrations.AlterField(
            model_name='pilogs',
            name='batch_no',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='pilogs',
            name='ctrl_id',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='pilogs',
            name='ctrl_number',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='pilogs',
            name='quantity',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='pilogs',
            name='stock_label',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='pilogs',
            name='user_id',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.AddField(
            model_name='audittrail',
            name='quapi_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mrolive.QueryApi'),
        ),
    ]
