from django.http import HttpResponse

from django.urls import path

from . import views

from pi_update import views

app_name = 'pi_update'

from django.conf import settings
from django.conf.urls.static import static
# Use include() to add paths from the catalog application 
from django.urls import include
from django.urls import path

urlpatterns = [
    path('mro_live/', views.pi_update, name='pi_update'),
    path('mro_live/<int:quapi_id>', views.pi_update, name='pi_update'),
] + static(settings.STATIC_URL, document_root=settings.STAT)