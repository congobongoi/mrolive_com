from django.db import models

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
