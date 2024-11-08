import datetime
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User,Group,AbstractUser
from django.contrib import admin
# Create your models here.

class Document(models.Model):
    docfile = models.FileField()
    #fields to store the images/pdfs retrieved from Quantum's file/image server
    source_pk = models.IntegerField(default=80) 
    source_table = models.CharField(blank=True,null=True,default="",max_length=120)
    server_url = models.CharField(blank=True,null=True,default="",max_length=120)
    server_port = models.IntegerField(default=80) 
    url_path = models.CharField(blank=True,null=True,default="",max_length=120)
    file_name = models.CharField(blank=True,null=True,default="",max_length=120)
    file_extension = models.CharField(blank=True,null=True,default="",max_length=20)
    file_key = models.IntegerField(default=1)
    #pdf=models.FileField(upload_to='uploads/', null=True, blank=True)
    #app_id = models.ForeignKey(MLApps, on_delete=models.CASCADE, blank=True, null=True) 
    session_id = models.CharField(blank=True, null=True, max_length=200, default="")

class OracleConnection(models.Model):
 
    name = models.CharField(max_length=200, default="", blank=True, null=True)
    conn_str = models.CharField(max_length=200, blank=True, null=True)
    schema = models.CharField(max_length=200, blank=True, null=True)
    url = models.CharField(max_length=2000, blank=True, null=True)
    key = models.CharField(max_length=200, blank=True, null=True)
    secret = models.CharField(max_length=200, blank=True, null=True)
    host = models.CharField(max_length=200)
    port = models.IntegerField(default=1521)
    sid = models.CharField(max_length=200)
    db_user = models.CharField(max_length=200)
    db_pwd = models.CharField(max_length=200)
    dj_user_id = models.IntegerField('Django auth user id.',default=0)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class UserGroupProfile(models.Model):
    quantum_cmp_key = models.IntegerField('Quantum Company Key', blank=True, null=True, default="0")
    group = models.OneToOneField(Group, on_delete=models.CASCADE, blank=True, null=True)
    conn_string = models.CharField('Phone Home Connection String', blank=True, null=True, max_length=200, default="")
    private_key = models.TextField('Private Key', blank=True, null=True, max_length=300, default="")
    public_key = models.TextField('Public Key', blank=True, null=True, max_length=300, default="")
    priority = models.CharField(blank=True, null=True, max_length=40, default="lowest_priority", choices = (('lowest_priority','Lowest Priority'),('highest_priority','Highest Priority')))
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
        
    def __str__(self):
        return self.group.name
        
class MLApps(models.Model):
    menu_seq = models.IntegerField('Menu sequence',default=0) 
    types = (('operations','Operations'),('management','Management'),('dashboards','Dashboards'),('setup','Setup'),('exports','Exports'))
    name = models.CharField(max_length=200, default="", blank=True, null=True)
    code = models.CharField(max_length=200, default="", blank=True, null=True)
    uri = models.CharField(max_length=200, default="", blank=True, null=True)
    audit_ok = models.BooleanField('Audit Trail OK', default=False) 
    app_type = models.CharField(blank=True, null=True, choices = types, max_length=200, default='operations') 
    active = models.BooleanField('Active', default=True)
    print_enabled = models.BooleanField('Print Enabled', default=False)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name     
        
class UserProfile(models.Model):
    kiosk_check = models.CharField('Kiosk Checked', blank=True, null=True, max_length=200, default="")
    sizes = (('80','Narrow'),('medium','Medium'),('wide','Wide'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    logo = models.ImageField('User Logo',blank=True, null=True)
    sysur_auto_key = models.IntegerField('sysur_auto_key from Quantum',blank=True, null=True,default="0") 
    kiosk_apps = models.ManyToManyField(MLApps, blank=True, null=True)
    user_name = models.CharField('User Name', blank=True, null=True, max_length=200, default="")
    first_name = models.CharField('First Name', blank=True, null=True, max_length=200, default="")
    last_name = models.CharField('Last Name', blank=True, null=True, max_length=200, default="")
    user_key = models.IntegerField('User Key',blank=True, null=True, default=0)
    email = models.CharField('Email', blank=True, null=True, max_length=200, default="")
    is_kiosk = models.BooleanField('Kiosk User', default=False)
    num_records = models.IntegerField('# of Records- Grid First Page',blank=True, null=True, default=0)
    cw_total_cost = models.CharField('Total Cost',blank=True, null=True, max_length=200, default="")
    cw_item_number = models.CharField('Item',blank=True, null=True, max_length=200, default="")
    cw_sub_wo_gate = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_gate_qty = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_gate_1_text = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_gate_2_text = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_gate_3_text = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_gate_4_text = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_wo_number = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_parent_wo = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_time_status = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_status = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_due_date = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_entry_date = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_stock_line = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_part_number = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_description = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_serial_number = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_stock_owner = models.CharField('Stock Owner', blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_location_code = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_condition_code = models.CharField('Part Condition Code',blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_wh_code = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_time_loc = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_due_date_var = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_update_stamp = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_customer = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_manager = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_rank = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_wo_type = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_cust_ref_number = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_rack = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_ctrl_number = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_ctrl_id = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')   
    cw_quantity = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')  
    cw_batch_no = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow') 
    cw_wot_sequence = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_wot_description = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow') 
    cw_wot_status = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow')
    cw_wot_labor_hours = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow') 
    cw_wot_labor_last = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow') 
    cw_wot_technician = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='narrow') 
    cw_approved_date = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='80') 
    cw_quoted_date = models.CharField(blank=True, null=True, choices = sizes, max_length=2000, default='80') 
    cw_item_number = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='80') 
    cw_condition_code = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='80') 
    cw_misc_cost = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='80') 
    cw_parts_cost = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='80') 
    cw_labor_cost = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='80') 
    cw_notes = models.CharField(blank=True, null=True, choices = sizes, max_length=200, default='80') 
    cw_next_dlv_date = models.CharField('Next Delivery Date', choices = sizes, null=True, max_length=200, default='80')    
    cw_vendor = models.CharField('Vendor',blank=True, null=True, choices = sizes, max_length=200, default="80")
    
    def save(self, *args, **kwargs):
        user = self.user
        if user:
            self.user_name = user.username
            self.first_name = user.first_name
            self.last_name = user.last_name
            self.email = user.email
            self.user_key = user.id
            is_kiosk = False
            kiosk_check = 'blank.png'
            #check apps that are kiosk user apps and return the flag in the view to prompt for user_id
            for app in self.kiosk_apps.all():
                if app.code == 'labor-tracking':  
                    is_kiosk = True
                    kiosk_check = "green-check.png"
                    break
            self.is_kiosk = is_kiosk
            self.kiosk_check = kiosk_check
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username  

class Operation(models.Model):
    session_id = models.CharField(blank=True, null=True, max_length=200, default="")
    opm_auto_key = models.IntegerField('OPM Key', default="")
    version = models.CharField(max_length=200, default="")
    operation_id = models.CharField(max_length=200, default="")
    exp_date = models.DateField(blank=True, null=True,default=datetime.date.today)
    default_repair = models.BooleanField('Default Repair', default=False)
    op_desc = models.CharField(max_length=200, default="")
    part_number = models.CharField(max_length=200, default="")
    part_desc = models.CharField(max_length=200, default="")
    
    def __str__(self):
        return self.operation_id       
        
class MoTemplate(models.Model):
    opm_auto_key = models.IntegerField('OPM AUTO KEY', default="")
    msg = models.CharField(max_length=6000, default="")
    mo_number = models.CharField(max_length=200, default="")
    is_debug = models.BooleanField('Debug On')
    host = models.CharField(max_length=200)
    port = models.IntegerField(default=1521)
    sid = models.CharField(max_length=200)
    db_user = models.CharField(max_length=200)
    db_pwd = models.CharField(max_length=200)
    
    def save(self, *args, **kwargs):
        self.db_pwd = make_password(self.db_pwd)
        super(MoTemplate, self).save(*args, **kwargs)
        
class TaskLabor(models.Model):
    sysur_auto_key = models.IntegerField(blank=True, null=True, default="0")
    session_id = models.CharField(blank=True, null=True, max_length=200, default="")
    wo_number = models.CharField(blank=True, null=True, max_length=200, default="None")
    wot_auto_key = models.IntegerField(blank=True, null=True, default=0) 
    wtl_auto_key = models.IntegerField(blank=True, null=True, default=0)     
    sequence = models.IntegerField(blank=True, null=True, default="0") 
    task_name = models.CharField(blank=True, null=True, max_length=200, default="None")
    task_desc = models.CharField(blank=True, null=True, max_length=200, default="None")
    pn = models.CharField(blank=True, null=True, max_length=200, default="None")
    part_desc = models.CharField(blank=True, null=True, max_length=200, default="None")
    loc_code = models.CharField(blank=True, null=True, max_length=200, default="None")    
    user_name = models.CharField(blank=True, null=True, max_length=200, default="None")
    entry_date = models.DateField(blank=True, null=True,default=datetime.date.today)
    hours = models.FloatField(blank=True, null=True, default="0.00")
    start_time = models.DateTimeField(blank=True, null=True)
    stop_time = models.DateTimeField(blank=True, null=True)
    batch_id = models.CharField(blank=True, null=True, max_length=200, default="None")
    dept_name = models.CharField(blank=True, null=True, max_length=200, default="None")
    skill_desc = models.CharField(blank=True, null=True, max_length=200, default="None")
    
    def __str__(self):
        return self.task_name

class TaskSkills(models.Model):
    session_id = models.CharField(blank=True, null=True, max_length=200, default="")
    name = models.CharField(blank=True, null=True, max_length=200, default="None")
    description = models.CharField(blank=True, null=True, max_length=200, default="None")     
    wok_auto_key = models.IntegerField(blank=True, null=True, default="0")
    
    def __str__(self):
        return str(self.description)        
        
class LaborBatch(models.Model):
    session_id = models.CharField(blank=True, null=True, max_length=200, default="")
    batch_id = models.CharField(blank=True, null=True, max_length=200, default="None")
    description = models.CharField(blank=True, null=True, max_length=200, default="None")     
    sysur_auto_key = models.IntegerField(blank=True, null=True, default="0") 
    start_time = models.DateTimeField(blank=True, null=True)
    stop_time = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return 'batch id: ' + str(self.batch_id)

        
class GridOptions(models.Model):
    session_id = models.CharField(blank=True, null=True, max_length=200, default="")
    col_width_dict = models.CharField(blank=True, null=True, max_length=2000000000, default="") 
    recs_per_page = models.IntegerField(default=25) 
    
class ColumnSettings(models.Model):
    name = models.CharField(max_length=200, default="", blank=True, null=True)
    field = models.CharField(max_length=200, default="", blank=True, null=True)
    type = models.CharField(max_length=200, blank=True, null=True)
    session_id = models.CharField(blank=True, null=True, max_length=200, default="")
    width = models.FloatField(blank=True, null=True, max_length=200, default="")
    tmpl_text = models.CharField(max_length=200, blank=True, null=True)
    seq_num = models.IntegerField(default=0)  
    groptions_id = models.ForeignKey(GridOptions, on_delete=models.CASCADE, blank=True, null=True)     
  
class QueryApi(models.Model):
 
    name = models.CharField(max_length=200, default="", blank=True, null=True)
    conn_str = models.CharField(max_length=200, blank=True, null=True)
    schema = models.CharField(max_length=200, blank=True, null=True)
    url = models.CharField(max_length=2000, blank=True, null=True)
    key = models.CharField(max_length=200, blank=True, null=True)
    secret = models.CharField(max_length=200, blank=True, null=True)
    host = models.CharField(max_length=200, blank=True, null=True)
    port = models.IntegerField(default=1521, blank=True, null=True)
    sid = models.CharField(max_length=200, blank=True, null=True)
    db_user = models.CharField(max_length=200, blank=True, null=True)
    db_pwd = models.CharField(max_length=200, blank=True, null=True)
    dj_user_id = models.IntegerField('Django auth user id.',default=0, blank=True, null=True) 
    orcl_conn_id = models.IntegerField('Oracle connect remote API connection id.(schema)',default=0, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name        
    
class QuantumUser(models.Model):
    quapi_id = models.ForeignKey(QueryApi, on_delete=models.CASCADE, blank=True, null=True)
    user_id = models.CharField('USER_ID from SYS_USERS table in QCTL.', max_length=200, default="None", blank=True, null=True)
    user_auto_key = models.IntegerField('User Key from Quantum DB', default=0)
    pass_key = models.CharField(max_length=200, default="", blank=True, null=True)
    user_name = models.CharField(max_length=200, default="", blank=True, null=True)
    employee_code = models.CharField(max_length=200, default="", blank=True, null=True)
    first_name = models.CharField(max_length=200, default="", blank=True, null=True)
    last_name = models.CharField(max_length=200, default="", blank=True, null=True)
    email = models.CharField(max_length=200, default="", blank=True, null=True)
    dj_user_id = models.IntegerField('Django auth user id.',default=0, blank=True, null=True) 
    logo = models.ImageField('User Logo', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user_name
   
class InlineImage(admin.TabularInline):
    model = QuantumUser

class UserAdmin(admin.ModelAdmin):
    inlines = [InlineImage]
    
class Companies(models.Model):
    quapi_id = models.ForeignKey(QueryApi, on_delete=models.CASCADE, blank=True, null=True)
    cmp_auto_key = models.IntegerField(default=0)
    name = models.CharField(blank=True, null=True, max_length=200)
    is_vendor = models.BooleanField('Is Vendor', default=0)
    is_customer = models.BooleanField('Is Customer', default=0)
    is_acc_co = models.BooleanField('Is Account Company', default=0)
    dj_user_id = models.IntegerField('Django auth user id.',default=0)    

    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
    
class Departments(models.Model):
    quapi_id = models.ForeignKey(QueryApi, on_delete=models.CASCADE, blank=True, null=True)
    dpt_auto_key = models.IntegerField(default=0)
    name = models.CharField(blank=True, null=True, max_length=200)
    dj_user_id = models.IntegerField('Django auth user id.',default=0)    

    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)          

class Location(models.Model):
    quapi_id = models.ForeignKey(QueryApi, on_delete=models.CASCADE, blank=True, null=True)
    loc_auto_key = models.IntegerField(default=0)
    name = models.CharField(blank=True, null=True, max_length=200)
    location_code = models.CharField(max_length=200)
    dj_user_id = models.IntegerField('Django auth user id.',default=0) 
    iq_enable = models.BooleanField('IQ Enable (sets cart null)', default=1)    

    def __str__(self):
        return self.location_code
        
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
        
class Warehouse(models.Model):
    quapi_id = models.ForeignKey(QueryApi, on_delete=models.CASCADE, blank=True, null=True)
    whs_auto_key = models.IntegerField(default=0)
    loc_auto_key = models.IntegerField(default=0)
    name = models.CharField(blank=True, null=True, max_length=200)
    warehouse_code = models.CharField(max_length=200, blank=True, null=True)
    dj_user_id = models.IntegerField('Django auth user id.',default=0)    

    def __str__(self):
        return self.warehouse_code
        
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
        
class WarehouseLocation(models.Model):
    session_id = models.CharField(blank=True, null=True, max_length=200, default="")
    #loc_id = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    #whs_id = models.ForeignKey(Warehouse, on_delete=models.CASCADE, blank=True, null=True) 
    location_code = models.CharField(max_length=200)
    location_name = models.CharField(max_length=200)
    whs_code = models.CharField(max_length=200)   
    whs_name = models.CharField(max_length=200) 
    bulk_imp_error = models.CharField(blank=True, null=True,max_length=20000, default="")    
    
    def __str__(self):
        return (self.location_code + ' ' + self.whs_code)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)        
        
class StockCart(models.Model):
    quapi_id = models.ForeignKey(QueryApi, on_delete=models.CASCADE, blank=True, null=True)
    udl_auto_key = models.IntegerField(default=0)
    name = models.CharField(blank=True, null=True, max_length=200)
    udl_code = models.CharField(max_length=200)
    dj_user_id = models.IntegerField('Django auth user id.',default=0)    

    def __str__(self):
        return self.udl_code
        
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
        
class StatusSelection(models.Model):
    session_id = models.CharField(blank=True, null=True, max_length=200, default="")
    quapi_id = models.ForeignKey(QueryApi, on_delete=models.CASCADE, blank=True, null=True)
    wos_auto_key = models.IntegerField(default=0)
    severity = models.CharField(blank=True, null=True, max_length=200)
    name = models.CharField(max_length=200)
    is_dashboard = models.BooleanField('Is Dashboard', default=1)
    user_id = models.ForeignKey(QuantumUser, on_delete=models.CASCADE, blank=True, null=True)
    dj_user_id = models.IntegerField('Django auth user id.',default=0) 
    
    def __str__(self):
        return self.name
        
    @classmethod
    def create(cls, wos_auto_key, severity, name):
        status = cls(wos_auto_key = wos_auto_key, severity = severity, name = name)
        status.save()
        return status 
        
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
   

class AppModes(models.Model):
    name = models.CharField(max_length=200, default="", blank=True, null=True)
    code = models.CharField(max_length=200, default="", blank=True, null=True)
    ml_apps_id = models.ForeignKey(MLApps, on_delete=models.CASCADE, blank=True, null=True)
    active = models.BooleanField('Active', default=True) 

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name  

class PrintSetting(models.Model): 
    orients = (('portait','Portrait'),('landscape','Landscape'))
    printer_name = models.CharField('Printer', blank=True, null=True, max_length=200, default="")
    computer_name = models.CharField('Computer ID', blank=True, null=True, max_length=200, default="")
    printnode_auth_key = models.CharField('Print Node Auth Key', blank=True, null=True, max_length=200, default="")
    print_width = models.FloatField('Print Width', blank=True, null=True, max_length=200, default=8.5)
    print_length = models.FloatField('Print Length', blank=True, null=True, max_length=200, default=11)
    print_tray = models.CharField('Print Tray', blank=True, null=True, max_length=200, default="1") 

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.computer_name + '-' + self.printer_name         
    
class UserAppPerms(models.Model):
    printset_id = models.ForeignKey(PrintSetting, on_delete=models.CASCADE, blank=True, null=True)
    default_repair = models.BooleanField("Default Repair", default=False)
    ml_apps_id = models.ForeignKey(MLApps, on_delete=models.CASCADE, blank=True, null=True)
    dj_group_id = models.IntegerField(blank=True, null=True, default=0)
    dj_user_id = models.IntegerField('Django admin user id.', blank=True, null=True, default=0)
    dj_username = models.CharField(max_length=200, default="", blank=True, null=True)     
    global_access = models.BooleanField('Global Access', default=True)
    audit_ok = models.BooleanField('Audit Trail OK', default=False) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
        
    def __str__(self):
        return (self.dj_username)
    
class UserQuapiRel(models.Model):
    quapi_id = models.ForeignKey(QueryApi, on_delete=models.CASCADE, blank=True, null=True)
    dj_user_id = models.IntegerField('Django admin user id.', blank=True, null=True, default=0)
    dj_username = models.CharField(max_length=200, default="", blank=True, null=True)     
    global_access = models.BooleanField('Global Access', default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
        
    def __str__(self):
        return (self.dj_username)
    
class AuditTrail(models.Model):
    create_date = models.DateTimeField(blank=True, null=True,default=datetime.date.today)
    write_date = models.DateTimeField(blank=True, null=True,default=datetime.date.today)
    field_changed = models.CharField(max_length=2000000, default="")
    new_val = models.CharField(max_length=2000000, default="")
    description = models.CharField(max_length=2200000, default="")
    quapi_id = models.ForeignKey(QueryApi, on_delete=models.CASCADE, blank=True, null=True)
    #quapi_db_id = models.IntegerField('Query API db ID that contains user and connection details.', blank=True, null=True, default=0)
    user_id = models.CharField(blank=True, null=True,max_length=20, default="")
    ml_apps_id = models.ForeignKey(MLApps, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(blank=True, null=True, max_length=20, default="failure", choices = (('success','Success'),('failure','Failure'),('either','Either')))
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
        
    def __str__(self):
        return self.description
        
class WOTask(models.Model):
    
    ult_parent_woo = models.IntegerField(blank=True, null=True, default=0)   
    woo_auto_key = models.IntegerField(blank=True, null=True, default=0) 
    wot_auto_key = models.IntegerField(blank=True, null=True, default=0)  
    wtm_auto_key = models.IntegerField(blank=True, null=True, default=0)        
    wot_sequence = models.IntegerField(blank=True, null=True, default=0)
    task_master_desc = models.CharField(blank=True, null=True, max_length=200, default="")
    wot_description = models.CharField(blank=True, null=True, max_length=200, default="") 
    wot_status = models.CharField(blank=True, null=True, max_length=200, default="") 
    status_type = models.CharField(blank=True, null=True, max_length=200, default="")
    skills_est_hours = models.FloatField(blank=True, null=True, max_length=200,default="0")
    wot_labor_hours = models.FloatField(blank=True, null=True, max_length=200,default="0") 
    wot_labor_last = models.CharField(blank=True, null=True, max_length=200, default="") 
    wot_technician = models.CharField(blank=True, null=True, max_length=200, default="")
    sysur_signoff = models.CharField(blank=True, null=True, max_length=200, default="")
    sysur_signoff2 = models.CharField(blank=True, null=True, max_length=200, default="")
    si_number = models.CharField(blank=True, null=True, max_length=200, default="")
    sysur_auto_key = models.IntegerField('sysur_auto_key from Quantum',blank=True, null=True,default="0") 
    session_id = models.CharField(blank=True, null=True, max_length=200, default="")
    
class StockReceiver(models.Model):
    
    rch_auto_key = models.IntegerField(blank=True, null=True, default=0) 
    rc_number = models.CharField(blank=True, null=True, max_length=200, default="") 
    company_name = models.CharField(blank=True, null=True, max_length=200, default="")
    order_type = models.CharField(blank=True, null=True, max_length=200, default="") 
    order_number = models.CharField(blank=True, null=True, max_length=200, default="") 
    create_date = models.DateTimeField(blank=True, null=True,default=datetime.date.today)
    location_code = models.CharField(blank=True, null=True, max_length=200, default="")
    airway_bill = models.CharField(blank=True, null=True, max_length=200, default="") 
    user_name = models.CharField(blank=True, null=True, max_length=200, default="") 
    account_company = models.CharField(blank=True, null=True, max_length=200, default="") 
    session_id = models.CharField(blank=True, null=True, max_length=200, default="")
 
class Sale(models.Model):
    so_number = models.CharField(blank=True, null=True, max_length=200, default="")  
    soh_auto_key = models.IntegerField(blank=True, null=True, default=0)
    so_status = models.CharField(blank=True, null=True, max_length=200, default="")  
    sos_auto_key = models.IntegerField(blank=True, null=True, default=0)
    customer = models.CharField(blank=True, null=True, max_length=200, default="")  
    cmp_auto_key = models.IntegerField(default=0)
    spn_auto_key = models.IntegerField(default=0)
    spn_code = models.CharField(blank=True,null=True,default="",max_length=120) 
    part_number = models.CharField(blank=True, null=True, max_length=200, default="")
    description = models.CharField(blank=True, null=True, max_length=200, default="") 
    priority = models.CharField(blank=True, null=True, max_length=200, default="")
    due_date = models.DateTimeField(blank=True, null=True,default=datetime.date.today)    
    session_id = models.CharField(blank=True, null=True, max_length=200, default="")

class PartNumbers(models.Model):
    session_id = models.CharField(blank=True, null=True, max_length=200, default="") 
    part_number = models.CharField(blank=True, null=True, max_length=200)
    description = models.CharField(blank=True, null=True, max_length=200)
    pnm_auto_key = models.IntegerField(blank=True, null=True, default=0) 

    def __str__(self):
        return self.part_number
        
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)    
    
class PartConditions(models.Model):
    session_id = models.CharField(blank=True, null=True, max_length=200, default="") 
    condition_code = models.CharField(blank=True, null=True, max_length=200)

    def __str__(self):
        return self.condition_code
        
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
        
class Consignments(models.Model):
    session_id = models.CharField(blank=True, null=True, max_length=200, default="") 
    code = models.CharField(blank=True, null=True, max_length=200)

    def __str__(self):
        return self.code
        
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs) 

class Activities(models.Model):
    session_id = models.CharField(blank=True, null=True, max_length=200, default="") 
    activity = models.CharField(blank=True, null=True, max_length=200)

    def __str__(self):
        return self.activity
        
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)    
    
class WOStatus(models.Model):
    exp_date = models.DateField(blank=True, null=True,default=datetime.date.today)
    cart=models.CharField(blank=True,null=True,default="",max_length=120)
    slug=models.CharField(blank=True,null=True,default="",max_length=120)
    pdf=models.FileField(upload_to='uploads/', null=True, blank=True)
    loc_validated_date = models.DateTimeField(blank=True,null=True,default=datetime.date.today)
    spn_code = models.CharField(blank=True,null=True,default="",max_length=120) 
    wot_est_hours = models.CharField(blank=True, null=True,max_length=20000, default="")
    bulk_imp_error = models.CharField(blank=True, null=True,max_length=20000, default="")
    task_close_reqs = models.CharField(blank=True, null=True,max_length=20000, default="")
    task_title = models.CharField(blank=True, null=True,max_length=200, default="")
    task_position = models.CharField(blank=True, null=True,max_length=20000, default="")
    task_ref = models.CharField(blank=True, null=True,max_length=20000, default="")
    start_date = models.DateField('Start Date',blank=True, null=True,default=datetime.date.today)
    wot_sequence = models.CharField(blank=True, null=True, max_length=200, default='')
    skill_desc = models.CharField(blank=True, null=True, max_length=200, default="")
    task_master_desc = models.CharField(blank=True, null=True, max_length=200, default="")
    cmp_auto_key = models.IntegerField(default=0)
    next_num = models.CharField(blank=True, null=True, max_length=200, default="")
    syscm_auto_key = models.IntegerField(blank=True, null=True, default=0)
    dpt_auto_key = models.IntegerField(blank=True, null=True, default=0)
    qty_oh = models.FloatField(blank=True, null=True, default=0)    
    qty_needed = models.FloatField(blank=True, null=True, default=0)
    qty_available = models.FloatField(blank=True, null=True, default=0)
    alt_avail = models.FloatField(blank=True, null=True, default=0)
    qty_reserved = models.FloatField(blank=True, null=True, default=0)
    airway_bill = models.CharField(blank=True, null=True, max_length=200, default="") 
    pnm_modify = models.CharField(blank=True, null=True, max_length=200, default="") 
    department = models.CharField(blank=True, null=True, max_length=200, default="") 
    account_company = models.CharField(blank=True, null=True, max_length=200, default="") 
    arrival_date = models.DateField('Arrival Date',blank=True, null=True,default=datetime.date.today)
    notes = models.CharField(blank=True, null=True, max_length=2000, default="")
    misc_cost = models.CharField(blank=True, null=True, max_length=200, default="")
    parts_cost = models.CharField(blank=True, null=True, max_length=200, default="")
    labor_cost = models.CharField(blank=True, null=True, max_length=200, default="")
    approved_date = models.DateField('Quote Approved Date',blank=True, null=True,default=datetime.date.today)
    quoted_date = models.DateField('Quote Received Date',blank=True, null=True,default=datetime.date.today)
    next_dlv_date = models.DateField('Next Delivery Date',blank=True, null=True,default=datetime.date.today)
    total_cost = models.CharField('Total Cost', blank=True, null=True, max_length=200, default="")
    item_number = models.CharField('Item',blank=True, null=True, max_length=200, default="")
    quapi_id = models.ForeignKey(QueryApi, on_delete=models.CASCADE, blank=True, null=True)
    int_rank = models.IntegerField(blank=True, null=True, default=0) 
    sub_wo_gate = models.CharField(blank=True, null=True, max_length=200, default="")
    gate_qty = models.IntegerField(blank=True, null=True, default=0) 
    gate_1_text = models.CharField(blank=True, null=True, max_length=200, default="")
    gate_2_text = models.CharField(blank=True, null=True, max_length=200, default="")
    gate_3_text = models.CharField(blank=True, null=True, max_length=200, default="")
    gate_4_text = models.CharField(blank=True, null=True, max_length=200, default="")
    gate_1_qty = models.IntegerField(blank=True, null=True, default=0) 
    gate_2_qty = models.IntegerField(blank=True, null=True, default=0) 
    gate_3_qty = models.IntegerField(blank=True, null=True, default=0) 
    gate_4_qty = models.IntegerField(blank=True, null=True, default=0) 
    stock_owner = models.CharField('Stock Owner',blank=True, null=True, max_length=200, default="")
    is_toll = models.BooleanField(blank=True, null=True, default=0)
    is_detail = models.BooleanField(blank=True, null=True, default=0)
    is_repair_order = models.BooleanField(blank=True, null=True, default=0)
    wo_number = models.CharField(blank=True, null=True, max_length=200, default="")
    si_number = models.CharField(blank=True, null=True, max_length=200, default="")
    parent_wo = models.CharField(blank=True, null=True, max_length=200, default="")
    parent_auto_key = models.IntegerField(blank=True, null=True, default=0)
    woo_auto_key = models.IntegerField(blank=True, null=True, default=0) 
    wob_auto_key = models.IntegerField(blank=True, null=True, default=0)
    stm_auto_key = models.IntegerField(blank=True, null=True, default=0)
    str_auto_key = models.IntegerField(blank=True, null=True, default=0)    
    wos_auto_key = models.IntegerField(blank=True, null=True, default=0)
    wot_auto_key = models.IntegerField(blank=True, null=True, default=0)
    rod_auto_key = models.IntegerField(blank=True, null=True, default=0)
    wo_task = models.CharField(blank=True, null=True, max_length=200, default="")
    reg_user_id = models.ForeignKey(QuantumUser, on_delete=models.CASCADE, blank=True, null=True)    
    status_key = models.ForeignKey(StatusSelection, on_delete=models.CASCADE, blank=True, null=True)
    supdate_msg = models.CharField(blank=True, null=True, max_length=6000, default="")
    time_status = models.CharField(blank=True, null=True, max_length=200, default="")
    status = models.CharField(blank=True, null=True, max_length=200, default="")
    due_date = models.DateField(blank=True, null=True,default=datetime.date.today)
    entry_date = models.DateField(blank=True, null=True,default=datetime.date.today)
    stock_line = models.CharField(blank=True, null=True, max_length=200, default="")
    part_number = models.CharField(blank=True, null=True, max_length=200, default="")
    pnm_auto_key = models.IntegerField(blank=True, null=True, default=0)
    description = models.CharField(blank=True, null=True, max_length=200, default="")
    serial_number = models.CharField(blank=True, null=True, max_length=200, default="")
    location_code = models.CharField(blank=True, null=True, max_length=200, default="")
    condition_code = models.CharField(blank=True, null=True, max_length=200, default="")
    cond_level = models.IntegerField(blank=True, null=True, default=0)
    cond_level_gsix = models.CharField(blank=True, null=True, max_length=200, default="")
    cond_level_zero = models.CharField(blank=True, null=True, max_length=200, default="")
    consignment_code = models.CharField(blank=True, null=True, max_length=200, default="")
    wh_code = models.CharField(blank=True, null=True, max_length=200, default="")
    time_loc = models.CharField(blank=True, null=True, max_length=200, default="")
    active = models.BooleanField('Active', default=True)
    user_id = models.CharField(blank=True, null=True, max_length=200, default="")
    need_date_variance = models.IntegerField(blank=True, null=True, default=0)
    due_date_var = models.CharField(blank=True, null=True, max_length=200, default="None")
    update_stamp = models.CharField(blank=True, null=True, max_length=200, default="None")
    customer = models.CharField(blank=True, null=True, max_length=200, default="")
    vendor = models.CharField('Vendor',blank=True, null=True, max_length=200, default="")
    vendor_key = models.IntegerField(blank=True, null=True, default=0) 
    manager = models.CharField(blank=True, null=True, max_length=200, default="")
    rank = models.CharField(blank=True, null=True, max_length=200, default="None")
    wo_type = models.CharField(blank=True, null=True, max_length=200, default="")
    cust_ref_number = models.CharField(blank=True, null=True,max_length=200, default="")
    is_dashboard = models.BooleanField(blank=True, null=True, default=1)
    is_racking = models.BooleanField(blank=True, null=True, default=0) 
    session_id = models.CharField(blank=True, null=True, max_length=200, default="")
    rack = models.CharField(blank=True, null=True, max_length=200, default="none set")
    ctrl_number = models.CharField(blank=True, null=True, max_length=200, default="")
    ctrl_id = models.CharField(blank=True, null=True, max_length=200, default="")    
    quantity = models.FloatField(blank=True, null=True, default=0)
    mode_id = models.ForeignKey(AppModes, on_delete=models.CASCADE, blank=True, null=True)
    app_mode = models.CharField(blank=True, null=True, max_length=200, default="")
    priority = models.CharField(blank=True, null=True, max_length=200, default="")
    activity = models.CharField(blank=True, null=True, max_length=200, default="")
    ro_number = models.CharField(blank=True, null=True, max_length=200, default="")    
    po_number = models.CharField(blank=True, null=True, max_length=200, default="")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.wo_number 

class UserDefAtts(models.Model):    
    auto_key = models.IntegerField(blank=True, null=True, default=0) 
    att_seq = models.IntegerField(blank=True, null=True, default=0)     
    att_value = models.CharField(blank=True, null=True, max_length=200, default="")
    att_name = models.CharField(blank=True, null=True, max_length=200, default="")
    att_type = models.CharField(blank=True, null=True, max_length=200, default="")
    activity = models.CharField(blank=True, null=True, max_length=200, default="")
    session_id = models.CharField(blank=True, null=True, max_length=2000, default="")
        
class PILogs(models.Model):        
    batch_no = models.CharField(blank=True, null=True, max_length=200, default="")
    quantity = models.FloatField(blank=True, null=True, default=0)
    batch = models.CharField(blank=True, null=True, max_length=200, default="")
    qty = models.FloatField(blank=True, null=True, default=0)
    stock_label = models.CharField(blank=True, null=True, max_length=200, default="")
    ctrl_number = models.CharField(blank=True, null=True, max_length=200, default="")
    ctrl_id = models.CharField(blank=True, null=True, max_length=200, default="")
    location_code = models.CharField(blank=True, null=True, max_length=200, default="")
    active = models.BooleanField('Active', default=True)
    user_id = models.CharField(blank=True, null=True, max_length=200, default="")
    session_id = models.CharField(blank=True, null=True, max_length=2000, default="")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.stock_label