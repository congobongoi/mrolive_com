# Generated by Django 2.2.4 on 2020-11-12 14:40

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppModes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('code', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docfile', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='GridOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('col_width_dict', models.CharField(blank=True, default='', max_length=2000000000, null=True)),
                ('recs_per_page', models.IntegerField(default=25)),
            ],
        ),
        migrations.CreateModel(
            name='MLApps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('code', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('uri', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('audit_ok', models.BooleanField(default=False, verbose_name='Audit Trail OK')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
            ],
        ),
        migrations.CreateModel(
            name='MoTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opm_auto_key', models.IntegerField(default='', verbose_name='OPM AUTO KEY')),
                ('msg', models.CharField(default='', max_length=6000)),
                ('mo_number', models.CharField(default='', max_length=200)),
                ('is_debug', models.BooleanField(verbose_name='Debug On')),
                ('host', models.CharField(max_length=200)),
                ('port', models.IntegerField(default=1521)),
                ('sid', models.CharField(max_length=200)),
                ('db_user', models.CharField(max_length=200)),
                ('db_pwd', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='OracleConnection',
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
            ],
        ),
        migrations.CreateModel(
            name='PILogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_no', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('quantity', models.FloatField(blank=True, default=0, null=True)),
                ('batch', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('qty', models.FloatField(blank=True, default=0, null=True)),
                ('stock_label', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('ctrl_number', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('ctrl_id', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('location_code', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('user_id', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('session_id', models.CharField(blank=True, default='', max_length=2000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuantumUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, default='None', max_length=200, null=True, verbose_name='USER_ID from SYS_USERS table in QCTL.')),
                ('user_auto_key', models.IntegerField(default=0, verbose_name='User Key from Quantum DB')),
                ('pass_key', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('user_name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('employee_code', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('first_name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('last_name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('email', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('dj_user_id', models.IntegerField(blank=True, default=0, null=True, verbose_name='Django auth user id.')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='User Logo')),
            ],
        ),
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
            name='StatusSelection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wos_auto_key', models.IntegerField(default=0)),
                ('severity', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(max_length=200)),
                ('is_dashboard', models.BooleanField(default=1, verbose_name='Is Dashboard')),
                ('dj_user_id', models.IntegerField(default=0, verbose_name='Django auth user id.')),
                ('quapi_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.QueryApi')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.QuantumUser')),
            ],
        ),
        migrations.CreateModel(
            name='StockReceiver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rch_auto_key', models.IntegerField(blank=True, default=0, null=True)),
                ('rc_number', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('company_name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('order_type', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('order_number', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('create_date', models.DateTimeField(blank=True, default=datetime.date.today, null=True)),
                ('location_code', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('airway_bill', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('user_name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('account_company', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('session_id', models.CharField(blank=True, default='', max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WarehouseLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('location_code', models.CharField(max_length=200)),
                ('location_name', models.CharField(max_length=200)),
                ('whs_code', models.CharField(max_length=200)),
                ('whs_name', models.CharField(max_length=200)),
                ('bulk_imp_error', models.CharField(blank=True, default='', max_length=20000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WOTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ult_parent_woo', models.IntegerField(blank=True, default=0, null=True)),
                ('woo_auto_key', models.IntegerField(blank=True, default=0, null=True)),
                ('wot_auto_key', models.IntegerField(blank=True, default=0, null=True)),
                ('wot_sequence', models.IntegerField(blank=True, default=0, null=True)),
                ('wot_description', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('wot_status', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('wot_labor_hours', models.FloatField(blank=True, default='', max_length=200, null=True)),
                ('wot_labor_last', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('wot_technician', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('session_id', models.CharField(blank=True, default='', max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WOStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wot_est_hours', models.CharField(blank=True, default='', max_length=20000, null=True)),
                ('bulk_imp_error', models.CharField(blank=True, default='', max_length=20000, null=True)),
                ('task_close_reqs', models.CharField(blank=True, default='', max_length=20000, null=True)),
                ('task_title', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('task_position', models.CharField(blank=True, default='', max_length=20000, null=True)),
                ('task_ref', models.CharField(blank=True, default='', max_length=20000, null=True)),
                ('start_date', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Start Date')),
                ('wot_sequence', models.IntegerField(blank=True, default=0, null=True)),
                ('skill_desc', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('task_master_desc', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('cmp_auto_key', models.IntegerField(default=0)),
                ('next_num', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('syscm_auto_key', models.IntegerField(blank=True, default=0, null=True)),
                ('dpt_auto_key', models.IntegerField(blank=True, default=0, null=True)),
                ('qty_reserved', models.FloatField(blank=True, default=0, null=True)),
                ('airway_bill', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('pnm_modify', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('department', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('account_company', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('arrival_date', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Arrival Date')),
                ('notes', models.CharField(blank=True, default='', max_length=2000, null=True)),
                ('misc_cost', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('parts_cost', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('labor_cost', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('approved_date', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Quote Approved Date')),
                ('quoted_date', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Quote Received Date')),
                ('next_dlv_date', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Next Delivery Date')),
                ('total_cost', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Total Cost')),
                ('item_number', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Item')),
                ('sub_wo_gate', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('gate_qty', models.IntegerField(blank=True, default=0, null=True)),
                ('gate_1_text', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('gate_2_text', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('gate_3_text', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('gate_4_text', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('gate_1_qty', models.IntegerField(blank=True, default=0, null=True)),
                ('gate_2_qty', models.IntegerField(blank=True, default=0, null=True)),
                ('gate_3_qty', models.IntegerField(blank=True, default=0, null=True)),
                ('gate_4_qty', models.IntegerField(blank=True, default=0, null=True)),
                ('stock_owner', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Stock Owner')),
                ('is_toll', models.BooleanField(blank=True, default=0, null=True)),
                ('is_detail', models.BooleanField(blank=True, default=0, null=True)),
                ('is_repair_order', models.BooleanField(blank=True, default=0, null=True)),
                ('wo_number', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('parent_wo', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('parent_auto_key', models.IntegerField(blank=True, default=0, null=True)),
                ('woo_auto_key', models.IntegerField(blank=True, default=0, null=True)),
                ('stm_auto_key', models.IntegerField(blank=True, default=0, null=True)),
                ('wos_auto_key', models.IntegerField(blank=True, default=0, null=True)),
                ('wot_auto_key', models.IntegerField(blank=True, default=0, null=True)),
                ('rod_auto_key', models.IntegerField(blank=True, default=0, null=True)),
                ('wo_task', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('supdate_msg', models.CharField(blank=True, default='', max_length=6000, null=True)),
                ('time_status', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('status', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('due_date', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('entry_date', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('stock_line', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('part_number', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('description', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('serial_number', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('location_code', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('condition_code', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('wh_code', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('time_loc', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('user_id', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('need_date_variance', models.IntegerField(blank=True, default=0, null=True)),
                ('due_date_var', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('update_stamp', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('customer', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('vendor', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Vendor')),
                ('manager', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('rank', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('wo_type', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('cust_ref_number', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('is_dashboard', models.BooleanField(blank=True, default=1, null=True)),
                ('is_racking', models.BooleanField(blank=True, default=0, null=True)),
                ('session_id', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('rack', models.CharField(blank=True, default='none set', max_length=200, null=True)),
                ('ctrl_number', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('ctrl_id', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('quantity', models.FloatField(blank=True, default=0, null=True)),
                ('app_mode', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('priority', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('mode_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.AppModes')),
                ('quapi_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.QueryApi')),
                ('reg_user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.QuantumUser')),
                ('status_key', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.StatusSelection')),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whs_auto_key', models.IntegerField(default=0)),
                ('loc_auto_key', models.IntegerField(default=0)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('warehouse_code', models.CharField(blank=True, max_length=200, null=True)),
                ('dj_user_id', models.IntegerField(default=0, verbose_name='Django auth user id.')),
                ('quapi_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.QueryApi')),
            ],
        ),
        migrations.CreateModel(
            name='UserQuapiRel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dj_user_id', models.IntegerField(blank=True, default=0, null=True, verbose_name='Django admin user id.')),
                ('dj_username', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('global_access', models.BooleanField(default=True, verbose_name='Global Access')),
                ('quapi_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.QueryApi')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(upload_to='', verbose_name='User Logo')),
                ('sysur_auto_key', models.IntegerField(blank=True, default='0', null=True, verbose_name='sysur_auto_key from Quantum')),
                ('num_records', models.IntegerField(blank=True, null=True, verbose_name='# of Records- Grid First Page')),
                ('cw_total_cost', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Total Cost')),
                ('cw_sub_wo_gate', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_gate_qty', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_gate_1_text', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_gate_2_text', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_gate_3_text', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_gate_4_text', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_wo_number', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_parent_wo', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_time_status', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_status', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_due_date', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_entry_date', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_stock_line', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_part_number', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_description', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_serial_number', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_stock_owner', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True, verbose_name='Stock Owner')),
                ('cw_location_code', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_wh_code', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_time_loc', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_due_date_var', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_update_stamp', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_customer', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_manager', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_rank', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_wo_type', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_cust_ref_number', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_rack', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_ctrl_number', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_ctrl_id', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_quantity', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_batch_no', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_wot_sequence', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_wot_description', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_wot_status', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_wot_labor_hours', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_wot_labor_last', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_wot_technician', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='narrow', max_length=200, null=True)),
                ('cw_approved_date', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='80', max_length=200, null=True)),
                ('cw_quoted_date', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='80', max_length=2000, null=True)),
                ('cw_item_number', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='80', max_length=200, null=True)),
                ('cw_condition_code', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='80', max_length=200, null=True)),
                ('cw_misc_cost', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='80', max_length=200, null=True)),
                ('cw_parts_cost', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='80', max_length=200, null=True)),
                ('cw_labor_cost', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='80', max_length=200, null=True)),
                ('cw_notes', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='80', max_length=200, null=True)),
                ('cw_next_dlv_date', models.CharField(choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='80', max_length=200, null=True, verbose_name='Next Delivery Date')),
                ('cw_vendor', models.CharField(blank=True, choices=[('80', 'Narrow'), ('medium', 'Medium'), ('wide', 'Wide')], default='80', max_length=200, null=True, verbose_name='Vendor')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserAppPerms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dj_group_id', models.IntegerField(blank=True, default=0, null=True)),
                ('dj_user_id', models.IntegerField(blank=True, default=0, null=True, verbose_name='Django admin user id.')),
                ('dj_username', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('global_access', models.BooleanField(default=True, verbose_name='Global Access')),
                ('audit_ok', models.BooleanField(default=False, verbose_name='Audit Trail OK')),
                ('ml_apps_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.MLApps')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StockCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('udl_auto_key', models.IntegerField(default=0)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('udl_code', models.CharField(max_length=200)),
                ('dj_user_id', models.IntegerField(default=0, verbose_name='Django auth user id.')),
                ('quapi_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.QueryApi')),
            ],
        ),
        migrations.AddField(
            model_name='quantumuser',
            name='quapi_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.QueryApi'),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loc_auto_key', models.IntegerField(default=0)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('location_code', models.CharField(max_length=200)),
                ('dj_user_id', models.IntegerField(default=0, verbose_name='Django auth user id.')),
                ('quapi_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.QueryApi')),
            ],
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
        migrations.CreateModel(
            name='CustomProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_logo', models.ImageField(upload_to='', verbose_name='User Logo')),
                ('admin_user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cmp_auto_key', models.IntegerField(default=0)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('is_vendor', models.BooleanField(default=0, verbose_name='Is Vendor')),
                ('is_customer', models.BooleanField(default=0, verbose_name='Is Customer')),
                ('is_acc_co', models.BooleanField(default=0, verbose_name='Is Account Company')),
                ('dj_user_id', models.IntegerField(default=0, verbose_name='Django auth user id.')),
                ('quapi_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.QueryApi')),
            ],
        ),
        migrations.CreateModel(
            name='ColumnSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('field', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('type', models.CharField(blank=True, max_length=200, null=True)),
                ('session_id', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('width', models.FloatField(blank=True, default='', max_length=200, null=True)),
                ('tmpl_text', models.CharField(blank=True, max_length=200, null=True)),
                ('seq_num', models.IntegerField(default=0)),
                ('groptions_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.GridOptions')),
            ],
        ),
        migrations.CreateModel(
            name='AuditTrail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(blank=True, default=datetime.date.today, null=True)),
                ('write_date', models.DateTimeField(blank=True, default=datetime.date.today, null=True)),
                ('field_changed', models.CharField(default='', max_length=2000000)),
                ('new_val', models.CharField(default='', max_length=2000000)),
                ('description', models.CharField(default='', max_length=2200000)),
                ('user_id', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('status', models.CharField(blank=True, choices=[('success', 'Success'), ('failure', 'Failure'), ('either', 'Either')], default='failure', max_length=20, null=True)),
                ('ml_apps_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.MLApps')),
                ('quapi_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.QueryApi')),
            ],
        ),
        migrations.AddField(
            model_name='appmodes',
            name='ml_apps_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.MLApps'),
        ),
    ]
