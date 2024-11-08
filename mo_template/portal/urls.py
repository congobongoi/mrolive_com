from django.http import HttpResponse
from portal import views
app_name = 'portal'
from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.contrib import admin

urlpatterns = [
    path('smd-management/<quapi_id>', views.shipping_mgmt, name='shipping_mgmt'),
    path('stock-picking/<quapi_id>', views.stock_picking, name='stock_picking'), 
    path('repair-order-mgmt/<quapi_id>', views.repair_order_mgmt, name='repair_order_mgmt'),    
    re_path(r'^json$', views.RecordJsonView.as_view(), name='record-json'),
] + static(settings.STATIC_URL, document_root=settings.STAT)