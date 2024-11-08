import datetime
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.

"""class User(AbstractUser):
    #is_manager = models.BooleanField('Manager', related_name="mgr_profile", default=False)
    #is_staff = models.BooleanField('Staff Member', related_name="staff_profile", default=False)
    pass
    """
    
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
    
class QuantumUser(models.Model):

    user_id = models.CharField('USER_ID from SYS_USERS table in QCTL.', max_length=200, default="None", blank=True, null=True)
    user_auto_key = models.IntegerField('User Key from Quantum DB', default=0)
    pass_key = models.CharField(max_length=200, default="", blank=True, null=True)
    user_name = models.CharField(max_length=200, default="", blank=True, null=True)
    employee_code = models.CharField(max_length=200, default="", blank=True, null=True)
    first_name = models.CharField(max_length=200, default="", blank=True, null=True)
    last_name = models.CharField(max_length=200, default="", blank=True, null=True)
    email = models.CharField(max_length=200, default="", blank=True, null=True)
    dj_user_id = models.IntegerField('Django auth user id.',default=0, blank=True, null=True) 
    
class QueryApi(models.Model):
 
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
    orcl_conn_id = models.IntegerField('Oracle connect remote API connection id.(schema)',default=0)
        
class StatusSelection(models.Model):

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
  
class MLApps(models.Model):
    name = models.CharField(max_length=200, default="", blank=True, null=True)
    code = models.CharField(max_length=200, default="", blank=True, null=True)
    uri = models.CharField(max_length=200, default="", blank=True, null=True) 
    #tmpl_page = models.CharField(max_length=200, default="", blank=True, null=True) 
    active = models.BooleanField('Active', default=True)          

class AppModes(models.Model):
    name = models.CharField(max_length=200, default="", blank=True, null=True)
    code = models.CharField(max_length=200, default="", blank=True, null=True)
    ml_apps_id = models.ForeignKey(MLApps, on_delete=models.CASCADE, blank=True, null=True)
    active = models.BooleanField('Active', default=True)    
    
class UserAppPerms(models.Model):
    ml_apps_id = models.ForeignKey(MLApps, on_delete=models.CASCADE, blank=True, null=True)
    dj_group_id = models.IntegerField(blank=True, null=True, default=0)
    dj_user_id = models.IntegerField('Django admin user id.', blank=True, null=True, default=0)
    dj_username = models.CharField(max_length=200, default="", blank=True, null=True)     
    global_access = models.BooleanField('Global Access', default=True)
    
class UserQuapiRel(models.Model):
    quapi_id = models.ForeignKey(QueryApi, on_delete=models.CASCADE, blank=True, null=True)
    dj_user_id = models.IntegerField('Django admin user id.', blank=True, null=True, default=0)
    dj_username = models.CharField(max_length=200, default="", blank=True, null=True)     
    global_access = models.BooleanField('Global Access', default=True)
    
class AuditTrail(models.Model):
    create_date = models.DateTimeField(blank=True, null=True,default=datetime.date.today)
    write_date = models.DateTimeField(blank=True, null=True,default=datetime.date.today)
    field_changed = models.CharField(max_length=200, default="")
    new_val = models.CharField(max_length=200, default="")
    description = models.CharField(max_length=2200, default="")
    quapi_id = models.ForeignKey(QueryApi, on_delete=models.CASCADE, blank=True, null=True)
    user_id = models.CharField(max_length=200, default="")
    ml_apps_id = models.ForeignKey(MLApps, on_delete=models.CASCADE, blank=True, null=True)
    
class WOStatus(models.Model):  
    wo_number = models.CharField(blank=True, null=True, max_length=200, default="")
    parent_wo = models.CharField(blank=True, null=True, max_length=200, default="")
    woo_auto_key = models.IntegerField(blank=True, null=True, default=0) 
    stm_auto_key = models.IntegerField(blank=True, null=True, default=0) 
    wos_auto_key = models.IntegerField(blank=True, null=True, default=0)
    reg_user_id = models.ForeignKey(QuantumUser, on_delete=models.CASCADE, blank=True, null=True)    
    status_key = models.ForeignKey(StatusSelection, on_delete=models.CASCADE, blank=True, null=True)
    supdate_msg = models.CharField(blank=True, null=True, max_length=6000, default="")
    #create_date = models.DateTimeField(blank=True, null=True,default=datetime.date.today)
    #write_date = models.DateTimeField(blank=True, null=True,default=datetime.date.today)
    time_status = models.CharField(blank=True, null=True, max_length=200, default="")
    status = models.CharField(blank=True, null=True, max_length=200, default="")
    due_date = models.DateField(blank=True, null=True,default=datetime.date.today)
    entry_date = models.DateField(blank=True, null=True,default=datetime.date.today)
    stock_line = models.CharField(blank=True, null=True, max_length=200, default="")
    part_number = models.CharField(blank=True, null=True, max_length=200, default="")
    description = models.CharField(blank=True, null=True, max_length=200, default="")
    serial_number = models.CharField(blank=True, null=True, max_length=200, default="")
    location_code = models.CharField(blank=True, null=True, max_length=200, default="")
    wh_code = models.CharField(blank=True, null=True, max_length=200, default="")
    time_loc = models.CharField(blank=True, null=True, max_length=200, default="")
    active = models.BooleanField('Active', default=True)
    user_id = models.CharField(blank=True, null=True, max_length=200, default="")
    need_date_variance = models.IntegerField(blank=True, null=True, default=0)
    due_date_var = models.CharField(blank=True, null=True, max_length=200, default="None")
    update_stamp = models.CharField(blank=True, null=True, max_length=200, default="None")
    customer = models.CharField(blank=True, null=True, max_length=200, default="")
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