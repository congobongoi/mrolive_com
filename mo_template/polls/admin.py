from django.contrib import admin
from polls.models import PrintSetting,UserGroupProfile,QueryApi,AppModes,AuditTrail,MLApps,UserAppPerms,UserQuapiRel,QuantumUser,UserProfile,StatusSelection,OracleConnection
# Register your models here.
admin.site.register(PrintSetting)
admin.site.register(QuantumUser)
admin.site.register(MLApps)
admin.site.register(UserAppPerms)
admin.site.register(QueryApi)
admin.site.register(AppModes)
admin.site.register(UserQuapiRel)
admin.site.register(UserProfile)
admin.site.register(UserGroupProfile)
admin.site.register(StatusSelection)
admin.site.register(OracleConnection)