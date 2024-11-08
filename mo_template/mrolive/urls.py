from django.http import HttpResponse
from django.urls import path
from mrolive import views
app_name = 'mrolive'
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.contrib import admin
 
urlpatterns = [
    path('audit-trail/<quapi_id>', views.audit_trail, name='audit_trail'),
    path('barcoding/<quapi_id>', views.barcarting, name='barcarting'),
    path('wo-dashboard/<quapi_id>', views.dashboard, name='dashboard'),
    path('wo-management/<quapi_id>', views.management, name='management'),
    path('physical-inventory/<quapi_id>', views.pi_update, name='pi_update'),
    #url(r'^results_grid_pop/$', views.results_grid_pop, name='results_grid_pop'),
    #url('results_grid_pop', views.results_grid_pop, name='results_grid_pop'),
    url(r'^admin/', admin.site.urls),
    #url(r'^record-json$', views.RecordJsonView.as_view(), name='record-json'),
    #url('record-list', views.RecordListView.as_view(), name='record-list'),
    url(r'^json$', views.RecordJsonView.as_view(), name='record-json'),
    url(r'^pi-json$', views.PIJsonView.as_view(), name='pi-json'),
    url(r'^adt-json$', views.ADTJsonView.as_view(), name='adt-json'),
    url(r'^list$', views.RecordListView.as_view(), name='record-list'),
    url(r'^pi-list$', views.PIListView.as_view(), name='pi-list'),
    url(r'^adt-list$', views.ADTListView.as_view(), name='adt-list'),
] + static(settings.STATIC_URL, document_root=settings.STAT)