# Generated by Django 4.2.4 on 2023-11-07 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0090_tasklabor_loc_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskSkills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('name', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('description', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('wok_auto_key', models.IntegerField(blank=True, default='0', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='computer_name',
        ),
        migrations.AddField(
            model_name='location',
            name='session_id',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='cart_code',
            field=models.CharField(blank=True, default='', max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='loc_code',
            field=models.CharField(blank=True, default='', max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='po_number',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='ro_number',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='smd_number',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='whs_code',
            field=models.CharField(blank=True, default='', max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='stockcart',
            name='session_id',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='tasklabor',
            name='wtl_auto_key',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_batch_no',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_ctrl_id',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_ctrl_number',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_cust_ref_number',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_customer',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_description',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_due_date',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_due_date_var',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_entry_date',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_gate_1_text',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_gate_2_text',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_gate_3_text',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_gate_4_text',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_gate_qty',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_location_code',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_manager',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_parent_wo',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_part_number',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_quantity',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_rack',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_rank',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_serial_number',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_status',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_stock_line',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_stock_owner',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True, verbose_name='Stock Owner'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_sub_wo_gate',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_time_loc',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_time_status',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_total_cost',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Total Cost'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_update_stamp',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_wh_code',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_wo_number',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_wo_type',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_wot_description',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_wot_labor_hours',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_wot_labor_last',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_wot_sequence',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_wot_status',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cw_wot_technician',
            field=models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='First Name'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_kiosk',
            field=models.BooleanField(default=False, verbose_name='Kiosk User'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='kiosk_check',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Kiosk Checked'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Last Name'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_key',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='User Key'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_name',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='User Name'),
        ),
        migrations.AddField(
            model_name='warehouse',
            name='session_id',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='wotask',
            name='skills_est_hours',
            field=models.FloatField(blank=True, default='0', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='queryapi',
            name='db_pwd',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='queryapi',
            name='db_user',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='queryapi',
            name='dj_user_id',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Django auth user id.'),
        ),
        migrations.AlterField(
            model_name='queryapi',
            name='host',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='queryapi',
            name='orcl_conn_id',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Oracle connect remote API connection id.(schema)'),
        ),
        migrations.AlterField(
            model_name='queryapi',
            name='port',
            field=models.IntegerField(blank=True, default=1521, null=True),
        ),
        migrations.AlterField(
            model_name='queryapi',
            name='sid',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='num_records',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='# of Records- Grid First Page'),
        ),
    ]
