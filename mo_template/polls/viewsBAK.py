#!/usr/bin/env python3
# -*- coding: utf8 -*-
# encoding=utf8
from polls.models import MoTemplate,PILogs,WOStatus,QueryApi,StatusSelection,QuantumUser,AppModes,AuditTrail,MLApps,UserAppPerms,UserQuapiRel
from django.http import Http404
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
import os
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

#*********************************Authentication Code**************************************************************  
def account_route(request):
    #get current user's SQLite db id
    app_sel,quapi_sel,app_selected,quapi_selected,red='','','','',''
    req_post = None
    quapis = QueryApi.objects.all()
    apps = MLApps.objects.all()
    #import pdb;pdb.set_trace()
    if request.method == 'POST':
        #based on the user's selection of quapi and app, we will route to the appropriate place
        req_post = request.POST
        app_selected = 'app_selector' in req_post and req_post['app_selector'] or ''
        app_sel = app_selected and apps.filter(id=app_selected) or '' 
        app_sel = app_sel and app_sel[0] or None
        quapi_selected = 'quapi_selector' in req_post and req_post['quapi_selector'] or ''
        quapi_sel = quapi_selected and quapis.filter(id=quapi_selected) or None   
        quapi_sel = quapi_sel and quapi_sel[0] or None             
    user = request.user
    user_id = user and user.is_authenticated and user.id or None
    #check user_id in the rel table that associates the Django app user
    #with the quantum user
    session_id = request.session and request.session.session_key or None 
    quapi_id = user_id and quapis and quapis.filter(dj_user_id = user_id) or None
    quapi_id = quapi_id and quapi_id[0] or None
    user_apps = user_id and UserAppPerms.objects.all().filter(dj_user_id = user_id) or None

    val_dict = {
        'app_set': user_apps,
        'app_sel': app_sel and app_sel.id or None,
        'user_id': user_id,
        'quapi_id': quapi_id and quapi_id.id or None,
        'quapi_set': quapis,
        'quapi_sel': quapi_selected,        
        'session_id': session_id,
        }
    if req_post and user_id:
        app_view = app_sel and '/mrolive/' + str(app_sel.code) + '/' + str(quapi_selected) or None
        #url = app_view and quapi_id and request.build_absolute_uri(reverse(app_view, args=(quapi_id, ))) or None
        #app_view = app_sel and '/mrolive/' + str(app_sel.code) or None
        if app_view:
            return redirect(app_view)
    return render(request, 'registration/home.html', val_dict) 

def app_mgmt(request):
    #get current user's SQLite db id
    app_sel,app_selected,user_sel,user_selected,error,res,dj_user_name='','','','','','',''
    req_post,dupe_app,dupe_quapi = None,False,False
    apps = MLApps.objects.all()
    user = request.user
    username = user and user.username or 'No Username'
    user_id = user and user.is_authenticated and user.id or None
    from django.contrib.auth.models import User
    users = User.objects.all()
    quapis = QueryApi.objects.all()
    #import pdb;pdb.set_trace()
    if request.method == 'POST':
        #based on the user's selection of quapi and app, we will route to the appropriate place
        req_post = request.POST
        app_selected = 'app_selected' in req_post and req_post['app_selected'] or ''
        app_sel = app_selected and apps.filter(id=app_selected) or '' 
        app_sel = app_sel and app_sel[0] or None
        user_selected = 'user_selected' in req_post and req_post['user_selected'] or ''
        user_sel = user_selected and users.filter(id=user_selected) or None   
        user_sel = user_sel and user_sel[0] or 0        
        dj_user_name = user_sel.username
        quapi_selected = 'quapi_selector' in req_post and req_post['quapi_selector'] or ''
        quapi_sel = quapi_selected and quapis.filter(id=quapi_selected) or None   
        quapi_sel = quapi_sel and quapi_sel[0] or None         
    #check user_id in the rel table that associates the Django app user
    #with the quantum user
    session_id = request.session and request.session.session_key or None
    user_perms = user_selected and UserAppPerms.objects.filter(dj_user_id=user_selected) or []
    val_dict = {
        'app_set': apps,
        'app_sel': app_selected and int(app_selected) or None,
        'user_id': user_id,
        'user_sel': user_selected and int(user_selected) or None, 
        'quapi_sel': quapi_selected and int(quapi_selected) or None,        
        'user_perms': user_perms,  
        'users': users,        
        'session_id': session_id,
        'error': error,
        'quapi_set': quapis,
        }
    if user_selected and app_selected and app_sel:
        search_dupes = UserAppPerms.objects.filter(dj_user_id=user_selected,ml_apps_id=app_sel)
        if search_dupes:
            val_dict['error'] = 'This user already has global access to that app'
            dupe_app = True
            #return render(request, 'registration/app_management.html', val_dict)            
        if not dupe_app:
            try:
                res = UserAppPerms(dj_username=dj_user_name,dj_user_id=user_selected,ml_apps_id=app_sel)   
                res.save()   
            except Exception as exc:
                logger.exception('Creating permissions caused this exception: %r', exc) 
    user_perms = user_selected and UserAppPerms.objects.filter(dj_user_id=user_selected) or []
    if user_selected and quapi_selected and quapi_sel:
        search_dupes = QueryApi.objects.filter(dj_user_id=user_selected,id=quapi_selected)
        if search_dupes:
            val_dict['error'] = 'This user is already associated with that schema.'
            dupe_quapi = True
            #return render(request, 'registration/app_management.html', val_dict) 
        if not dupe_quapi:            
            try:
                res = UserQuapiRel(dj_username=dj_user_name,dj_user_id=user_selected,quapi_id=quapi_sel)   
                res.save()   
            except Exception as exc:
                logger.exception('Creating API access for the user caused this exception: %r', exc) 
    user_schema = user_selected and UserQuapiRel.objects.filter(dj_user_id=user_selected) or []
    val_dict['user_perms'] = user_perms
    val_dict['user_schema'] = user_schema
    return render(request, 'registration/app_management.html', val_dict)    
#**************************************************End User Accounts and Sessions**********************************************************   
#*********************************Begin WO Dashboards*************************************************************
def dashboard(request,quapi_id=None):
    new_status,location,filter_status = '','',''
    user_id,user_rec = 'user not set',None
    wo_number = ''
    val_dict = {}
    all_woos = WOStatus.objects.all().filter(active=1, is_dashboard=1, session_id='') 
    updated_woos = all_woos 
    woos_updated = False    
    error,msg,loc_msg,stat_msg = '','','',''
    woos_updated = False
    from polls.models import StatusSelection as stat_sel, QueryApi
    dj_user_id = quapi_id and QueryApi.objects.all().filter(id=quapi_id) or None
    dj_user_id = dj_user_id and dj_user_id[0] and dj_user_id[0].dj_user_id or None
    user = request.user
    reg_user_id = user and user.is_authenticated and user.id or None
    if not dj_user_id or (dj_user_id and dj_user_id != reg_user_id):
        error += 'Access denied.'
        val_dict['error'] = error
        return render(request, 'polls/wodashboards.html', val_dict)      
    from polls.tasks import run_updates,get_statuses_nsync
    if request.method == 'GET':
        res = get_statuses_nsync.delay(is_dashboard=1,quapi_id=quapi_id)
        stat_error = res.get()             
    val_dict['status_vals'] = dj_user_id and stat_sel.objects.all().filter(dj_user_id=dj_user_id).distinct() or [] 
    if request.method == 'POST':
        customer = 'customer' in request.POST and request.POST['customer'] or ''
        wo_number = 'wo_number' in request.POST and request.POST['wo_number'] or ''
        new_status = 'status_selector' in request.POST and request.POST['status_selector'] or ''
        due_date = 'get_due_date' in request.POST and request.POST['get_due_date'] or ''
        new_due_date = 'due_date' in request.POST and request.POST['due_date'] or '' 
        search_mgr = 'get_manager' in request.POST and request.POST['get_manager'] or ''
        manager = 'manager' in request.POST and request.POST['manager'] or ''
        rank = 'rank' in request.POST and request.POST['rank'] or ''
        user_id = 'user_id' in request.POST and request.POST['user_id'] or ''
        #update hidden fields
        filter_status = 'filter_status' in request.POST and request.POST['filter_status'] or ''
        filter_due_date = 'filter_due_date' in request.POST and request.POST['filter_due_date'] or ''
        filter_customer = 'filter_customer' in request.POST and request.POST['filter_customer'] or ''
        filter_number = 'filter_number' in request.POST and request.POST['filter_number'] or ''
        filter_manager = 'filter_manager' in request.POST and request.POST['filter_manager'] or ''
        filter_session = 'filter_session' in request.POST and request.POST['filter_session'] or ''
        update_session = 'update_session' in request.POST and request.POST['update_session'] or ''
        session_id = 'csrfmiddlewaretoken' in request.POST and request.POST['csrfmiddlewaretoken'] or ''
        total_rows = 'total_rows' in request.POST and request.POST['total_rows'] or 0
        sel_rows = 'sel_rows' in request.POST and request.POST['sel_rows'] or 0        
        val_dict.update({
            'all_woos': updated_woos, 
            'msg': msg,
            'new_status': new_status or filter_status, 
            'customer': customer,
            'get_due_date': due_date,
            'new_due_date': new_due_date,
            'user_id': user_id or '',
            'manager': manager,
            'get_manager': search_mgr,
            'rank': rank,
            'wo_number': wo_number,
            'filter_status': filter_status or new_status,
            'filter_customer': filter_customer or customer,
            'filter_number': filter_number or wo_number,
            'filter_due_date': filter_due_date or due_date,
            'filter_manager': filter_manager or search_mgr,
            'filter_session': filter_session or session_id,#even when the update form is submitted, filter session always takes
            'update_session': update_session or session_id,
            'session_id': session_id,
            'sel_rows': sel_rows,
            'total_rows': total_rows,
        })
        from polls.tasks import add_wo_record
        res = add_wo_record.delay(quapi_id=quapi_id,user_id='',customer=customer,status=new_status,manager=search_mgr,due_date=due_date,wo_number=wo_number,session_id=session_id) 
        error,msg = res.get()  
        if error == 'no errors':
            error = ''        
        updated_woos = WOStatus.objects.all().filter(active=1, is_dashboard=1, session_id=session_id)
        val_dict['all_woos'] = updated_woos                      
    val_dict['msg'] = msg
    val_dict['error'] = error
    val_dict['total_rows'] = str(len(updated_woos))
    return render(request, 'polls/wodashboards.html', val_dict)     
    
def management(request,quapi_id=None):
    new_status,location,filter_status = '','',''
    user_id,user_rec = 'user not set',None
    wo_number = ''
    val_dict = {}
    all_woos = WOStatus.objects.all().filter(active=1, is_dashboard=1, session_id='') 
    updated_woos = all_woos 
    woos_updated = False    
    msg,loc_msg,stat_msg = '','',''
    from polls.models import StatusSelection as stat_sel,QuantumUser as quser, QueryApi
    dj_user_id = quapi_id and QueryApi.objects.all().filter(id=quapi_id) or None
    dj_user_id = dj_user_id and dj_user_id[0] and dj_user_id[0].dj_user_id or None
    user = request.user
    reg_user_id = user and user.is_authenticated and user.id or None
    if not dj_user_id or (dj_user_id and dj_user_id != reg_user_id):
        error = 'Access denied.'
        val_dict['error'] = error
        return render(request, 'polls/womgmt.html', val_dict)  
    from polls.tasks import run_updates,get_statuses_nsync,get_users_nsync
    if request.method == 'GET':
        res = get_statuses_nsync.delay(is_dashboard=1,quapi_id=quapi_id)
        stat_error = res.get() 
        res = get_users_nsync.delay(is_dashboard=1,quapi_id=quapi_id)
        user_error = res.get()   
        val_dict['sel_rows'] = 0        
    val_dict['emp_vals'] = dj_user_id and quser.objects.all().filter(dj_user_id=dj_user_id).distinct() or [] 
    val_dict['status_vals'] = dj_user_id and stat_sel.objects.all().filter(is_dashboard=1,dj_user_id=dj_user_id).distinct()
    woos_updated = False
    if request.method == 'POST':
        customer = 'customer' in request.POST and request.POST['customer'] or ''
        wo_number = 'wo_number' in request.POST and request.POST['wo_number'] or ''
        new_status = 'new_status' in request.POST and request.POST['new_status'] or ''
        status_rec = new_status and StatusSelection.objects.filter(name=new_status) or None
        status_wosak = status_rec and status_rec[0] and status_rec[0].wos_auto_key or None
        due_date = 'get_due_date' in request.POST and request.POST['get_due_date'] or ''
        new_due_date = 'due_date' in request.POST and request.POST['due_date'] or '' 
        search_mgr = 'get_manager' in request.POST and request.POST['get_manager'] or ''
        manager = 'manager' in request.POST and request.POST['manager'] or ''
        rank = 'rank' in request.POST and request.POST['rank'] or ''
        user_id = 'user_id' in request.POST and request.POST['user_id'] or ''
        total_rows = 'total_rows' in request.POST and request.POST['total_rows'] or 0
        sel_rows = 'sel_rows' in request.POST and request.POST['sel_rows'] or 0
        #update hidden fields
        filter_status = 'filter_status' in request.POST and request.POST['filter_status'] or ''
        filter_status_rec = filter_status and StatusSelection.objects.filter(name=filter_status) or None
        filter_status_wosak = filter_status_rec and filter_status_rec[0] and filter_status_rec[0].wos_auto_key or None
        filter_due_date = 'filter_due_date' in request.POST and request.POST['filter_due_date'] or ''
        filter_customer = 'filter_customer' in request.POST and request.POST['filter_customer'] or ''
        filter_number = 'filter_number' in request.POST and request.POST['filter_number'] or ''
        filter_manager = 'filter_manager' in request.POST and request.POST['filter_manager'] or ''
        filter_session = 'filter_session' in request.POST and request.POST['filter_session'] or ''
        update_session = 'update_session' in request.POST and request.POST['update_session'] or ''
        session_id = 'csrfmiddlewaretoken' in request.POST and request.POST['csrfmiddlewaretoken'] or ''     
        val_dict.update({
            'all_woos': updated_woos, 
            'msg': msg,
            'new_status':new_status or filter_status, 
            'customer': customer or filter_customer,
            'get_due_date': due_date or filter_due_date,
            'new_due_date': new_due_date or filter_due_date,
            'user_id': user_id or '',
            'manager': manager,
            'get_manager': search_mgr or filter_manager,
            'rank': rank,
            'wo_number': wo_number or filter_number,
            'filter_status': filter_status or new_status,
            'filter_customer': filter_customer or customer,
            'filter_number': filter_number or wo_number,
            'filter_due_date': filter_due_date or due_date,
            'filter_manager': filter_manager or search_mgr,
            'filter_session': filter_session or session_id,#even when the update form is submitted, filter session always takes
            'update_session': update_session or session_id,
            'session_id': session_id,
            'sel_rows': sel_rows,
            'total_rows': total_rows,
            #'search_user': search_user,
        })
        woo_id_list = []
        if 'woos_list[]' in request.POST:
            woo_id_list = request.POST.getlist('woos_list[]')                             
        #when filter form submitted, filter_session is '', 
        #when update form submitted, filter_session took 
        #initial filter session page load and stored it on the wo record.   
        #when an update has to match the wo's, it looks for the filter's session_id
        #(search/filter form) session_id == filter_session (update form)        
        if 'user_id' in request.POST and not user_id:
            msg += 'You must enter your Employee ID before updating any WO\'s.'
            val_dict['msg'] = msg
            return render(request, 'polls/womgmt.html', val_dict)
        elif user_id:         
            #lookup user_id in the database to make sure we can authenticate
            user_rec = QuantumUser.objects.all().filter(user_id=user_id)
            user_rec = user_rec and user_rec[0] or None
            if not user_rec:
                msg += 'Invalid employee number.  Please enter a valid one.'
                val_dict['msg'] = msg
                return render(request, 'polls/womgmt.html', val_dict)
            if (rank or new_due_date or manager):
                #now, set the user on the active woos for the dashboard / csrfmiddlewaretoken
                #woos_update = WOStatus.objects.all().filter(active=1, is_dashboard=1, user_id = '', session_id = filter_session)
                #foos = WOStatus.objects.all().filter(active=1, is_dashboard=1, session_id = (filter_session or update_session))
                update_the_woos = WOStatus.objects.all().filter(active=1, is_dashboard=1, session_id = (filter_session or update_session)).update(user_id=user_id,reg_user_id = user_rec)                                 
                try:                
                    from polls.tasks import make_updates
                    res = make_updates.delay(
                        user_id=user_id, 
                        rank=rank,
                        manager=manager,
                        due_date=due_date,
                        new_due_date=new_due_date or due_date,
                        customer=filter_customer,
                        status=status_wosak,
                        search_mgr=filter_manager or manager,
                        wo_number=filter_number,
                        session_id=filter_session or update_session,
                        woo_id_list=woo_id_list,
                        quapi_id=quapi_id,
                        )
                    error,msg = res.get()                     
                    updated_woos = WOStatus.objects.all().filter(active=1, is_dashboard=1, user_id=user_id, session_id=(filter_session or update_session)) 
                    val_dict['all_woos'] = updated_woos
                    val_dict['sel_rows'] = 0 
                except Exception as exc:
                    logger.exception('Sending make_updates task raised this exception: %r', exc)                                          
        else:
            from polls.tasks import add_wo_record
            res = add_wo_record.delay(customer=customer,status=status_wosak,manager=search_mgr,due_date=due_date,wo_number=wo_number,session_id=session_id,quapi_id=quapi_id) 
            error,msg = res.get()            
            updated_woos = WOStatus.objects.all().filter(active=1, is_dashboard=1, session_id=session_id)
            val_dict['all_woos'] = updated_woos 
            val_dict['sel_rows'] = 0            
    val_dict['msg'] = msg
    val_dict['total_rows'] = str(len(updated_woos))
    return render(request, 'polls/womgmt.html', val_dict)
    
#****************************************************begin wostatus****************************************************************   
def get_control(barcode,delim_str):
    ctrl_number = barcode.partition(delim_str)
    ctrl_id = ctrl_number and ctrl_number[2] or None
    ctrl_number = ctrl_number and ctrl_number[0] or None 
    return ctrl_number,ctrl_id 
    
def get_modes():  
    """AppModes.objects.all().delete()    
    mode_one = AppModes.objects.create(name='Update', code=1)
    mode_one.save()
    mode_two = AppModes.objects.create(name='Transfer Cart', code=2)
    mode_two.save()   
    mode_three = AppModes.objects.create(code=3,name='Validate')
    mode_three.save()"""
    return AppModes.objects.order_by('code')

def racking(request,quapi_id=None):  
    location,user_id,user_logged,update,warehouse,rack,new_rack,rerack,rack_user = '','','','','','','','',''
    wo_number = ''
    val_dict,updated_woos,all_woos,woo_num_list,woo_key_list = {},[],[],[],[]           
    msg,loc_msg,stat_msg,error,lookup_recs = '','','','',False
    modes = get_modes()
    val_dict['modes'] = modes
    from polls.models import StatusSelection as stat_sel,QuantumUser as quser, QueryApi
    dj_user_id = quapi_id and QueryApi.objects.all().filter(id=quapi_id) or None
    dj_user_id = dj_user_id and dj_user_id[0] and dj_user_id[0].dj_user_id or None
    user = request.user
    reg_user_id = user and user.is_authenticated and user.id or None
    if not dj_user_id or (dj_user_id and dj_user_id != reg_user_id):
        error += 'Access denied.'
        val_dict['error'] = error
        return render(request, 'polls/racking.html', val_dict)  
    from polls.tasks import run_updates,get_statuses_nsync,get_users_nsync
    if request.method == 'GET':
        res = get_statuses_nsync.delay(is_dashboard=0,quapi_id=quapi_id)
        stat_error = res.get() 
        res = get_users_nsync.delay(is_dashboard=0,quapi_id=quapi_id)
        user_error = res.get()         
    val_dict['emp_vals'] = dj_user_id and quser.objects.all().filter(dj_user_id=dj_user_id).distinct() or [] 
    val_dict['status_vals'] = dj_user_id and stat_sel.objects.all().filter(is_dashboard=0,dj_user_id=dj_user_id).distinct() 
    if request.method == 'POST':
        req_post = request.POST
        total_rows = 'total_rows' in request.POST and request.POST['total_rows'] or 0
        sel_rows = 'sel_rows' in request.POST and request.POST['sel_rows'] or 0
        session_id = 'session_id' in request.POST and request.POST['session_id'] or ''
        if not session_id:
            session_id = 'csrfmiddlewaretoken' in request.POST and request.POST['csrfmiddlewaretoken'] or ''
        user_id = 'user_id' in req_post and req_post['user_id'] or ''#sysur_auto_key
        user_logged = 'user_logged' in req_post and req_post['user_logged'] or ''
        rack_user = 'rack_user' in req_post and req_post['rack_user'] or '' 
        user_id = user_id or user_logged or rack_user or ''
        #lookup user_id in the database to make sure we can authenticate
        user_rec = QuantumUser.objects.all().filter(user_id=user_id)
        user_rec = user_rec and user_rec[0] or None
        clear_form = 'clear_form' in req_post and req_post['clear_form'] or False       
        wo_number = 'wo_number' in req_post and req_post['wo_number'] or ''
        lookup_recs = 'lookup_recs' in req_post and req_post['lookup_recs'] or False           
        location = 'location' in req_post and req_post['location'] or '' 
        rack = 'rack' in req_post and req_post['rack'] or '' 
        new_rack = 'new_rack' in req_post and req_post['new_rack'] or '' 
        warehouse = 'warehouse' in req_post and req_post['warehouse'] or ''
        active_mode = 'mode_selector' in req_post and req_post['mode_selector'] or ''
        sel_mode = 'sel_mode' in req_post and req_post['sel_mode'] or ''        
        new_status = 'new_status' in request.POST and request.POST['new_status'] or ''
        status_rec = new_status and StatusSelection.objects.filter(name=new_status) or None
        status_wosak = status_rec and status_rec[0] and status_rec[0].wos_auto_key or None        
        show_status = 'show_status' in req_post and req_post['show_status'] or ''
        do_status = active_mode and active_mode == '1' or False         
        val_dict.update({
            'all_woos': updated_woos,
            'msg': msg,
            'warehouse': warehouse,
            'location': location,
            'user_id': user_id or user_logged or rack_user,
            'rack': rack or new_rack,
            'user_logged': user_logged or user_id,
            'rack_user': user_id,
            'new_rack': rack,
            'modes': modes,
            'active_mode': active_mode or sel_mode or '',
            'sel_mode': sel_mode or active_mode or '',
            'new_status': new_status,
            'lookup_recs': lookup_recs,
            'show_status': show_status or do_status,
            'do_status': do_status or show_status,
            'session_id': session_id,
            'sel_rows': sel_rows,
            'total_rows': total_rows,
            })  
        if not user_rec and clear_form != '1':
            error += 'Invalid employee number.  Please enter a valid one.'
            val_dict['error'] = error
            return render(request, 'polls/racking.html', val_dict)
        #if user submitted clear list form by pressing button
        if clear_form and req_post['clear_form']=='1':         
            WOStatus.objects.all().filter(user_id=user_logged,is_dashboard=0,active=1,is_racking=1).delete()
            val_dict['all_woos'] = []            
            val_dict['msg'] = 'Values cleared.' 
            val_dict['active_mode'] = sel_mode            
            return render(request, 'polls/racking.html', val_dict)            
        ctrl_number,ctrl_id = get_control(wo_number,'000000')
        if not ctrl_id:
            ctrl_number,ctrl_id = get_control(wo_number,'00000')
        sysur_auto_key = user_rec and user_rec.user_auto_key or ''
        all_woos = WOStatus.objects.all().filter(active=1,is_dashboard=0,is_racking=1,user_id=user_id)  
        keys = set(woo.woo_auto_key for woo in all_woos)
        woo_key_list = list(keys)
        #if user submitted Re-rack form by pressing button with same name
        if 'new_rack' in req_post and req_post['new_rack']:      
            rerack = True           
        from polls.tasks import run_racking
        res = run_racking.delay(
            session_id,
            rack = rack,
            location=location,
            wo_number=wo_number,
            warehouse=warehouse,
            new_status=status_wosak,
            user_id=user_id,
            sysur_auto_key=sysur_auto_key,
            woo_key_list=woo_key_list,
            ctrl_id = ctrl_id,
            ctrl_number = ctrl_number,
            mode = active_mode,
            lookup_recs = lookup_recs,
            quapi_id = quapi_id,
        )
        error,msg = res.get()
        updated_woos = WOStatus.objects.all().filter(active=1,is_dashboard=0,user_id=user_id,is_racking=1)
        val_dict['all_woos'] = updated_woos 
        val_dict['total_rows'] = str(len(updated_woos))
        val_dict['msg'] = msg   
        val_dict['error'] = error        
        if not wo_number and lookup_recs not in [1,'1']:
            val_dict['lookup_recs'] = 1
        elif wo_number and lookup_recs not in [0,'0']:
            val_dict['lookup_recs'] = 0         
    return render(request, 'polls/racking.html', val_dict) 
    
def barcoding(request,quapi_id):
    new_status,location,user_id,update = '','','','' 
    wo_number = ''
    val_dict,updated_woos,all_woos,woo_num_list = {},[],[],[]           
    msg,loc_msg,stat_msg,error = '','','',''
    from polls.models import StatusSelection as stat_sel,QuantumUser as quser, QueryApi
    dj_user_id = quapi_id and QueryApi.objects.all().filter(id=quapi_id) or None
    dj_user_id = dj_user_id and dj_user_id[0] and dj_user_id[0].dj_user_id or None
    user = request.user
    reg_user_id = user and user.is_authenticated and user.id or None
    if not dj_user_id or (dj_user_id and dj_user_id != reg_user_id):
        error += 'Access denied.'
        val_dict['error'] = error
        return render(request, 'polls/wostatus.html', val_dict)      
    from polls.tasks import run_updates,get_statuses_nsync,get_users_nsync
    if request.method == 'GET':
        res = get_statuses_nsync.delay(is_dashboard=0,quapi_id=quapi_id)
        stat_error = res.get() 
        res = get_users_nsync.delay(is_dashboard=0,quapi_id=quapi_id)
        user_error = res.get()             
    emp_vals = dj_user_id and quser.objects.all().filter(dj_user_id=dj_user_id).distinct() or [] 
    status_vals = dj_user_id and stat_sel.objects.all().filter(is_dashboard=0,dj_user_id=dj_user_id).distinct()    
    val_dict['status_vals'] = status_vals 
    val_dict['emp_vals'] = emp_vals   
    if request.method == 'POST':
        user_id = 'user_id' in request.POST and request.POST['user_id'] or ''     
        #lookup user_id in the database to make sure we can authenticate
        user_rec = QuantumUser.objects.all().filter(user_auto_key=user_id and int(user_id) or 0)
        user_rec = user_rec and user_rec[0] or None
        clear_form = 'clear_form' in request.POST and request.POST['clear_form'] or False
        wo_number = 'wo_number' in request.POST and request.POST['wo_number'] or ''
        new_status = 'status_selector' in request.POST and request.POST['status_selector'] or ''          
        location = 'location' in request.POST and request.POST['location'] or ''
        if not clear_form and not user_rec:
            error += 'Invalid employee number.  Please enter a valid one.'
            val_dict.update({
            'all_woos': all_woos, 
            'msg': msg,
            'error': error,
            'new_status': new_status and int(new_status) or None, 
            'new_location': location,
            'user_id': user_id and int(user_id) or None, 
            'emp_vals': emp_vals,
            })
            return render(request, 'polls/wostatus.html', val_dict)
        all_woos = user_rec and WOStatus.objects.all().filter(active=1,is_dashboard=0,user_id=user_rec.user_id,is_racking=0) or []
        keys = set(woo.woo_auto_key for woo in all_woos)
        woo_key_list = list(keys)
        woos_to_clear = 'woos_to_clear[]' in request.POST and request.POST['clear_form']=='1'
        if not woos_to_clear:
            res = run_updates.delay(
                location=location,
                wo_number=wo_number,
                new_status=new_status,
                user_id=user_rec and user_rec.user_id or '',
                sysur_auto_key=user_id,
                woo_key_list=woo_key_list,
                quapi_id=quapi_id,
            )
            error,msg = res.get()
        #if user submitted clear list form by pressing button
        else:
            woos_to_remove = request.POST.getlist('woos_to_clear[]')                        
            if isinstance(woos_to_remove, list):
                #for woo_id in woos_to_remove:                  
                WOStatus.objects.all().filter(pk__in=woos_to_remove).delete()
        updated_woos = user_rec and WOStatus.objects.all().filter(active=1,is_dashboard=0,user_id=user_rec.user_id,is_racking=0) or []
    val_dict = {
        'status_vals': status_vals,
        'all_woos': updated_woos,
        'msg': msg,
        'error': error,
        'new_status': new_status and int(new_status) or None, 
        'new_location': location,
        'user_id': user_id and int(user_id) or None, 
        'emp_vals': emp_vals,
        }            
    return render(request, 'polls/wostatus.html', val_dict)

#++++++++++++===================Audit Trail Code============================++++++++++++++++++
def audit_trail(request):
    from polls.models import AuditTrail as Adt
    msg = ''
    val_dict,results = {},[]
    right_now = datetime.now()
    date_to_input = right_now.strftime('%m/%d/%Y')
    date_from_input = right_now - timedelta(days=45)
    date_from_input = date_from_input.strftime('%m/%d/%Y')
    filter_user_id,active_app,msg = '','',''
    user_apps = MLApps.objects.all()
    from polls.models import QueryApi
    dj_user_id = quapi_id and QueryApi.objects.all().filter(id=quapi_id) or None
    dj_user_id = dj_user_id and dj_user_id[0] and dj_user_id[0].dj_user_id or None
    user = request.user
    reg_user_id = user and user.is_authenticated and user.id or None
    if not dj_user_id or (dj_user_id and dj_user_id != reg_user_id):
        error += 'Access denied.'
        val_dict['error'] = error
        return render(request, 'polls/racking.html', val_dict)   
    if request.method == 'POST':
        req_post = request.POST
        format = '%Y-%m-%d %H:%M:%S'
        new_format = '%m-%d-%Y %H:%M:%S'
        filter_user_id = 'user_id' in req_post and req_post['user_id'] or None
        date_from_input = 'date_from' in req_post and req_post['date_from'] or None
        date_from = date_from_input and datetime.strptime(date_from_input, new_format) or None
        date_from = date_from and datetime.strftime(date_from, format) or None
        date_to_input = 'date_to' in req_post and req_post['date_to'] or None
        date_to = date_to_input and datetime.strptime(date_to_input, new_format) or None
        date_to = date_to and datetime.strftime(date_to, format) or None
        active_app = 'app_selector' in req_post and req_post['app_selector'] or None
    user_id = filter_user_id and QuantumUser.objects.all().filter(user_id=filter_user_id) or None
    user_id = user_id and user_id[0] or None
    app_id = active_app and user_apps.filter(id=active_app) or None
    app_id = app_id and app_id[0] or None
    results = app_id and user_id and Adt.objects.all().filter(ml_apps_id=app_id, user_id=user_id, create_date__gte = date_from, create_date__lte = date_to) or []
    if not results:
        msg = 'No audit trail records match your search.'
    val_dict = {
        'app_set': user_apps,
        'user_id': filter_user_id,
        'msg': msg,
        'date_from': date_from_input,
        'date_to': date_to_input,
        'adt_recs': results,
        'active_app': app_id,
        'msg': msg,
        }
    return render(request, 'polls/audit_trail.html', val_dict)  
    
#**************************************KENDO UI GRID CONTROLLERS********************************************************
from django.http import HttpResponse
from django.shortcuts import render_to_response
import json
def results_grid_pop(request):
    results = []
    for record in WOStatus.objects.all().filter(is_dashboard=1,active=1):
        results.append({'wo_number':record.wo_number,'status':record.status,
        'time_status':record.time_status,'due_date_var':record.due_date_var,'rank':record.rank,
        'part_number':record.part_number,'description':record.description,'serial_number':record.serial_number,
        'manager':record.manager,'wo_type':record.wo_type,'location_code':record.location_code,
        'time_loc':record.time_loc,'cust_ref_number':record.cust_ref_number})
    data = json.dumps(results)
    return HttpResponse(data)
    #was a parameter passed into HttpResponse:, mimetype='application/javascript'
#from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.views import generic
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import serializers, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

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
        session_id = self.request.GET['session_id'] 
        user_id = self.request.GET['user_id']
        is_wos = self.request.GET['is_wos'] or False        
        records = is_wos != '0' and session_id and WOStatus.objects.all().filter(session_id=session_id,active=1).order_by('id')
        if is_wos == '0':
            records = PILogs.objects.all().filter(user_id=user_id,session_id=session_id,active=1).order_by('id')                   
        field,direction = '',''
        if 'sort[0][dir]' in self.request.GET:
            try:
                direction = self.request.GET['sort[0][dir]']
                field = self.request.GET['sort[0][field]']
            except:
                pass    
            if direction == 'asc':
                records = records.order_by(field)
            elif direction == 'desc':
                records = records.order_by('-'+field)
            else:
                return records
        return records

"""
Methods for PI_UPDATE:
"""
def contains_zero(num):
    for n in num:
        if n == '0':
            return True 
            break            
    return False
    
def get_control(barcode,delim_str):
    ctrl_number = barcode.partition(delim_str)
    ctrl_id = ctrl_number and ctrl_number[2] or None
    ctrl_number = ctrl_number and ctrl_number[0] or None 
    return ctrl_number,ctrl_id
    
def pi_update(request,quapi_id=None):
    val_dict = {}
    user_id,location_sel,msg,show_modal,error,session_id = '','','',False,'',''
    locations = []
    batch_no,control_no,control_id,quantity = None,None,None,None 
    quapi_id = is_integer(quapi_id) or 0
    dj_user_id = quapi_id and QueryApi.objects.all().filter(id=quapi_id) or None
    dj_user_id = dj_user_id and dj_user_id[0] and dj_user_id[0].dj_user_id or None
    if not dj_user_id:
        error = 'Access denied.'
        val_dict['error'] = error
        return render(request, 'polls/pi_results.html', val_dict)           
    user = request.user
    reg_user_id = user and user.is_authenticated and user.id or None
    if not dj_user_id or (dj_user_id and dj_user_id != reg_user_id):
        error = 'Access denied.'
        val_dict['error'] = error
        return render(request, 'polls/pi_results.html', val_dict)      
    from polls.tasks import run_updates,get_users_nsync
    if request.method == 'GET':
        res = get_users_nsync.delay(is_dashboard=0,quapi_id=quapi_id)
        user_error = res.get()             
    if request.method == 'POST':
        total_rows = 'total_rows' in request.POST and request.POST['total_rows'] or 0
        sel_rows = 'sel_rows' in request.POST and request.POST['sel_rows'] or 0    
        batch = 'batch_no' in request.POST and request.POST['batch_no'] or ''
        scan = 'stock_label' in request.POST and request.POST['stock_label'] or ''
        new_qty = 'quantity' in request.POST and request.POST['quantity'] or '' 
        user_id = 'user_id' in request.POST and request.POST['user_id'] or ''
        #get the user_auto_key from this text
        total_rows = 'total_rows' in request.POST and request.POST['total_rows'] or 0
        session_id = 'session_id' in request.POST and request.POST['session_id'] or ''
        if not session_id:
            session_id = 'csrfmiddlewaretoken' in request.POST and request.POST['csrfmiddlewaretoken'] or ''
        all_woos = PILogs.objects.all().filter(active=1,session_id=session_id,user_id=user_id)
        #import pdb;pdb.set_trace()
        user_rec = QuantumUser.objects.filter(user_id=user_id)
        user_auto_key = user_rec and user_rec[0] and user_rec[0].user_auto_key or None
        location_input = 'location_input' in request.POST and request.POST['location_input']  or ''       
        show_modal = 'show_modal' in request.POST and request.POST['show_modal'] or None
        #if user submitted clear list form by pressing button
        clear = 'clear_form' in request.POST and request.POST['clear_form'] or None
        ctrl_number,ctrl_id = get_control(scan,'000000')
        if not ctrl_id:
            ctrl_number,ctrl_id = get_control(scan,'00000')
        val_dict = {
            'batch_no': batch,#PI_NUMBER from PI_HEADER
            'stock_label': scan,#STOCK LABEL INPUT FROM BARCODE SCAN
            'quantity': new_qty,
            'user_id': user_id,
            'user_in': user_id,
            'all_woos': all_woos,
            'location_input': location_input,
            'msg': msg,
            'show_modal': show_modal,
            'batch': batch,
            'scan': scan,
            'new_qty': new_qty,
            'control_id': ctrl_id,
            'control_number': ctrl_number,
            'ctrl_id': ctrl_id,
            'ctrl_number': ctrl_number, 
            'total_rows': str(len(all_woos)),
            'session_id': session_id,            
        }
        if user_id and not user_id.isalnum():
            msg+="Employee code must be alpha-numeric."
        if new_qty and not new_qty.isnumeric():
            msg+="Quantity must be a number."
        if scan and not scan.isnumeric():
            msg+="Stock label must be a number.  "
        if batch and not batch.isalnum():
            msg+="Batch must be alpha-numeric."
        if not clear and not (ctrl_id and ctrl_number):
            msg += 'Stock line does not exist.'
        if msg:
            val_dict.update({'msg': msg})
            return render(request, 'polls/pi_results.html', val_dict)
        if 'woos_to_clear[]' in request.POST and clear:
            woos_to_remove = request.POST.getlist('woos_to_clear[]')                        
            if isinstance(woos_to_remove, list):               
                PILogs.objects.all().filter(pk__in=woos_to_remove).delete()
            return render(request, 'polls/pi_results.html', val_dict)         
        if not (user_auto_key or clear):
            msg += 'Invalid employee number.'
            val_dict.update({'msg':msg})
            return render(request,'polls/pi_results.html', val_dict)        
        if not (batch and scan and new_qty and user_id):
            val_dict.update({'msg':'You must have valid data in all fields to update stock.'})
            return render(request, 'polls/pi_results.html', val_dict)
        if location_input and show_modal and show_modal == 'True':  
            from polls.tasks import make_pi_updates        
            res = make_pi_updates.delay(session_id,batch,ctrl_id,ctrl_number,new_qty,scan,user_id,user_auto_key,loc_input=location_input,quapi_id=quapi_id)               
            msg = res.get()
            val_dict.update({'msg': msg,'ctrl_id': ctrl_id,'ctrl_number': ctrl_number,'show_modal':'False'})                      
        elif batch and ctrl_id and ctrl_number and new_qty:
            from polls.tasks import make_pi_updates
            #msg = make_updates(cr,con_orcl,batch_no,ctrl_id,ctrl_number,quantity,stock_label,user_id,user_rec.user_auto_key)   
            res = make_pi_updates.delay(session_id,batch,ctrl_id,ctrl_number,new_qty,scan,user_id,user_auto_key,quapi_id=quapi_id) 
            msg = res.get()                
            if msg == 'show_modal':
                val_dict.update({'msg': 'Please enter location to create the inventory update.','show_modal':'True'})
            else:
                val_dict.update({'msg': msg,'show_modal':'False'}) 
    all_woos = PILogs.objects.all().filter(active=1,user_id=user_id,session_id=session_id)
    val_dict['total_rows'] = len(all_woos) 
    val_dict['all_woos'] = all_woos    
    return render(request, 'polls/pi_results.html', val_dict)
    
def is_integer(string):
    res = string
    try:
        res = int(string)
    except Exception as exc:
        logger.exception('Not authenticated due to invalid character in load view query string - Not an integer: %r', exc)
    return res        