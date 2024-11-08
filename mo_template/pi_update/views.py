#!/usr/bin/env python
# -*- coding: utf8 -*-
# encoding=utf8
from django.shortcuts import render
from django.http import Http404
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import os
import re
import sys
import logging
logger = logging.getLogger(__name__)
from datetime import datetime
from dateutil.parser import parse
from operator import itemgetter

"""
Methods for sending and executing queries:
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

def authenticate_user(cr,user_id):
    #user_check = get_one_user(cr,user_id)
    user_rec = QuantumUser.objects.all().filter(user_id = user_id)
    user_rec = user_rec and user_rec[0] or None
    #lookup user_id in the database to make sure we can authenticate
    if not user_rec:
        user_rec = get_one_user(cr,user_id)
        user_rec = user_rec and user_rec[0] and create_user(user_rec[0])
    return user_rec
    
def pi_update(request,quapi_id=None):
    from polls.models import QuantumUser as quser,QueryApi,PILogs
    val_dict = {}
    user_id,location_sel,msg,show_modal = '','','',False
    all_woos = PILogs.objects.all().filter(active=1)
    locations = []
    batch_no,control_no,control_id,quantity = None,None,None,None 
    dj_user_id = quapi_id and QueryApi.objects.all().filter(id=quapi_id) or None
    dj_user_id = dj_user_id and dj_user_id[0] and dj_user_id[0].dj_user_id or None
    user = request.user
    reg_user_id = user and user.is_authenticated and user.id or None
    if not dj_user_id or (dj_user_id and dj_user_id != reg_user_id):
        error += 'Access denied.'
        val_dict['error'] = error
        return render(request, 'polls/pi_results.html', val_dict)      
    from polls.tasks import run_updates,get_statuses_nsync,get_users_nsync
    if request.method == 'GET':
        res = get_statuses_nsync.delay(is_dashboard=0,quapi_id=quapi_id)
        stat_error = res.get() 
        res = get_users_nsync.delay(is_dashboard=0,quapi_id=quapi_id)
        user_error = res.get()             
    val_dict['emp_vals'] = dj_user_id and quser.objects.all().filter(dj_user_id=dj_user_id).distinct() or []      
    if request.method == 'POST':
        #import pdb;pdb.set_trace()
        batch = 'batch_no' in request.POST and request.POST['batch_no'] or ''
        scan = 'stock_label' in request.POST and request.POST['stock_label'] or ''
        new_qty = 'quantity' in request.POST and request.POST['quantity'] or '' 
        user_id = 'user_id' in request.POST and request.POST['user_id'] or ''
        location_input = 'location_input' in request.POST and request.POST['location_input']  or ''       
        show_modal = 'show_modal' in request.POST and request.POST['show_modal'] or None
        #if user submitted clear list form by pressing button
        clear = 'clear_form' in request.POST and request.POST['clear_form'] or None
        #import pdb;pdb.set_trace()
        ctrl_number,ctrl_id = get_control(scan,'000000')
        if not ctrl_id:
            ctrl_number,ctrl_id = get_control(scan,'00000')
        val_dict = {
            'batch_no': batch,#PI_NUMBER from PI_HEADER
            'stock_label': scan,#STOCK LABEL INPUT FROM BARCODE SCAN
            'quantity': new_qty,
            'user_id': user_id,
            'user_in': user_id,
            'all_woos': PILogs.objects.all().filter(active=1,user_id=user_id),
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
        user = user_id and authenticate_user(cr,user_id) or None
        if not (user or clear):
            msg += 'Invalid employee number.'
            val_dict.update({'msg':msg})
            return render(request,'polls/pi_results.html', val_dict)
        if isinstance(user,list):
            user_auto_key = user and user[0] and user[0].user_auto_key or None 
        else:
            user_auto_key = user.user_auto_key or None          
        if not (batch and scan and new_qty and user_id):
            val_dict.update({'msg':'You must have valid data in all fields to update stock.'})
            return render(request, 'polls/pi_results.html', val_dict)
        if location_input and show_modal and show_modal == 'True':               
            query = "SELECT LOC_AUTO_KEY FROM LOCATION WHERE LOCATION_CODE='%s'"%location_input
            loc_auto_key = query_fetchall(query,cr=cr)
            loc_auto_key = loc_auto_key and loc_auto_key[0] and loc_auto_key[0][0] or None
            if not loc_auto_key:
                val_dict.update({'msg':'That location doesn\'t exist. Please try again.','show_modal':'True'})
                return render(request, 'polls/pi_results.html', val_dict)                  
            else:                   
                from polls.tasks import make_pi_updates
                res = make_pi_updates.delay(batch,ctrl_id,ctrl_number,new_qty,scan,user_id,user_auto_key,location_key=loc_auto_key,loc_input=location_input)               
                msg = res.get()
                val_dict.update({'msg': msg,'ctrl_id': ctrl_id,'ctrl_number': ctrl_number,'show_modal':'False'})
                return render(request, 'polls/pi_results.html', val_dict)                       
        elif batch and ctrl_id and ctrl_number and new_qty:
            from polls.tasks import make_pi_updates
            #msg = make_updates(cr,con_orcl,batch_no,ctrl_id,ctrl_number,quantity,stock_label,user_id,user_rec.user_auto_key)   
            res = make_pi_updates.delay(batch,ctrl_id,ctrl_number,new_qty,scan,user_id,user_auto_key) 
            msg = res.get()                
            if msg == 'show_modal':
                val_dict.update({'msg': 'Please enter location to create the inventory update.','show_modal':'True'})
            else:
                val_dict.update({'msg': msg,'show_modal':'False'})             
    return render(request, 'polls/pi_results.html', val_dict)
    
def verify_loc_input(locations,loc_auto_key,cr=None):
    res = loc_auto_key in (item for loc_list in locations for item in loc_list) 
    return res