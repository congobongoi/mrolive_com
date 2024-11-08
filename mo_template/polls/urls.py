from django.http import HttpResponse
from django.urls import path
from polls import views
app_name = 'polls'
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.contrib import admin
 
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #path('mro_live/racking_beta', views.racking_beta, name='racking_beta'),
    #path('mro_live/barcoding_beta/<int:user_id>/<user_sesh>', views.update_beta, name='update_beta'),
    #path('mro_live/wo-dashboard_beta/<int:user_id>/<user_sesh>', views.dashboard_beta, name='dashboard_beta'),
    #path('mro_live/wo-management_beta', views.management_beta, name='management_beta'),
    #path('mro_live/pi_update_beta/<int:user_id>/<user_sesh>', views.pi_update_beta, name='pi_update_beta'),
    #path('mro_live/audit_trail', views.audit_trail_beta, name='audit_trail_beta'),
    url(r'^json$', views.RecordJsonView.as_view(), name='record-json'),
    url(r'^list$', views.RecordListView.as_view(), name='record-list'),
] + static(settings.STATIC_URL, document_root=settings.STAT)