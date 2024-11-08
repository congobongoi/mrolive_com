#!/usr/bin/env python3
# -*- coding: utf8 -*-
# encoding=utf8
from portal.forms import WODashboardForm,PIUpdateForm
from polls.models import MoTemplate,PILogs,WOStatus,QueryApi,StatusSelection,QuantumUser,AppModes,AuditTrail,MLApps,UserAppPerms,UserQuapiRel,UserProfile
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
from django.contrib.auth import logout
from django.core.exceptions import ValidationError

def full_clean(obj_to_clean):
    error = ''
    try:
        obj_to_clean.full_clean()
    except ValidationError as e:
        # Do something based on the errors contained in e.message_dict.
        # Display them to a user, or handle them programmatically.
        pass
        error = e
    return error

def logout_view(request):
    logout(request)
    import pdb;pdb.set_trace()
    # Redirect to a success page.
    val_dict={}
    return redirect('http://mrolive.com/')
    
def account_route(request):
    #get current user's SQLite db id
    app_sel,quapi_sel,app_selected,quapi_selected,red='','','','',''
    req_post = None
    quapis = QueryApi.objects.all()
    apps = MLApps.objects.all()
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
    profile = user and UserProfile.objects.filter(user=user) or None
    logo_url = profile and profile[0] and profile[0].logo and profile[0].logo.url or None
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
        'logo_url': logo_url,
        }
    if app_sel and user_id and req_post:
        app_view = app_sel and '/portal/' + str(app_sel.code) + '/' + str(quapi_selected) or None
        #url = app_view and quapi_id and request.build_absolute_uri(reverse(app_view, args=(quapi_id, ))) or None
        #app_view = app_sel and '/portal/' + str(app_sel.code) or None
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
    val_dict,form = {},{}
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
    if not reg_user_id or not dj_user_id or (dj_user_id and dj_user_id != reg_user_id):
        val_dict['error'] = 'Access denied.'
        return redirect('/login/')
    profile = user and UserProfile.objects.filter(user=user) or None
    logo_url = profile and profile[0] and profile[0].logo and profile[0].logo.url or None
    val_dict['logo_url'] = logo_url
    user_apps = reg_user_id and UserAppPerms.objects.all().filter(dj_user_id = reg_user_id) or None
    val_dict['user_apps'] = user_apps
    val_dict['quapi_id'] = quapi_id        
    from portal.tasks import run_updates,get_statuses_nsync
    if request.method == 'GET':
        res = get_statuses_nsync.delay(is_dashboard=1,quapi_id=quapi_id,)
        stat_error = res.get()  
        form = WODashboardForm()        
    val_dict['status_vals'] = dj_user_id and stat_sel.objects.all().filter(is_dashboard=1,dj_user_id=dj_user_id).distinct() or [] 
    if request.method == 'POST':
        req_post = request.POST
        form = WODashboardForm(req_post)
        if form.is_valid(): 
            exact_match = 'exact_match' in req_post and req_post['exact_match'] or ''
            if exact_match:
                exact_match = 'checked'
            customer = 'customer' in req_post and req_post['customer'] or ''
            wo_number = 'wo_number' in req_post and req_post['wo_number'] or ''
            new_status = 'new_status' in req_post and req_post['new_status'] or ''
            due_date = 'get_due_date' in req_post and req_post['get_due_date'] or ''
            new_due_date = 'due_date' in req_post and req_post['due_date'] or '' 
            search_mgr = 'get_manager' in req_post and req_post['get_manager'] or ''
            manager = 'manager' in req_post and req_post['manager'] or ''
            warehouse = 'warehouse' in req_post and req_post['warehouse'] or ''
            location = 'location' in req_post and req_post['location'] or ''
            rank = 'rank' in req_post and req_post['rank'] or ''
            user_id = 'user_id' in req_post and req_post['user_id'] or ''
            filter_status = 'filter_status' in req_post and req_post['filter_status'] or ''
            filter_due_date = 'filter_due_date' in req_post and req_post['filter_due_date'] or ''
            filter_customer = 'filter_customer' in req_post and req_post['filter_customer'] or ''
            filter_number = 'filter_number' in req_post and req_post['filter_number'] or ''
            filter_manager = 'filter_manager' in req_post and req_post['filter_manager'] or ''
            filter_session = 'filter_session' in req_post and req_post['filter_session'] or ''
            update_session = 'update_session' in req_post and req_post['update_session'] or ''
            session_id = 'csrfmiddlewaretoken' in req_post and req_post['csrfmiddlewaretoken'] or ''
            total_rows = 'total_rows' in req_post and req_post['total_rows'] or 0
            sel_rows = 'sel_rows' in req_post and req_post['sel_rows'] or 0         
            val_dict.update({
                'all_woos': updated_woos, 
                'msg': msg,
                'new_status': new_status and int(new_status), 
                'customer': customer,
                'get_due_date': due_date,
                'new_due_date': new_due_date,
                'user_id': user_id or '',
                'manager': manager,
                'get_manager': search_mgr,
                'rank': rank,
                'wo_number': wo_number,
                'filter_status': filter_status and int(filter_status) or new_status and int(new_status),
                'filter_customer': filter_customer or customer,
                'filter_number': filter_number or wo_number,
                'filter_due_date': filter_due_date or due_date,
                'filter_manager': filter_manager or search_mgr,
                'filter_session': filter_session or session_id,#even when the update form is submitted, filter session always takes
                'update_session': update_session or session_id,
                'session_id': session_id,
                'sel_rows': sel_rows,
                'total_rows': total_rows,
                'warehouse': warehouse,
                'location': location,
                'exact_match': exact_match,
            })
            from portal.tasks import add_wo_record
            res = add_wo_record.delay(quapi_id=quapi_id,user_id='',customer=customer,status=new_status,manager=search_mgr,due_date=due_date,warehouse=warehouse,location=location,wo_number=wo_number,session_id=session_id,exact_match=exact_match) 
            error,msg = res.get()  
            if error == 'no errors':
                error = ''        
            updated_woos = WOStatus.objects.all().filter(active=1, is_dashboard=1, session_id=session_id)
            val_dict['all_woos'] = updated_woos
        else:
            error = 'Invalid key or characters entered.'        
    val_dict['msg'] = msg
    val_dict['error'] = error
    val_dict['total_rows'] = str(len(updated_woos))
    val_dict['form'] = form
    return render(request, 'mrolive/wodashboards.html', val_dict)     
    
def management(request,quapi_id=None):
    new_status,location,filter_status,error = '','','',''
    user_id,user_rec,keep_recs = 'user not set',None,False
    wo_number = ''
    val_dict,form = {},{}
    all_woos = WOStatus.objects.all().filter(active=1, is_dashboard=1, session_id='') 
    updated_woos = all_woos 
    woos_updated = False    
    msg,loc_msg,stat_msg = '','',''
    from polls.models import StatusSelection as stat_sel,QuantumUser as quser, QueryApi
    dj_user_id = quapi_id and QueryApi.objects.all().filter(id=quapi_id) or None
    dj_user_id = dj_user_id and dj_user_id[0] and dj_user_id[0].dj_user_id or None
    user = request.user
    reg_user_id = user and user.is_authenticated and user.id or None
    if not reg_user_id or not dj_user_id or (dj_user_id and dj_user_id != reg_user_id):
        val_dict['error'] = 'Access denied.'
        return redirect('/login/')  
    profile = user and UserProfile.objects.filter(user=user) or None
    logo_url = profile and profile[0] and profile[0].logo and profile[0].logo.url or None
    val_dict['logo_url'] = logo_url
    user_apps = reg_user_id and UserAppPerms.objects.all().filter(dj_user_id = reg_user_id) or None
    val_dict['user_apps'] = user_apps
    val_dict['quapi_id'] = quapi_id
    from portal.tasks import run_updates,get_statuses_nsync,get_users_nsync
    if request.method == 'GET':
        res = get_statuses_nsync.delay(is_dashboard=1,quapi_id=quapi_id)
        stat_error = res.get() 
        res = get_users_nsync.delay(is_dashboard=1,quapi_id=quapi_id)
        user_error = res.get()   
        val_dict['sel_rows'] = 0
        form = WODashboardForm()        
    val_dict['emp_vals'] = dj_user_id and quser.objects.all().filter(dj_user_id=dj_user_id).distinct() or [] 
    val_dict['status_vals'] = dj_user_id and stat_sel.objects.all().filter(is_dashboard=1,dj_user_id=dj_user_id).distinct()
    woos_updated = False
    if request.method == 'POST':
        req_post = request.POST
        form = WODashboardForm(req_post)
        if form.is_valid(): 
            #import pdb;pdb.set_trace() 
            exact_match = 'exact_match' in req_post and req_post['exact_match'] or ''
            if exact_match == '1':
                exact_match = 'checked'
            is_bom_sched = 'bom_sched_val' in req_post and req_post['bom_sched_val'] or '' 
            if not is_bom_sched and is_bom_sched != '0':
                is_bom_sched = 'is_bom_sched' in req_post and req_post['is_bom_sched'] or ''            
            active_user = 'active_user' in req_post and req_post['active_user'] or ''
            customer = 'customer' in req_post and req_post['customer'] or ''
            wo_number = 'wo_number' in req_post and req_post['wo_number'] or ''
            new_status = 'new_status' in req_post and req_post['new_status'] or ''
            active_due_date = 'active_due_date' in req_post and req_post['active_due_date'] or ''
            get_due_date = 'get_due_date' in req_post and req_post['get_due_date'] or ''
            due_date = 'due_date' in req_post and req_post['due_date'] or '' 
            search_mgr = 'get_manager' in req_post and req_post['get_manager'] or ''
            manager = 'manager' in req_post and req_post['manager'] or ''
            warehouse = 'warehouse' in req_post and req_post['warehouse'] or ''
            location = 'location' in req_post and req_post['location'] or ''
            rank = 'rank' in req_post and req_post['rank'] or ''
            update_user = 'update_user' in req_post and req_post['update_user'] or ''
            user_id = 'user_id' in req_post and req_post['user_id'] or ''
            user_name = 'user_name' in req_post and req_post['user_name'] or ''
            #lookup user_id in the database to make sure we can authenticate
            user_rec = QuantumUser.objects.all().filter(user_id__iexact=user_id)
            if not user_rec: 
                if update_user:
                    user_rec = QuantumUser.objects.all().filter(user_id__iexact=update_user) 
                else:
                    user_rec = QuantumUser.objects.all().filter(user_id__iexact=active_user)                
            user_rec = user_rec and user_rec[0] or None
            show_all = 'show_all' in req_post and req_post['show_all'] or (user_name and 1) or None
            total_rows = 'total_rows' in req_post and req_post['total_rows'] or 0
            sel_rows = 'sel_rows' in req_post and req_post['sel_rows'] or 0
            #update hidden fields
            filter_status = 'filter_status' in req_post and req_post['filter_status'] or ''
            filter_due_date = 'filter_due_date' in req_post and req_post['filter_due_date'] or ''
            filter_customer = 'filter_customer' in req_post and req_post['filter_customer'] or ''
            filter_number = 'filter_number' in req_post and req_post['filter_number'] or ''
            filter_manager = 'filter_manager' in req_post and req_post['filter_manager'] or ''
            filter_location = 'filter_location' in req_post and req_post['filter_location'] or ''
            filter_warehouse = 'filter_warehouse' in req_post and req_post['filter_warehouse'] or ''
            filter_session = 'filter_session' in req_post and req_post['filter_session'] or ''
            update_session = 'update_session' in req_post and req_post['update_session'] or ''
            session_id = 'session_id' in req_post and req_post['session_id'] or ''
            import pdb;pdb.set_trace()
            if not session_id and not filter_session:
                session_id = 'csrfmiddlewaretoken' in req_post and req_post['csrfmiddlewaretoken'] or ''
                filter_session = session_id
            if not session_id and filter_session:
                session_id = filter_session           
            dash_update = 'dash_update' in req_post and req_post['dash_update'] or None    
            user_name = user_rec and user_rec.user_name or ''      
            val_dict.update({
                'all_woos': updated_woos, 
                'msg': msg,
                'new_status':new_status and int(new_status) or filter_status and int(filter_status), 
                'customer': customer or filter_customer,
                'get_due_date': get_due_date or filter_due_date,
                'due_date': due_date or filter_due_date,
                'user_id': user_id or active_user or update_user,
                'manager': manager,
                'location': location,
                'warehouse': warehouse,
                'get_manager': search_mgr or filter_manager,
                'rank': rank,
                'wo_number': wo_number or filter_number,
                'filter_status': filter_status and int(filter_status) or new_status and int(new_status),
                'filter_customer': filter_customer or customer,
                'filter_number': filter_number or wo_number,
                'filter_due_date': filter_due_date or get_due_date,
                'filter_manager': filter_manager or search_mgr,
                'filter_location': filter_location or location,
                'filter_warehouse': filter_warehouse or warehouse,
                'filter_session': filter_session or session_id,#even when the update form is submitted, filter session always takes
                'update_session': update_session or session_id,
                'update_user': update_user or user_id or active_user,
                'session_id': session_id,
                'sel_rows': sel_rows,
                'total_rows': total_rows,
                'user_name': user_name,
                'active_user': active_user or user_id,
                'show_all': show_all or len(user_name) or active_user,
                'is_bom_sched': is_bom_sched, 
                'exact_match': exact_match,
            })
            form = WODashboardForm(val_dict)
            val_dict['form'] = form
            if 'user_id' in req_post and not user_id:
                msg += 'You must enter your Employee ID before updating any WO\'s.'
                val_dict['error'] = msg
                return render(request, 'mrolive/womgmt.html', val_dict)
            if user_id and not user_rec:
                msg += 'Invalid employee number.  Please enter a valid one.'
                val_dict['error'] = msg
                return render(request, 'mrolive/womgmt.html', val_dict)
            woo_id_list = []
            if 'woos_list[]' in req_post:
                woo_id_list = req_post.getlist('woos_list[]')   
            #import pdb;pdb.set_trace()                 
            if is_bom_sched and is_bom_sched != '0':
                from portal.tasks import bom_schedule
                res = bom_schedule.delay(woo_id_list,quapi_id,user_id,filter_session or update_session,) 
                error,msg = res.get()                  
            elif user_id and (rank or due_date or manager):
                #now, set the user on the active woos for the dashboard / csrfmiddlewaretoken
                #woos_update = WOStatus.objects.all().filter(active=1, is_dashboard=1, user_id = '', session_id = filter_session)
                #foos = WOStatus.objects.all().filter(active=1, is_dashboard=1, session_id = (filter_session or update_session))
                update_the_woos = WOStatus.objects.all().filter(active=1, is_dashboard=1, session_id = (filter_session or update_session)).update(user_id=user_id,reg_user_id = user_rec)                                 
                try:                
                    from portal.tasks import make_updates
                    res = make_updates.delay(
                        user_id=user_id, 
                        rank=rank,
                        manager=manager,
                        due_date=get_due_date,
                        new_due_date=due_date or active_due_date,
                        customer=filter_customer,
                        status=new_status,
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
            elif not user_id:
                if dash_update:
                    keep_recs = True
                from portal.tasks import add_wo_record
                res = add_wo_record.delay(keep_recs=keep_recs,customer=customer,status=new_status,manager=search_mgr,location=location,warehouse=warehouse,due_date=get_due_date,wo_number=wo_number,session_id=session_id,quapi_id=quapi_id,exact_match=exact_match) 
                error,msg = res.get()             
                val_dict['sel_rows'] = 0 
            updated_woos = WOStatus.objects.all().filter(active=1, is_dashboard=1, session_id=session_id)
            if not updated_woos:
                updated_woos = WOStatus.objects.all().filter(active=1, is_dashboard=1, session_id=filter_session)        
            val_dict['all_woos'] = updated_woos 
        else:
            error = 'Invalid key or characters entered.'                
    val_dict['msg'] = msg
    val_dict['total_rows'] = str(len(updated_woos))
    val_dict['error'] = error
    val_dict['msg'] = msg
    val_dict['form'] = form
    return render(request, 'mrolive/womgmt.html', val_dict)
    
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

def barcarting(request,quapi_id=None): 
    location,user_id,user_logged,update,warehouse,rack,new_rack,rerack,rack_user = '','','','','','','','',''
    wo_number = ''
    val_dict,form,updated_woos,all_woos,woo_num_list,woo_key_list = {},{},[],[],[],[]           
    msg,loc_msg,stat_msg,error,lookup_recs,clear_cart = '','','','',False,False
    modes = get_modes()
    val_dict['modes'] = modes
    from polls.models import StatusSelection as stat_sel,QuantumUser as quser, QueryApi
    quapi = quapi_id and QueryApi.objects.all().filter(id=quapi_id) or None
    dj_user_id = quapi and quapi[0] and quapi[0].dj_user_id or None
    user = request.user
    reg_user_id = user and user.is_authenticated and user.id or None
    if not reg_user_id or not dj_user_id or (dj_user_id and dj_user_id != reg_user_id):
        val_dict['error'] = 'Access denied.'
        return redirect('/login/') 
    profile = user and UserProfile.objects.filter(user=user) or None
    logo_url = profile and profile[0] and profile[0].logo and profile[0].logo.url or None      
    val_dict['logo_url'] = logo_url    
    user_apps = reg_user_id and UserAppPerms.objects.all().filter(dj_user_id = reg_user_id) or None
    val_dict['user_apps'] = user_apps
    val_dict['quapi_id'] = quapi_id        
    from portal.tasks import run_updates,get_statuses_nsync,get_users_nsync
    if request.method == 'GET':
        form = WODashboardForm()   
        res = get_statuses_nsync.delay(is_dashboard=0,quapi_id=quapi_id)
        stat_error = res.get() 
        res = get_users_nsync.delay(is_dashboard=0,quapi_id=quapi_id)
        user_error = res.get()         
    val_dict['emp_vals'] = dj_user_id and quser.objects.all().filter(dj_user_id=dj_user_id).distinct() or [] 
    val_dict['status_vals'] = dj_user_id and stat_sel.objects.all().filter(is_dashboard=0,dj_user_id=dj_user_id).distinct() 
    if request.method == 'POST':
        req_post = request.POST
        form = WODashboardForm(req_post) 
        if form.is_valid():
            cleaned_data = form.cleaned_data 
        total_rows = 'total_rows' in req_post and req_post['total_rows'] or 0
        sel_rows = 'sel_rows' in req_post and req_post['sel_rows'] or 0
        session_id = 'session_id' in req_post and req_post['session_id'] or ''
        if not session_id:
            session_id = 'csrfmiddlewaretoken' in req_post and req_post['csrfmiddlewaretoken'] or ''
        user_id = 'user_id' in req_post and req_post['user_id'] or ''#sysur_auto_key
        user_logged = 'user_logged' in req_post and req_post['user_logged'] or ''
        rack_user = 'rack_user' in req_post and req_post['rack_user'] or '' 
        user_id = user_id or user_logged or rack_user or ''
        user_name = 'user_name' in req_post and req_post['user_name'] or ''
        #lookup user_id in the database to make sure we can authenticate
        user_rec = QuantumUser.objects.all().filter(user_id__iexact=user_id)
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
        cart_code = 'cart_code' in req_post and req_post['cart_code'] or ''         
        new_status = 'new_status' in req_post and req_post['new_status'] or ''     
        show_status = 'show_status' in req_post and req_post['show_status'] or ''
        show_user = 'show_user' in req_post and req_post['show_user'] or ''
        show_all = 'show_all' in req_post and req_post['show_all'] or ''
        clear_cart = 'ccart_form' in req_post and True or False
        stock_label = 'stock_label' in req_post and req_post['stock_label'] or ''
        do_status = sel_mode and (sel_mode == '2' or sel_mode == '1') or False
        do_user = sel_mode or False  
        do_all = user_id or user_logged or rack_user or False       
        val_dict.update({
            'all_woos': updated_woos,
            'msg': msg,
            'warehouse': warehouse,
            'location': location,
            'user_id': user_rec and user_rec.user_id or user_logged or rack_user,
            'user_name': user_name or (user_rec and user_rec.user_name) or '',
            'rack': rack or new_rack,
            'user_logged': user_logged or user_id,
            'rack_user': user_id,
            'new_rack': rack,
            'modes': modes,
            'active_mode': active_mode or sel_mode or '',
            'sel_mode': sel_mode or active_mode or '',
            'cart_code': cart_code or rack or '',
            'stock_label': stock_label or wo_number or '',
            'new_status': new_status and int(new_status) or None,
            'lookup_recs': lookup_recs,
            'show_status': show_status or do_status,
            'do_status': do_status or show_status,
            'show_user': show_user or do_user,
            'do_user': do_status or show_status,
            'show_all': show_all and show_all!='0' or do_all,
            'do_all': do_all or show_all,
            'session_id': session_id,
            'sel_rows': sel_rows,
            'total_rows': total_rows,
            'form': form,
            })             
        if show_user and not user_rec and clear_form != '1':
            error += 'Invalid employee number.  Please enter a valid one.'
            val_dict['error'] = error
            return render(request, 'mrolive/barcoding.html', val_dict)
        if clear_cart:
            rack = rack or cart_code or ''        
        #if user submitted clear list form by pressing button
        if clear_form and req_post['clear_form']=='1':       
            WOStatus.objects.all().filter(user_id=user_logged,is_dashboard=0,active=1,is_racking=1).delete()
            val_dict['all_woos'] = []            
            val_dict['msg'] = '' 
            val_dict['active_mode'] = sel_mode  
            val_dict['username'] = ''
            val_dict['show_all'] = 0            
            return render(request, 'mrolive/barcoding.html', val_dict) 
        wo_number = wo_number or stock_label or ''            
        ctrl_number,ctrl_id = get_control(wo_number,'000000')
        if not ctrl_id:
            ctrl_number,ctrl_id = get_control(wo_number,'00000')
        sysur_auto_key = user_rec and user_rec.user_auto_key or ''
        all_woos = WOStatus.objects.all().filter(active=1,is_dashboard=0,is_racking=1,user_id=user_id)  
        keys = set(woo.woo_auto_key for woo in all_woos)
        woo_key_list = list(keys)         
        if user_id and (clear_cart or rack or cart_code or location or warehouse or wo_number):
            from portal.tasks import run_racking
            res = run_racking.delay(
                session_id,
                rack = rack or cart_code,
                location=location,
                wo_number=wo_number or stock_label,
                warehouse=warehouse,
                new_status=new_status,
                user_id=user_id,
                sysur_auto_key=sysur_auto_key,
                woo_key_list=woo_key_list,
                ctrl_id = ctrl_id,
                ctrl_number = ctrl_number,
                stock_label = wo_number or stock_label,
                mode = active_mode or sel_mode,
                lookup_recs = lookup_recs,
                quapi_id = quapi_id,
                clear_cart = clear_cart,
            )
            error,msg = res.get()
        updated_woos = WOStatus.objects.all().filter(active=1,session_id=session_id,is_dashboard=0,user_id=user_id,is_racking=1)
        val_dict['all_woos'] = updated_woos
        val_dict['total_rows'] = str(len(updated_woos))
        val_dict['msg'] = msg   
        val_dict['error'] = error        
        if not wo_number and lookup_recs not in [1,'1']:
            val_dict['lookup_recs'] = 1
        elif wo_number and lookup_recs not in [0,'0']:
            val_dict['lookup_recs'] = 0         
    return render(request, 'mrolive/barcoding.html', val_dict)
    
#++++++++++++===================Audit Trail Code============================++++++++++++++++++
def audit_trail(request,quapi_id=None):
    from polls.models import AuditTrail as Adt
    filter_user_id,active_app,msg,error,user_name,show_grid = '','','','','',False
    val_dict,results,req_post,form = {},[],{},{}
    right_now = datetime.now()
    date_to_input = right_now  + timedelta(days=1)
    date_to_input = date_to_input.strftime('%m/%d/%Y')
    date_from_input = right_now - timedelta(days=45)
    date_from_input = date_from_input.strftime('%m/%d/%Y')
    from polls.models import QueryApi
    quapi = quapi_id and QueryApi.objects.all().filter(id=quapi_id) or None
    dj_user_id = quapi and quapi[0] and quapi[0].dj_user_id or None
    user = request.user
    reg_user_id = user and user.is_authenticated and user.id or None
    user_apps = UserAppPerms.objects.filter(dj_user_id = reg_user_id)
    audit_apps = UserAppPerms.objects.filter(dj_user_id = reg_user_id,audit_ok = True)
    profile = user and UserProfile.objects.filter(user=user) or None
    logo_url = profile and profile[0] and profile[0].logo and profile[0].logo.url or None
    if not dj_user_id or (dj_user_id and dj_user_id != reg_user_id):
        error += 'Access denied.'
        val_dict['error'] = error
        return redirect('/login/')
    if request.method == 'POST':
        req_post = request.POST
        form = WODashboardForm(req_post)
        format = '%Y-%m-%d %H:%M:%S'
        new_format = '%m/%d/%Y'
        total_rows = 'total_rows' in req_post and req_post['total_rows'] or 0
        filter_user_id = 'user_id' in req_post and req_post['user_id'] or None
        date_from_input = 'date_from' in req_post and req_post['date_from'] or None
        date_from = date_from_input and datetime.strptime(date_from_input, new_format) or None
        date_from = date_from and datetime.strftime(date_from, format) or None
        date_to_input = 'date_to' in req_post and req_post['date_to'] or None
        date_to = date_to_input and datetime.strptime(date_to_input, new_format) or None
        date_to = date_to and datetime.strftime(date_to, format) or None
        active_app = 'app_selector' in req_post and req_post['app_selector'] or None
        user_id = filter_user_id and QuantumUser.objects.all().filter(user_id__iexact=filter_user_id) or None
        user_id = user_id and user_id[0] or None
        user_name = user_id and user_id.user_name or ''
        show_grid = user_name and True or None
        if not user_id:
            error = 'Invalid user.'        
    else:
        form = WODashboardForm(initial={'date_from': date_from_input, 'date_to': date_to_input})    
    app_id = active_app and UserAppPerms.objects.filter(id=active_app) or None
    app_id = app_id and app_id[0] and app_id[0].ml_apps_id and app_id[0].ml_apps_id.id or None
    results = app_id and user_id and Adt.objects.all().filter(quapi_id = quapi and quapi[0] or None, ml_apps_id=app_id, user_id__iexact=filter_user_id, create_date__gte = date_from, create_date__lte = date_to) or []
    if not results and req_post:
        error = 'No audit trail records match your search.'
    val_dict = {
        'app_set': user_apps,
        'audit_apps': audit_apps,
        'user_name': user_name,
        'user_id': filter_user_id,
        'user': user,
        'msg': msg,
        'error': error,
        'date_from': date_from_input,
        'date_to': date_to_input,
        'active_app': active_app and int(active_app) or None,
        'msg': msg,
        'quapi_id': quapi_id,
        'logo_url': logo_url,
        'show_grid': show_grid,
        'total_rows': len(results),
        'form': form,
        }
    return render(request, 'mrolive/audit_trail.html', val_dict) 
    
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

class PIPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'pageSize'
    
class ADTSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditTrail
        fields = '__all__'

# Create your views here.
class ADTListView(generic.ListView):
    model = AuditTrail
    def get_context_data(self, **kwargs):       
        context = super(ADTListView, self).get_context_data(**kwargs)
        return context

class ADTJsonView(generics.ListAPIView):
    serializer_class = ADTSerializer
    pagination_class = PIPageNumberPagination
    
    def get_queryset(self, *args, **kwargs):
        format = '%Y-%m-%d %H:%M:%S'
        new_format = '%m/%d/%Y'
        date_from_input = self.request.GET['date_from']
        date_to_input = self.request.GET['date_to']  
        date_from = date_from_input and datetime.strptime(date_from_input, new_format) or None
        date_from = date_from and datetime.strftime(date_from, format) or None
        date_to = date_to_input and datetime.strptime(date_to_input, new_format) or None
        date_to = date_to and datetime.strftime(date_to, format) or None        
        app_id = self.request.GET['app_id']
        app_id = app_id and UserAppPerms.objects.filter(id=app_id) or None
        ml_apps_id = app_id and app_id[0] and app_id[0].ml_apps_id or None
        quapi_id = self.request.GET['quapi_id']
        quapi = quapi_id and QueryApi.objects.filter(id=quapi_id) or None
        user_id = self.request.GET['user_id']
        records = quapi_id and AuditTrail.objects.filter(ml_apps_id=ml_apps_id,user_id__iexact=user_id,quapi_id = quapi and quapi[0] or None,create_date__gte = date_from,create_date__lte = date_to).order_by('-id')                   
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

class PISerializer(serializers.ModelSerializer):
    class Meta:
        model = PILogs
        fields = '__all__'

# Create your views here.
class PIListView(generic.ListView):
    model = WOStatus
    def get_context_data(self, **kwargs):       
        context = super(PIListView, self).get_context_data(**kwargs)
        return context

class PIJsonView(generics.ListAPIView):
    serializer_class = PISerializer
    pagination_class = PIPageNumberPagination
    
    def get_queryset(self, *args, **kwargs):
        session_id = self.request.GET['session_id'] 
        user_id = self.request.GET['user_id']
        records = PILogs.objects.all().filter(user_id=user_id,session_id=session_id,active=1).order_by('-id')                   
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
        if not user_id:
            records = is_wos != '0' and session_id and WOStatus.objects.all().filter(user_id=user_id,session_id=session_id,active=1).order_by('-id')  
        else:
            records = is_wos != '0' and session_id and WOStatus.objects.all().filter(session_id=session_id,active=1).order_by('-id')                  
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
    val_dict,form = {},{}
    user_id,location_sel,msg,show_modal,error,session_id,user_error = '','','',False,'','',''
    locations,user_rec = [],[]
    batch_no,control_no,control_id,quantity = None,None,None,None 
    dj_user_id = quapi_id and QueryApi.objects.all().filter(id=quapi_id) or None
    dj_user_id = dj_user_id and dj_user_id[0] and dj_user_id[0].dj_user_id or None          
    user = request.user
    reg_user_id = user and user.is_authenticated and user.id or None
    if not reg_user_id or not dj_user_id or (dj_user_id and dj_user_id != reg_user_id):
        val_dict['error'] = 'Access denied.'
        return redirect('/login/') 
    profile = user and UserProfile.objects.filter(user=user) or None
    logo_url = profile and profile[0] and profile[0].logo and profile[0].logo.url or None
    val_dict['logo_url'] = logo_url
    user_apps = reg_user_id and UserAppPerms.objects.all().filter(dj_user_id = reg_user_id) or None
    val_dict['user_apps'] = user_apps
    val_dict['quapi_id'] = quapi_id        
    from portal.tasks import run_updates,get_users_nsync
    if request.method == 'GET':
        res = get_users_nsync.delay(is_dashboard=0,quapi_id=quapi_id)
        user_error = res.get()  
        form = PIUpdateForm()         
    if request.method == 'POST':
        req_post = request.POST
        form = PIUpdateForm(req_post)
        sel_rows = 'sel_rows' in req_post and req_post['sel_rows'] or 0    
        batch = 'batch_no' in req_post and req_post['batch_no'] or ''
        scan = 'stock_label' in req_post and req_post['stock_label'] or ''
        new_qty = 'quantity' in req_post and req_post['quantity'] or '' 
        user_id = 'user_id' in req_post and req_post['user_id'] or ''
        user_val = 'user_val' in req_post and req_post['user_val'] or ''
        user_name = 'user_name' in req_post and req_post['user_name'] or ''
        #get the user_auto_key from this text
        total_rows = 'total_rows' in req_post and req_post['total_rows'] or 0
        session_id = 'session_id' in req_post and req_post['session_id'] or ''
        if not session_id:
            session_id = 'csrfmiddlewaretoken' in req_post and req_post['csrfmiddlewaretoken'] or ''
        user_rec = QuantumUser.objects.filter(user_id__iexact=user_id)
        user_rec = user_rec and user_rec[0] or None
        user_name = user_rec and user_rec.user_name or ''
        user_auto_key = user_rec and user_rec.user_auto_key or None
        all_woos = user_rec and PILogs.objects.all().filter(active=1,session_id=session_id,user_id=user_rec.user_id) or []
        location_input = 'location_input' in req_post and req_post['location_input']  or ''       
        show_modal = 'show_modal' in req_post and req_post['show_modal'] or None
        show_all = 'show_all' in req_post and req_post['show_all'] or (user_name and 1) or None
        #if user submitted clear list form by pressing button
        clear = 'clear_form' in req_post and req_post['clear_form'] or None
        ctrl_number,ctrl_id = get_control(scan,'000000')
        if not ctrl_id:
            ctrl_number,ctrl_id = get_control(scan,'00000')
        val_dict.update({
            'batch_no': batch,#PI_NUMBER from PI_HEADER
            'stock_label': scan,#STOCK LABEL INPUT FROM BARCODE SCAN
            'quantity': new_qty,
            'user_id': user_rec and user_rec.user_id or '',
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
            'show_all': show_all or len(user_name),
            'user_name': user_name or (user_rec and user_rec.user_name) or '',
            'session_id': session_id, 
            'form': form,            
        })
        if user_id and not user_id.isalnum():
            error+="Employee code must be alpha-numeric."
        if new_qty and not new_qty.isnumeric():
            error+="Quantity must be a number."
        if scan and not scan.isnumeric():
            error+="Stock label must be a number.  "
        if batch and not batch.isalnum():
            error+="Batch must be alpha-numeric."
        #if not clear and not (ctrl_id and ctrl_number):
        #    msg += 'Stock line does not exist.'
        if error:
            val_dict.update({'error': error})
            return render(request, 'mrolive/pi_results.html', val_dict)
        if 'woos_to_clear[]' in req_post and clear:
            woos_to_remove = req_post.getlist('woos_to_clear[]')                        
            if isinstance(woos_to_remove, list):               
                PILogs.objects.all().filter(pk__in=woos_to_remove).delete()
            return render(request, 'mrolive/pi_results.html', val_dict)         
        if not (user_auto_key or clear):
            error += 'Invalid employee number.'
            val_dict.update({'error':error})
            return render(request,'mrolive/pi_results.html', val_dict)        
        if location_input and show_modal and show_modal == 'True':  
            from portal.tasks import make_pi_updates        
            res = make_pi_updates.delay(session_id,batch,ctrl_id,ctrl_number,new_qty,scan,user_rec.user_id,user_auto_key,loc_input=location_input,quapi_id=quapi_id)               
            error = res.get()
            val_dict.update({'error': error,'msg': msg,'ctrl_id': ctrl_id,'ctrl_number': ctrl_number,'show_modal':'False'})                      
        elif batch and scan and new_qty:
            from portal.tasks import make_pi_updates
            #msg = make_updates(cr,con_orcl,batch_no,ctrl_id,ctrl_number,quantity,stock_label,user_id,user_rec.user_auto_key)   
            res = make_pi_updates.delay(session_id,batch,ctrl_id,ctrl_number,new_qty,scan,user_rec.user_id,user_auto_key,quapi_id=quapi_id) 
            error = res.get()                
            if error == 'show_modal':
                val_dict.update({'msg': 'Please enter location to create the inventory update.','show_modal':'True'})
            else:
                val_dict.update({'error': error,'show_modal':'False'}) 
    all_woos = user_rec and PILogs.objects.all().filter(active=1,user_id=user_rec.user_id,session_id=session_id) or []
    val_dict['total_rows'] = len(all_woos) 
    val_dict['all_woos'] = all_woos  
    val_dict['error'] = error != 'show_modal' and error + user_error 
    val_dict['msg'] = msg
    val_dict['form'] = form
    return render(request, 'mrolive/pi_results.html', val_dict)
    
def is_integer(string):
    res = string
    try:
        res = string and int(string) or None
    except Exception as exc:
        logger.exception('Not authenticated due to invalid character in load view query string - Not an integer: %r', exc)
    return res        