"""mo_template URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from portal import views
from django.conf.urls.static import static

urlpatterns = [
    path('', include('django.contrib.auth.urls')), #login/pwd reset/logout
    path('pi_update/', include('pi_update.urls')),
    path('polls/', include('polls.urls')),
    path('queries/', include('queries.urls')),
    path('padron', admin.site.urls),
    path('padron/mrolive', TemplateView.as_view(template_name='registration/home.html'), name='home'),
    path('padron/apps', views.app_mgmt, name='app_mgmt'),
    path('logout/', views.logout_view, name='logout_view'),
    path('login/route/', views.accounts_route, name='accounts_route'),
    path('login/route', views.accounts_route, name='accounts_route'),
    path('mrolive/', include('mrolive.urls')),
    path('portal/', include('portal.urls')),
    ]
    
if settings.TOOLBAR:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]+ urlpatterns"""
