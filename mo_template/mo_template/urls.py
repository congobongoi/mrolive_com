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
from django.conf import settings
from django.contrib import admin
from django.urls import include,path,re_path
from django.views.generic.base import TemplateView
from portal import views
from .views import redirect_root
from django.conf.urls.static import static

urlpatterns = [
    path('', include('django.contrib.auth.urls')), #login/pwd reset/logout
    path('queries/', include('queries.urls')),
    path('padron', admin.site.urls),
    path('logout/', views.logout_view, name='logout_view'),
    path('login/route/<logoff>', views.account_route, name='account_route'),
    path('login/route/', views.account_route, name='account_route'),
    path('portal/', include('portal.urls')),
    re_path(r'^$', redirect_root),
]
#if settings.DEBUG: 
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
if settings.TOOLBAR:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]+ urlpatterns