from django.db import models
from django.utils import timezone
        
class QCUser(models.Model):

    user_id = models.CharField(max_length=200, default="None", blank=True, null=True)
    user_auto_key = models.IntegerField('User Key from Quantum DB', default=0)
    pass_key = models.CharField(max_length=200, default="", blank=True, null=True)
    user_name = models.CharField(max_length=200, default="", blank=True, null=True)
    employee_code = models.CharField(max_length=200, default="", blank=True, null=True)
    
class PIUpdate(models.Model):  
        
    batch_no = models.CharField(max_length=200, default="", blank=True, null=True)
    stock_label = models.CharField(max_length=200, default="", blank=True, null=True)
    control_no = models.CharField(max_length=200, default="", blank=True, null=True)
    control_id = models.IntegerField('Control ID', default=0, blank=True, null=True)
