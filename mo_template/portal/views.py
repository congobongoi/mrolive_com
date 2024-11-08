#!/usr/bin/env python3
# -*- coding: utf8 -*-
# encoding=utf8
from portal.forms import WODashboardForm,PIUpdateForm
from polls.models import MoTemplate,PILogs,WOStatus,QueryApi,StatusSelection,WOTask,TaskLabor,Operation
from polls.models import QuantumUser,AppModes,AuditTrail,MLApps,UserAppPerms,Companies
from polls.models import Location,Warehouse,StockCart,UserQuapiRel,UserProfile,UserGroupProfile,StockReceiver
from polls.models import ColumnSettings,Departments,WarehouseLocation,Document,Sale
from polls.models import ShipVia,Priority
from django.http import Http404
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.core.signing import Signer
import os
import csv
import re
import sys 
import importlib
import itertools
import math
import logging
from operator import itemgetter
logger = logging.getLogger(__name__)
from datetime import datetime, timedelta
from dateutil.parser import parse
from django.contrib.auth import logout
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models import F
from django.http import JsonResponse
FILE_PATH = settings.MEDIA_URL


def shipping_mgmt(request,quapi_id=None):
    new_status,location,filter_status = '','',''
    user_id,user_rec,fail_ms = 'user not set',None,''
    val_dict,form = {},{} 
    error,msg,loc_msg,stat_msg = '','','',''
    user = request and request.user or None
    if not (user and user.id):
        val_dict['error'] = 'Access denied.'
        return redirect('/login/')  
    user_profile = user and UserProfile.objects.filter(user=user) or None   
    user_profile = user_profile and user_profile[0] or None   
    sysur_auto_key = user_profile and user_profile.sysur_auto_key or None
    user_name = user and user.username or 'No Username'
    reg_user_id = user and user.is_authenticated and user.id or None
    dj_user_id = quapi_id and UserQuapiRel.objects.filter(user=user,quapi_id=quapi_id) or None
    dj_user_id = dj_user_id and user.id or None
    user_apps = user and UserAppPerms.objects.filter(user=user) or None
    op_apps = user_apps and user_apps.filter(ml_apps_id__app_type='operations').order_by('ml_apps_id__menu_seq') or None
    val_dict['op_apps'] = op_apps
    mgmt_apps = user_apps and user_apps.filter(ml_apps_id__app_type='management').order_by('ml_apps_id__menu_seq') or None    
    val_dict['mgmt_apps'] = mgmt_apps
    dash_apps = user_apps and user_apps.filter(ml_apps_id__app_type='dashboards').order_by('ml_apps_id__menu_seq') or None
    val_dict['dash_apps'] = dash_apps
    setup_apps = user_apps and user_apps.filter(ml_apps_id__app_type='setup').order_by('ml_apps_id__menu_seq') or None
    val_dict['setup_apps'] = setup_apps
    app_id = MLApps.objects.filter(code='smd-management')[0]
    app_allow = user_apps and user_apps.filter(ml_apps_id=app_id)
    if not (reg_user_id and dj_user_id and app_allow):
        val_dict['error'] = 'Access denied.'
        return redirect('/login/') 
    val_dict['quapi_id'] = quapi_id
    from portal.tasks import get_shipping_status,get_ship_vias,get_priorities
    from portal.tasks import get_users_nsync_beta
    session_id = 'anSI823(2$3%234MLK8'    
    res = get_ship_vias.delay(quapi_id,session_id,app='Shipping Mgmt')
    svia_error,app = res.get() 
    ship_vias = ShipVia.objects.filter(session_id=session_id) 
    res = get_priorities.delay(quapi_id,session_id,app='Shipping Mgmt')
    pri_error,app = res.get()  
    priorities = Priority.objects.filter(session_id=session_id) 
    res = get_shipping_status.delay(quapi_id,session_id,app='Shipping Mgmt')
    stat_error,app = res.get()  
    statuses = StatusSelection.objects.filter(session_id=session_id) 
    res = get_users_nsync_beta.delay(quapi_id,dj_user_id)
    users = QuantumUser.objects.filter(quapi_id=quapi_id,dj_user_id=dj_user_id)
    
    val_dict.update({
        'status_vals':statuses,
        'users': users,
        'ship_via_codes':ship_vias,
        'priorities':priorities,
    })
    
    if request.method == 'GET':
        form = WODashboardForm()
        
                                                                                                                     
                                  
                                                                                                                                  
    if request.method == 'POST':
        req_post = request.POST
        form = WODashboardForm(req_post) 
        customer=req_post.get('customer','')
        order=req_post.get('order','')
        entry_date=req_post.get('entry_date','')
        status=req_post.get('status','')
        part_number=req_post.get('part_number','')
        description=req_post.get('description','')
        user_id=req_post.get('user_id','')
        ship_via=req_post.get('ship_via','')
        priority=req_post.get('priority','')
        location=req_post.get('location','')
        whs=req_post.get('warehouse','') 
        launch_update = req_post.get('launch_update','')
        is_search = req_post.get('search_stock','')
        is_update = req_post.get('is_update','')  
        user_update = req_post.get('user_update','')
        tote = req_post.get('tote','')
        notes = req_post.get('notes','')        
        session_id=req_post.get('session_id','')
        
        if not session_id:
            session_id = req_post.get('csrfmiddlewaretoken','')
            
        val_dict.update({
            'msg': msg,
            'customer': customer,
            'order': order,
            'entry_date': entry_date,
            'status': status,
            'part_number': part_number,
            'user_id': user_id,
            'description': description,
            'ship_via': ship_via,
            'priority': priority,
            'location': location,
            'whs': whs, 
            'user_name': user_name,            
            'session_id': session_id, 
            'sel_rows': 0,            
        })

        filter_list = [customer,order,entry_date,status,part_number]
        filter_list += [description,ship_via,priority,location,whs,user_id]
        
        smds_list = []
        if 'smd_sels[]' in req_post:
            smds_list = req_post.getlist('smd_sels[]')
            
        elif 'woos_list[]' in req_post:
            smds_list = req_post.getlist('woos_list[]')  
            val_dict['smds_list'] = smds_list
            
        
        if is_search == '1':

            if any(f.strip() for f in filter_list):         
                
                from portal.tasks import search_shipping
                res = search_shipping.delay(quapi_id,session_id,\
                    sysur_auto_key,filter_list)
                error,msg = res.get()
                all_smds = WOStatus.objects.filter(session_id=session_id)
                val_dict['total_rows'] = len(all_smds)
                
            else:
                error = 'Please enter a value into at least one filter.'
                
        elif launch_update == '1':
            val_dict['session_id'] = session_id
            val_dict['launch_update'] = 'T'
            val_dict['smds_list'] = smds_list 
            all_smds = WOStatus.objects.filter(session_id=session_id)
            val_dict['total_rows'] = len(all_smds)   
            
        elif is_update == '1':
        
            if not smds_list:
                error = 'Select grid rows to update'
                return render(request, 'mrolive/shipping_edit.html', val_dict) 
       
            from portal.tasks import update_shipping,search_shipping
            res = update_shipping.delay(quapi_id,session_id,\
                sysur_auto_key,user_update,smds_list,tote,notes)
            error,msg = res.get()
            
            if not error:

                from portal.tasks import search_shipping
                res = search_shipping.delay(quapi_id,session_id,\
                    sysur_auto_key,filter_list=[],smds_list=smds_list)
                error,msg = res.get()
                
                updated_smds = WOStatus.objects.filter(
                    session_id=session_id,
                    )

                scan_time = datetime.now()
                scan_time = scan_time.strftime('%m/%d/%Y %H:%M:%S')
                
                val_dict.update({
                    'smds':updated_smds,
                    'user_id': user_update,
                    'scan_time': scan_time,
                })
                
                return render(request, 'mrolive/shipping_label.html', val_dict)                 
            
    val_dict['msg'] = msg
    val_dict['error'] = error
    val_dict['form'] = form
    return render(request, 'mrolive/shipping_edit.html', val_dict)  

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    val_dict={}
    return redirect('https://portal.mrolive.com/')
    
def account_route(request, logoff='0'):
    #get current user's SQLite db id
    app_sel,quapi_sel,app_selected,quapi_selected,red,val_dict='','','','','',{}
    req_post = None
    quapis = QueryApi.objects.all()
    apps = MLApps.objects.all()
    from datetime import timezone
    from django.contrib.sessions.models import Session
    from django.contrib.auth import logout
    right_now = datetime.now(timezone.utc)
    #all_sessions = Session.objects.filter(expire_date__gte=right_now)
    user = request.user
    user_apps = user and UserAppPerms.objects.filter(user=user) or None
    if not user_apps:
        val_dict['error'] = 'No apps assigned. Use user management to assign.'
        return render(request, 'registration/home.html', val_dict)         
    op_apps = user_apps and user_apps.filter(ml_apps_id__app_type='operations').order_by('ml_apps_id__menu_seq') or None
    val_dict['op_apps'] = op_apps
    mgmt_apps = user_apps and user_apps.filter(ml_apps_id__app_type='management').order_by('ml_apps_id__menu_seq') or None
    val_dict['mgmt_apps'] = mgmt_apps
    dash_apps = user_apps and user_apps.filter(ml_apps_id__app_type='dashboards').order_by('ml_apps_id__menu_seq') or None
    val_dict['dash_apps'] = dash_apps
    setup_apps = user_apps and user_apps.filter(ml_apps_id__app_type='setup').order_by('ml_apps_id__menu_seq') or None
    val_dict['setup_apps'] = setup_apps
    username = user and user.username or 'No Username'
    user_id = user and user.is_authenticated and user.id or None
    if not user.id or not user_id:
        val_dict['error'] = 'Access denied.'
        return redirect('/login/') 
    #check group and get quantum_cmp_key
    #group = user_groups and user_groups[0] or None
    #using the user profile, query Quantum to confirm the sysur_auto_key is correct
    #we could either use the get_users() task or run a query just for our user 
    #look up latest users and then compare the username with the user_id field.    
    from portal.tasks import get_users_nsync_beta
    res = get_users_nsync_beta.delay(1,user_id,is_dashboard=0,app='account-route')
    user_error,app = res.get()
    # | Q(employee_code=username)
    q_user = QuantumUser.objects.filter(user_id=username)
    if not q_user:
        q_user = QuantumUser.objects.filter(employee_code=username)
    if not q_user:
        q_user = QuantumUser.objects.filter(user_name=username)
    q_user = q_user and q_user[0] or None    
    if q_user:
        #check that the sysur_auto_key is correct
        #if not, then we have to correct it on the user profile record
        user_profile = UserProfile.objects.filter(user=user)
        user_profile = user_profile and user_profile[0] or None 
        sysur_auto_key = user_profile.sysur_auto_key
        if sysur_auto_key != q_user.user_auto_key:
            #change the sysur_auto_key
            user_profile.sysur_auto_key = q_user.user_auto_key
    else:
        #prompt the user to synch up the username with that of a user_id from a Quantum user.
        val_dict['error'] = 'User name does not match any USER IDs in Quantum.'
    group = None
    user_groups = user.groups.all()
    for user_group in user_groups:
        group = UserGroupProfile.objects.filter(group=user_group.id)
        group = group and group[0] or None
        if group:
            break
    if not group:
        val_dict['error'] = 'User must belong to the company group.'
        return render(request, 'registration/home.html', val_dict)	    
    quantum_cmp_key = group.quantum_cmp_key                                                                         
    if request.method == 'POST':
        #based on the user's selection of quapi and app, we will route to the appropriate place
        req_post = request.POST
        app_sel = None
        app_selected = 'app_selector' in req_post and req_post['app_selector'] or None
        """mgmt_app_selected = 'mgmt_app_selector' in req_post and req_post['mgmt_app_selector'] or None
        setup_app_selected = 'setup_app_selector' in req_post and req_post['setup_app_selector'] or None
        dash_app_selected = 'dash_app_selector' in req_post and req_post['dash_app_selector'] or None
        if op_app_selected:
            app_sel = op_app_selected and apps.filter(id=op_app_selected) or '' 
            app_sel = app_sel and app_sel[0] or None
        elif mgmt_app_selected:
            app_sel = mgmt_app_selected and apps.filter(id=mgmt_app_selected) or '' 
            app_sel = app_sel and app_sel[0] or None
        elif dash_app_selected:
            app_sel = dash_app_selected and apps.filter(id=dash_app_selected) or '' 
            app_sel = app_sel and app_sel[0] or None"""
        if app_selected:
            app_sel = app_selected and apps.filter(id=app_selected) or '' 
            app_sel = app_sel and app_sel[0] or None
        quapi_selected = 'quapi_selector' in req_post and req_post['quapi_selector'] or 1
        #quapi_sel = quapi_selected and quapis.filter(id=quapi_selected) or None   
        #quapi_sel = quapi_sel and quapi_sel[0] or None
    quapi_set = user_id and UserQuapiRel.objects.filter(user=user) or []
    if not quapi_set or not user:
        render(request, 'registration/home.html', val_dict)   
    #check user_id in the rel table that associates the Django app user
    #with the quantum user
    session_id = request.session and request.session.session_key or None 
    #quapi_id = user_id and quapis and quapis.filter(id = quapi_id) or None
    #quapi_id = quapi_id and quapi_id[0] or None
    val_dict.update({
        'app_set': user_apps,
        'app_sel': app_sel and app_sel.id or None,
        'user_id': user_id,
        'quapi_set': quapi_set,
        'quapi_sel': quapi_selected and int(quapi_selected) or 0,        
        'session_id': session_id,
        })
    if app_sel and user_id and req_post:
        app_view = app_sel and '/portal/' + str(app_sel.code) + '/' + str(quapi_selected) or None
        #url = app_view and quapi_id and request.build_absolute_uri(reverse(app_view, args=(quapi_id, ))) or None
        #app_view = app_sel and '/portal/' + str(app_sel.code) or None
        if app_view:
            return redirect(app_view)
    return render(request, 'registration/home.html', val_dict) 
  
def stock_picking(request,quapi_id=None):
    new_status,location,filter_status = '','',''
    user_id,user_rec = 'user not set',None
    wo_number = ''
    val_dict,form = {},{}
    all_woos = WOStatus.objects.filter(active=1, is_dashboard=1, session_id='') 
    updated_woos = all_woos 
    woos_updated = False    
    error,msg,loc_msg,stat_msg = '','','',''
    woos_updated = False
    from polls.models import StatusSelection as stat_sel,QuantumUser as quser
    user = request.user
    user_id = user and user.is_authenticated and user.id or None
    if not user_id:
        return redirect('/login/')   
    reg_user_id = user and user.is_authenticated and user.id or None
    dj_user_id = user and quapi_id and UserQuapiRel.objects.filter(user=user,quapi_id=quapi_id) or None
    dj_user_id = dj_user_id and user.id or None
    if not reg_user_id or not dj_user_id:
        val_dict['error'] = 'Access denied.'
        return redirect('/login/')  
    user_profile = user and UserProfile.objects.filter(user=user) or None   
    user_profile = user_profile and user_profile[0] or None
    sysur_auto_key = user_profile and user_profile.sysur_auto_key or None
    user_apps = user and UserAppPerms.objects.filter(user=user) or None
    op_apps = user_apps and user_apps.filter(ml_apps_id__app_type='operations').order_by('ml_apps_id__menu_seq') or None
    val_dict['op_apps'] = op_apps
    mgmt_apps = user_apps and user_apps.filter(ml_apps_id__app_type='management').order_by('ml_apps_id__menu_seq') or None
    val_dict['mgmt_apps'] = mgmt_apps
    dash_apps = user_apps and user_apps.filter(ml_apps_id__app_type='dashboards').order_by('ml_apps_id__menu_seq') or None
    val_dict['dash_apps'] = dash_apps
    setup_apps = user_apps and user_apps.filter(ml_apps_id__app_type='setup').order_by('ml_apps_id__menu_seq') or None
    val_dict['setup_apps'] = setup_apps                               
    val_dict['quapi_id'] = quapi_id        
    from portal.tasks import get_statuses_nsync_beta
    if request.method == 'GET':                                  
        form = WODashboardForm()        
    val_dict['status_vals'] = dj_user_id and stat_sel.objects.filter(quapi_id=quapi_id,dj_user_id=dj_user_id,is_dashboard=1).distinct() or [] 
    if request.method == 'POST':
        req_post = request.POST
        
        form = WODashboardForm(req_post)
        exact_match = 'exact_match' in req_post and req_post['exact_match'] or ''
        if exact_match:
            exact_match = 'checked'
        wo_number = 'wo_number' in req_post and req_post['wo_number'] or ''                                                                                     
        user_id = 'user_id' in req_post and req_post['user_id'] or ''
        session_id = 'session_id' in req_post and req_post['session_id'] or ''
        if not session_id:
            session_id = 'csrfmiddlewaretoken' in req_post and req_post['csrfmiddlewaretoken'] or ''
        total_rows = 'total_rows' in req_post and req_post['total_rows'] or 0
        sel_rows = 'sel_rows' in req_post and req_post['sel_rows'] or 0 
        options_col,page_size = get_options(req_post,session_id) 
        wo_reserve = 'wo_reserve' in req_post and req_post['wo_reserve'] or ''        
        val_dict.update({
            'all_woos': updated_woos, 
            'msg': msg,
            'user_id': user_id or '',           
            'wo_number': '',
            'session_id': session_id,
            'sel_rows': sel_rows,
            'total_rows': total_rows,
            'exact_match': exact_match,
            'options_col': options_col,
            'page_size': page_size,               
        })
        wob_id_list = []
        from portal.tasks import stock_picking
        if 'wobs_list[]' in req_post:
            wob_id_list = req_post.getlist('wobs_list[]')
            #print report with all of the stock moves and reserve them all to the bom for the part
            res = stock_picking.delay(quapi_id,sysur_auto_key,session_id,wo_number,exact_match=True,wob_id_list=wob_id_list) 
            error,msg = res.get() 
        else:
            if not wo_number:
                val_dict['error'] = 'Enter WO#.' 
                return render(request, 'mrolive/stock_picking.html', val_dict) 
            res = stock_picking.delay(quapi_id,sysur_auto_key,session_id,wo_number,exact_match=True) 
            error,msg = res.get()               
        if error == 'no errors':
            error = ''        
        updated_woos = WOStatus.objects.filter(session_id=session_id,is_detail=False)
        val_dict['all_woos'] = updated_woos
    val_dict['msg'] = msg
    val_dict['error'] = error
    val_dict['total_rows'] = str(len(updated_woos))
    val_dict['form'] = form
    user_profile = UserProfile.objects.filter(user=user)
    user_profile = user_profile and user_profile[0] or None
    val_dict['num_records'] = user_profile.num_records or 10
    return render(request, 'mrolive/stock_picking.html', val_dict) 
         
#**************************************KENDO UI GRID CONTROLLERS********************************************************
from django.http import HttpResponse
from django.views.generic import View
from django.views import generic
import json
from rest_framework import serializers, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

#==============================================================================================================            
class RecordPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'pageSize'

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WOStatus
        fields = '__all__'

# Create your views here.
class RecordListView(generic.ListView):
    model = WOStatus
    def get_context_data(self, **kwargs):       
        context = super(RecordListView, self).get_context_data(**kwargs)
        return context

class RecordJsonView(generics.ListAPIView):
    serializer_class = RecordSerializer
    pagination_class = RecordPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        rec_set = [] 
        shippers = self.request.GET.get('shippers','F')
        session_id = 'session_id' in self.request.GET and self.request.GET['session_id'] 
        user_id = 'user_id' in self.request.GET and self.request.GET['user_id']
        is_wos = 'is_wos' in self.request.GET and self.request.GET['is_wos'] or False
        is_dock = 'is_dock' in self.request.GET and self.request.GET['is_dock'] or False         
        active_mode = 'active_mode' in self.request.GET and self.request.GET['active_mode'] or False          
        is_rack = 'is_rack' in self.request.GET and self.request.GET['is_rack'] or False 
        is_shop = self.request.GET.get('is_shop','')
        sub_wo_gate = 'sub_wo_gate' in self.request.GET and self.request.GET['sub_wo_gate'] or ''
        is_toll_analysis = 'is_toll_analysis' in self.request.GET and self.request.GET['is_toll_analysis'] or ''
        is_toll_detail = 'is_toll_detail' in self.request.GET and self.request.GET['is_toll_detail'] or ''
        parent_auto_key = 'parent_auto_key' in self.request.GET and self.request.GET['parent_auto_key'] or ''
        is_loc_whs = 'is_loc_whs' in self.request.GET and self.request.GET['is_loc_whs'] or '' 
        is_parts_req = 'is_parts_req' in self.request.GET and self.request.GET['is_parts_req'] or ''  
        is_picking = 'is_picking' in self.request.GET and self.request.GET['is_picking'] or '' 
        sub_grid = 'sub_grid' in self.request.GET and self.request.GET['sub_grid'] or ''
        filter_val = 'filter_val' in self.request.GET and self.request.GET['filter_val'] or ''
        if shippers == 'T':
            wo_type = 'SHIPPER'       
            records = session_id and WOStatus.objects.filter(session_id=session_id,wo_type = wo_type).order_by('-id')
        elif is_shop == '1':          
            records = WOStatus.objects.filter(session_id=session_id).order_by('id')       
        elif is_toll_detail == '1':
            if sub_wo_gate and sub_wo_gate != '0':
                records = is_wos != '0' and session_id and WOStatus.objects.filter(parent_auto_key=parent_auto_key,is_detail=True,sub_wo_gate=sub_wo_gate,session_id=session_id,active=1).order_by('-id') 
            else:
                records = is_wos != '0' and session_id and WOStatus.objects.filter(parent_auto_key=parent_auto_key,is_detail=True,session_id=session_id,active=1).order_by('-id')              
        elif is_toll_analysis == '1':  
            records = is_wos != '0' and session_id and WOStatus.objects.filter(is_detail=False,session_id=session_id,active=1).order_by('-id')
        elif session_id and is_wos == '1':
            from django.db.models import Q
            rec_set1 = WOStatus.objects.filter(int_rank__lt=11,int_rank__gt=0,session_id=session_id).exclude(int_rank__isnull=True).exclude(int_rank=0).order_by(F('int_rank').asc(nulls_last=True),F('due_date').asc(nulls_last=True)) 
            rec_set2 = WOStatus.objects.filter(Q(int_rank__gte=11) | Q(int_rank=0),session_id=session_id).order_by(F('due_date').asc(nulls_last=True),F('int_rank').asc(nulls_last=True))     
            #rec_set3 = WOStatus.objects.filter(int_rank=0,session_id=session_id).order_by(F('due_date').asc(nulls_last=True))
            #rec_set = rec_set1 | rec_set2 | rec_set3
            rec_set = rec_set1 | rec_set2
            #records = list(rec_set1) + list(rec_set2) + list(rec_set3)
            records = list(rec_set1) + list(rec_set2)

        elif is_dock:
            records = session_id and WOStatus.objects.filter(session_id=session_id).order_by(F('due_date').asc(nulls_last=True))
        elif is_rack == '1' and active_mode == '3':      
            records = session_id and WOStatus.objects.filter(session_id=session_id).order_by('-id')                     
        elif is_loc_whs == '1':            
            records = session_id and WarehouseLocation.objects.filter(session_id=session_id).order_by('id')  
        elif sub_grid and filter_val:      
            records = session_id and WOStatus.objects.filter(si_number = filter_val, is_detail=True,session_id=session_id).order_by('ctrl_number')
        elif is_picking:    
            records = session_id and WOStatus.objects.filter(is_detail=False,session_id=session_id).order_by('wo_number','part_number')   
        else:      
            records = session_id and WOStatus.objects.filter(session_id=session_id).order_by('-id')            
        field,direction = '',''
        if 'sort[0][dir]' in self.request.GET:
            try:
                direction = self.request.GET['sort[0][dir]']
                field = self.request.GET['sort[0][field]']
            except:
                pass 
            if isinstance(records,list):
                records = rec_set           
            if direction == 'asc':
                records = records.order_by(field)
            elif direction == 'desc':
                records = records.order_by('-'+field)
            else:
                return records
        return records

#===============================================REPAIR ORDERS=============================================#        
def get_modes(app_id=None):  
    """a.	Reserve
        b.	Un-Reserve
        c.	Issue
        d.	Un-Issue"""
    modes = app_id and AppModes.objects.filter(ml_apps_id=app_id).order_by('code') or AppModes.objects.filter(ml_apps_id=None) or None
    return modes  

def get_control(barcode,delim_str):
    ctrl_number = barcode.partition(delim_str)
    ctrl_id = ctrl_number and ctrl_number[2] or None
    ctrl_number = ctrl_number and ctrl_number[0] or None 
    return ctrl_number,ctrl_id     

def repair_order_mgmt(request,quapi_id=None):   
    location,customer,user_id = '','',''
    wo_number,user_error,stat_error,loc_error = '','','',''
    val_dict,form,updated_woos,all_woos,woo_num_list,woo_key_list = {},{},[],[],[],[]           
    msg,loc_msg,stat_msg,error,lookup_recs,clear_cart = '','','','',False,False
    loc_key,whs_key,cart_key,new_status_name=None,None,None,''
    quser=QuantumUser
    val_dict['quapi_id'] = quapi_id 
    user = request.user
    if not user.id:
        val_dict['error'] = 'Access denied.'
        return redirect('/login/')  
    user_id = user.username
    user_profile = UserProfile.objects.filter(user=user)
    user_profile = user_profile and user_profile[0] or None
    sysur_auto_key = user_profile.sysur_auto_key
    reg_user_id = user and user.is_authenticated and user.id or None 
    dj_user_id = user and quapi_id and UserQuapiRel.objects.filter(user=user,quapi_id=quapi_id) or None
    dj_user_id = dj_user_id and user.id or None
    if not reg_user_id or not dj_user_id:
        val_dict['error'] = 'Access denied.'
        return redirect('/login/')      
    user_apps = user and UserAppPerms.objects.filter(user=user) or None
    op_apps = user_apps and user_apps.filter(ml_apps_id__app_type='operations').order_by('ml_apps_id__menu_seq') or None
    val_dict['op_apps'] = op_apps
    mgmt_apps = user_apps and user_apps.filter(ml_apps_id__app_type='management').order_by('ml_apps_id__menu_seq') or None
    val_dict['mgmt_apps'] = mgmt_apps
    dash_apps = user_apps and user_apps.filter(ml_apps_id__app_type='dashboards').order_by('ml_apps_id__menu_seq') or None
    val_dict['dash_apps'] = dash_apps
    setup_apps = user_apps and user_apps.filter(ml_apps_id__app_type='setup').order_by('ml_apps_id__menu_seq') or None
    val_dict['setup_apps'] = setup_apps
    alloc_app = MLApps.objects.filter(name="RO Management")
    alloc_app = alloc_app and alloc_app[0] or None
    modes = alloc_app and get_modes(alloc_app) or []
    val_dict['sel_rows'] = 0
    user_id = user.username
    if request.method == 'GET': 
        from portal.tasks import get_statuses_nsync_beta
        form = WODashboardForm()   
        #res = get_users_nsync_beta.delay(quapi_id,dj_user_id,is_dashboard=1)
        #user_error = res.get() 
        res = get_statuses_nsync_beta.delay(quapi_id,dj_user_id,is_dashboard=1,app='ro-management',object_type='SO')
        stat_error,app = res.get()
        sel_rows = 0
    val_dict['status_vals'] = dj_user_id and StatusSelection.objects.filter(quapi_id=quapi_id,dj_user_id=dj_user_id) or [] 
    #val_dict['emp_vals'] = quapi_id and QuantumUser.objects.filter(quapi_id=quapi_id,dj_user_id=dj_user_id).distinct() or ''
    if request.method == 'POST':
        req_post = request.POST
        form = WODashboardForm(req_post)
        wo_number = 'wo_number' in req_post and req_post['wo_number'] or ''
        part_number = 'part_number' in req_post and req_post['part_number'] or ''
        label = 'label' in req_post and req_post['label'] or ''
        condition_code = 'condition_code' in req_post and req_post['condition_code'] or ''
        location = 'location' in req_post and req_post['location'] or '' 
        customer = 'customer' in req_post and req_post['customer'] or '' 
        if not dj_user_id:
            dj_user_id = 'dj_user_id' in req_post and req_post['dj_user_id'] or ''#dj admin user id
        ctrl_number,ctrl_id = get_control(label,'000000')
        if not ctrl_id:
            ctrl_number,ctrl_id = get_control(label,'00000')
        #update hidden fields
        new_status = 'new_status' in req_post and req_post['new_status'] or ''
        filter_status = 'filter_status' in req_post and req_post['filter_status'] or ''
        show_modal = 'show_modal' in req_post and req_post['show_modal'] or None
        filter_label = 'filter_label' in req_post and req_post['filter_label'] or ''
        filter_customer = 'filter_customer' in req_post and req_post['filter_customer'] or ''
        filter_wo_number = 'filter_wo_number' in req_post and req_post['filter_wo_number'] or ''
        filter_part_number = 'filter_part_number' in req_post and req_post['filter_part_number'] or ''
        filter_location = 'filter_location' in req_post and req_post['filter_location'] or ''
        filter_condition_code = 'filter_condition_code' in req_post and req_post['filter_condition_code'] or ''
        filter_session = 'filter_session' in req_post and req_post['filter_session'] or ''
        update_session = 'update_session' in req_post and req_post['update_session'] or ''
        user_session = 'user_session' in req_post and req_post['user_session'] or ''
        active_user = 'active_user' in req_post and req_post['active_user'] or ''
        update_user = 'update_user' in req_post and req_post['update_user'] or ''
        #user_id = 'user_id' in req_post and req_post['user_id'] or None       
        user_in = 'user_in' in req_post and req_post['user_in'] or ''
        #user_name = 'user_name' in req_post and req_post['user_name'] or '' 
        #fields from pop-up to carry back to main form.
        wo_stat = 'wo_stat' in req_post and req_post['wo_stat'] or ''
        cond_code = 'cond_code' in req_post and req_post['cond_code'] or ''  
        location_code = 'location_code' in req_post and req_post['location_code'] or ''
        wo_num = 'wo_num' in req_post and req_post['wo_num'] or ''
        part_num = 'part_num' in req_post and req_post['part_num'] or ''
        stock_lab = 'stock_lab' in req_post and req_post['stock_lab'] or '' 
        mode_code = 'mode_code' in req_post and req_post['mode_code'] or ''        
        #lookup user_id in the database to make sure we can authenticate
        #user_rec = QuantumUser.objects.filter(quapi_id=quapi_id,user_id__iexact=user_id)
        #user_rec = user_rec and user_rec[0] or None
        #user_rec = QuantumUser.objects.filter(quapi_id=quapi_id,user_id__iexact=user_id)
        #if not user_rec: 
        #    if update_user:
        #        user_rec = QuantumUser.objects.filter(quapi_id=quapi_id,user_id__iexact=update_user)
        #    elif user_in: 
        #        user_rec = QuantumUser.objects.filter(quapi_id=quapi_id,user_id__iexact=user_in)            
        #    else:
        #        user_rec = QuantumUser.objects.filter(quapi_id=quapi_id,user_id__iexact=active_user)                
        #user_rec = user_rec and user_rec[0] or None
        clear_form = 'clear_form' in req_post and req_post['clear_form'] or False 
        vendor_input = 'vend_input' in req_post and req_post['vend_input'] or '' 
        stm_keys = 'stm_keys' in req_post and req_post['stm_keys'] or []
        active_mode = 'mode_selector' in req_post and req_post['mode_selector'] or ''
        ro_number = 'ro_number' in req_post and req_post['ro_number'] or ''
        sel_mode = 'sel_mode' in req_post and req_post['sel_mode'] or '' 
        sel_rows = 'sel_rows' in req_post and req_post['sel_rows'] or ''
        socond_code = req_post.get('socond_code','')
        filter_socond_code = req_post.get('filter_socond_code','')
        socondition_code = req_post.get('socondition_code','')
        active_mode = active_mode or sel_mode
        if not (sel_mode or not active_mode) and not vendor_input:
            val_dict['error'] = 'Must select a method for creating ROs.'
            render(request, 'mrolive/repair_order_mgmt.html', val_dict)  
        wo_update = 'wo_update' in req_post and req_post['wo_update'] or False
        show_all = 1
        search_stock = 'search_stock' in req_post and req_post['search_stock'] or False   
        session_id = 'session_id' in req_post and req_post['session_id'] or ''
        if not session_id and not filter_session:
            session_id = 'csrfmiddlewaretoken' in req_post and req_post['csrfmiddlewaretoken'] or ''
            filter_session = session_id
            user_session = session_id
        if not session_id and filter_session:
            session_id = filter_session
            user_session = filter_session
        if not session_id and not filter_session:
            session_id = user_session
            filter_session = user_session       
        val_dict.update({
            'wo_number': wo_number,
            'all_woos': updated_woos,
            'msg': msg,
            'customer': customer,
            'condition_code': condition_code or cond_code,
            'socondition_code': socondition_code or filter_socond_code or socond_code,
            'socond_code': socond_code or filter_socond_code or socondition_code,
            'cond_code': cond_code or filter_condition_code or condition_code,
            'location': location or location_code,
            'label': label or stock_lab,
            'ctrl_id': ctrl_id,
            'ctrl_number': ctrl_number,
            'dj_user_id': dj_user_id,
            'user_id': user_id or active_user or update_user or user_in,
            'user_in': user_in or user_id or active_user or update_user,
            'active_user': active_user or user_id,
            'show_all': show_all,
            'show_modal': show_modal,
            'session_id': session_id or user_session or filter_session or update_session,
            'sel_rows': sel_rows or 0,
            'vendor_input': vendor_input,
            'form': form, 
            'quapi_id': quapi_id, 
            'active_mode': active_mode or sel_mode or mode_code or '',
            'mode_code': mode_code or active_mode or sel_mode or '',
            'sel_mode': sel_mode or active_mode or mode_code or '',
            'new_status':new_status or filter_status or wo_stat or '', 
            'filter_status': filter_status or new_status or wo_stat,  
            'wo_stat': wo_stat or new_status or filter_status,             
            'filter_wo_number': filter_wo_number or wo_number or wo_num,
            'wo_num': wo_num or filter_wo_number or wo_number,
            'part_num': part_num or filter_part_number or part_number,
            'part_number': part_number or filter_part_number or part_num,
            'filter_part_number': filter_part_number or part_num or part_number,
            'filter_label': filter_label or label or stock_lab,
            'stock_lab': stock_lab or filter_label or label,
            'filter_location': filter_location or location or location_code,
            'filter_condition_code': filter_condition_code or condition_code or cond_code, 
            'filter_socond_code': filter_socond_code or socondition_code or socond_code,
            'filter_session': filter_session or session_id or user_session,
            'update_session': update_session or session_id or user_session, 
            'user_session': user_session or update_session or filter_session or session_id,
            'ro_number': ro_number,          
            })             
        #if user submitted clear list form by pressing button
        if clear_form and req_post['clear_form']=='1':       
            WOStatus.objects.filter(user_id=user_logged,is_dashboard=0,active=1,is_racking=1).delete()
            val_dict['all_woos'] = []            
            val_dict['msg'] = '' 
            val_dict['show_all'] = 1  
            form = WODashboardForm(val_dict)
            val_dict['form'] = form                         
            return render(request, 'mrolive/repair_order_mgmt.html', val_dict)                         
        stm_key_list = []
        woo_keys = []
        selection = None
        if 'stm_key_list[]' in req_post:
            stm_key_list = req_post.getlist('stm_key_list[]') 
            stm_key_tuple = tuple([int(stm) for stm in stm_key_list])
            selection = WOStatus.objects.filter(stm_auto_key__in = stm_key_tuple,session_id=session_id)  
            woo_keys = [woo.woo_auto_key for woo in selection]
        if not wo_update and ((ctrl_number and ctrl_id) or socondition_code or wo_number or part_number or condition_code or location or customer or new_status):
            from portal.tasks import run_ro_mgmt
            res = run_ro_mgmt.delay(
                session_id,
                wo_number=wo_number,
                part_number=part_number,
                customer=customer,
                location=location,
                condition_code=condition_code,
                socond_code=socondition_code,
                user_id=user_id,
                sysur_auto_key=sysur_auto_key,
                stock_label = label,
                ctrl_id = ctrl_id,
                ctrl_number = ctrl_number,
                quapi_id = quapi_id,
                clear_cart = clear_cart,
                dj_user_id = dj_user_id,
                wos_auto_key = new_status,
            )
            error,msg = res.get()
            val_dict['sel_rows'] = 0
            
        elif (active_mode in ['1','2'] or ro_number):
            if stm_key_list:            
                from portal.tasks import add_new_ro
                #if user enters a ro_number:
                if ro_number:
                    res = add_new_ro.delay(quapi_id,session_id,sysur_auto_key,ro_number=ro_number,stm_keys=stm_key_list,last_vendor=False,woo_keys=woo_keys)
                    error,msg = res.get()
                elif active_mode == '2' and selection:
                    #need to raise the pop-up to prompt for vendor_input.
                    val_dict['show_modal'] = '1'
                    val_dict['user_session'] = session_id                       
                    val_dict['stm_keys'] = selection
                    #get vendors now that we know we're going to need them
                    from portal.tasks import get_companies_n_sync
                    res = get_companies_n_sync.delay(quapi_id,dj_user_id,is_vendor=True)
                    error = res.get()
                    vendor_vals = Companies.objects.filter(quapi_id=quapi_id,dj_user_id=dj_user_id,is_vendor=True)
                    val_dict['vendor_vals'] = vendor_vals
                elif active_mode == '1':
                    #get the last vendor via sql query and create a new RO with that vendor
                    res = add_new_ro.delay(quapi_id,session_id,sysur_auto_key,stm_keys=stm_key_list,last_vendor=True,woo_keys=woo_keys)
                    error,msg = res.get()
            else:
                error = 'You must select at least one stock record in the grid to proceed.'
                
        elif vendor_input:  
            stm_keys_sel = 'stm_keys_sel' in req_post and req_post['stm_keys_sel'] or []
            if 'stm_keys_sel[]' in req_post:
                stm_keys_sel = req_post.getlist('stm_keys_sel[]')
            stm_key_list =  tuple([int(stm) for stm in stm_keys_sel])        
            from portal.tasks import add_new_ro
            #call the task that adds a new RO
            vendors = Companies.objects.filter(name=vendor_input,dj_user_id=dj_user_id,quapi_id=quapi_id)
            vendor_id = vendors and vendors[0] or None
            vendor_id = vendor_id and vendor_id.cmp_auto_key or None
            val_dict['session_id'] = user_session
            session_id = user_session 
            selection = stm_key_list and WOStatus.objects.filter(session_id=session_id,stm_auto_key__in=stm_key_list) or [] 
            woo_keys = [woo.woo_auto_key for woo in selection] 
            if vendor_id:
                res = add_new_ro.delay(quapi_id,session_id,sysur_auto_key,stm_keys=stm_keys_sel,vendor=vendor_id,last_vendor=False,woo_keys=woo_keys)
                error,msg = res.get()  
                val_dict['msg'] = msg
                val_dict['error'] = error                 
                val_dict['show_modal'] = '0' 
            else:
                val_dict['error'] = 'Vendor not found. Must select from the list'            
        #if user has already entered a vendor:
        #the user clicked the "New RO" button so we add a new one with the stock lines as RO's
        stm_key_list =[int(stm) for stm in stm_key_list]
        options_col,page_size = get_options(req_post,session_id)
        updated_woos = WOStatus.objects.filter(session_id=session_id)
        updated_woos = updated_woos.exclude(stm_auto_key__in=stm_key_list)
        val_dict['page_size'] = page_size
        val_dict['options_col'] = options_col
        val_dict['all_woos'] = updated_woos
        val_dict['total_rows'] = str(len(updated_woos))
        val_dict['msg'] = msg
        val_dict['error'] = error        
    form = WODashboardForm(val_dict)
    val_dict['form'] = form
    val_dict['num_records'] = user_profile.num_records or 10
    val_dict['modes'] = modes
    val_dict['error'] = error 
    return render(request, 'mrolive/repair_order_mgmt.html', val_dict)
  
def get_options(req_post,session_id):
    page_size = 'options_pagesize' in req_post and req_post['options_pagesize'] or 25
    options_col = 'options_col' in req_post and req_post['options_col'] or '' 
    if not options_col:
         options_col = 'update_col' in req_post and req_post['update_col'] or ''
         page_size = 'update_pagesize' in req_post and req_post['update_pagesize'] or 25
    if not options_col:
         options_col = 'vendor_col' in req_post and req_post['vendor_col'] or ''
         page_size = 'vendor_pagesize' in req_post and req_post['vendor_pagesize'] or 25
    if not options_col:
         options_col = 'split_ro_col' in req_post and req_post['split_ro_col'] or ''
         page_size = 'split_ro_pagesize' in req_post and req_post['split_ro_pagesize'] or 25
    if not options_col:
         options_col = 'loc_col' in req_post and req_post['loc_col'] or ''
         page_size = 'loc_pagesize' in req_post and req_post['loc_pagesize'] or 25
    if options_col:
        convert_to_dict = options_col.replace('true','True')
        convert_to_dict = convert_to_dict.replace('false','False') or None
        options_col = convert_to_dict and eval(convert_to_dict) or []
        num = 0
        col_recs = []
        cols_to_del = ColumnSettings.objects.filter(session_id=session_id)
        cols_to_del.delete()
        for col in options_col:
            #store each column with its name and widths
            col_recs.append(ColumnSettings(
                    name = 'title' in col and col['title'] or '',
                    field = 'field' in col and col['field'] or '',
                    width = 'width' in col and col['width'] and float(col['width']) or 80,
                    tmpl_text = 'template' in col and col['template'] or '',
                    type = 'grid',
                    session_id = session_id,
                    seq_num = num,
                )
            )  
            num += 1
        try:
            ColumnSettings.objects.bulk_create(col_recs)
        except Exception as exc:
            error = "\r\Problem with creating column settings locally: %s"%exc 
        options_col = ColumnSettings.objects.filter(session_id=session_id)
    return options_col,page_size
