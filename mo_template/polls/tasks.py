#!/usr/bin/env python3
import requests
import importlib
import os
os.environ[ 'DJANGO_SETTINGS_MODULE' ] = "mo_template.settings"
from celery import Celery,task
from datetime import datetime
import sys
sys.path.append(os.getcwd())
import logging
logger = logging.getLogger(__name__)
celery = Celery('tasks', broker='redis://localhost:6379/0', backend="rpc://")
celery.conf.update(accept_content = ['json','pickle'],accept_results = ['json','pickle'],broker_heartbeat = 15,acks_late=True)
"""
To Do's: obtain the results from the task methods
"""
#METHODS
def update_stock_audit(sysur_auto_key,sta_auto_key,employee_code,user_id=''):
    query = """"
        begin
        qc_trig_pkg.disable_triggers;
        update SA_LOG set SYSUR_AUTO_KEY = %s, EMPLOYEE_CODE = '%s' where STA_AUTO_KEY = %s;
        qc_trig_pkg.enable_triggers;
        end;"""%(sysur_auto_key,sta_auto_key,employee_code)
    msg = updation(query,user_id=user_id,quapi=quapi) 
    return msg
    
def update_trail(sysur_auto_key, woo_auto_key, new_status=None, new_location=None, stm_auto_key=None, quapi=None, user_id = None, new_mgr=None, new_due_date=None, new_rank=None):
    #parameters: user_id - integer ID for PK to the SYS_USERS table
    #            woo_auto_key - Quantum db primary key for user input WO#
    #            new_status - user input status to which to update
    #            new_location - user input location (converted to database id for loc_auto_key in STM table)
    msg = ''
    q1,q2 = '',''
    if not sysur_auto_key:
        return 'No user is logged in and therefore no update can be made to the audit trail table.'
    if new_rank:
        query = """
            UPDATE AUDIT_TRAIL SET SYSUR_AUTO_KEY=%s WHERE SOURCE_TABLE = 'WOO' AND SOURCE_AK = %s AND SOURCE_FIELD = 'RANK'
            AND NEW_VALUE = %s"""%(sysur_auto_key, woo_auto_key, new_rank)
        msg = updation(query,user_id=user_id,quapi=quapi)   
    if new_due_date:
        query = """
            UPDATE AUDIT_TRAIL SET SYSUR_AUTO_KEY=%s WHERE SOURCE_TABLE = 'WOO' AND SOURCE_AK = %s AND SOURCE_FIELD = 'DUE_DATE'
            AND NEW_VALUE = TO_DATE('%s', 'mm-dd-yyyy')"""%(sysur_auto_key, woo_auto_key, new_due_date)
        msg = updation(query,user_id=user_id,quapi=quapi)           
    if new_status:
        query = """
            UPDATE AUDIT_TRAIL SET SYSUR_AUTO_KEY=%s WHERE SOURCE_TABLE = 'WOO' AND SOURCE_AK = %s AND SOURCE_FIELD = 'STATUS'
            AND NEW_VALUE = (SELECT DESCRIPTION FROM WO_STATUS WHERE WOS_AUTO_KEY = '%s')"""%(sysur_auto_key, woo_auto_key, new_status)
        msg = updation(query,user_id=user_id,quapi=quapi)  
    return str(msg)
    
def check_if_same_status(wos_auto_key, woo_auto_key, user_id='', quapi=None):
    """
    Arguments: status - wos_auto_key supplied by user form input
            wo_number - SI_NUMBER supplied by user form input
            
    Returns: query results from function call to selection()     
    """
    update_ok = False
    query = """
        SELECT WOS_AUTO_KEY,SI_NUMBER FROM WO_OPERATION
            WHERE
            WOO_AUTO_KEY = %s"""%woo_auto_key
    results = selection(query, user_id=user_id,quapi=quapi)    
    if results and results[0] and results[0][0] != wos_auto_key:
        wos_auto_key = results[0][0]
        update_ok = True           
    return update_ok
    
def check_if_same_loc(location_code, woo_auto_key, user_id='',quapi=None):
    """
    Arguments: location - code supplied by user form input
            woo_auto_key - from a lookup of SI_NUMBER (wo_number) supplied by user form input           
    Returns: results from location       
    """
    update_ok = False
    stm_auto_key = ''
    #location code is what they enter/scan => from location - lookup location table to find location code
    query = """SELECT S.STM_AUTO_KEY, L.LOC_AUTO_KEY, L.LOCATION_CODE FROM WO_OPERATION W, WO_STATUS WS,STOCK_RESERVATIONS SR, STOCK S, LOCATION L WHERE W.WOS_AUTO_KEY = WS.WOS_AUTO_KEY AND W.WOO_AUTO_KEY = SR.WOO_AUTO_KEY AND SR.STM_AUTO_KEY = S.STM_AUTO_KEY AND S.LOC_AUTO_KEY = L.LOC_AUTO_KEY AND W.WOO_AUTO_KEY = %s"""%(woo_auto_key)
    results = selection(query, user_id=user_id,quapi=quapi)
    if not results:
        query = """SELECT S.STM_AUTO_KEY, L.LOC_AUTO_KEY, L.LOCATION_CODE FROM WO_OPERATION W, STOCK_RESERVATIONS SR, STOCK S, LOCATION L WHERE W.WOS_AUTO_KEY IS NULL AND W.WOO_AUTO_KEY = SR.WOO_AUTO_KEY AND SR.STM_AUTO_KEY = S.STM_AUTO_KEY AND S.LOC_AUTO_KEY = L.LOC_AUTO_KEY AND W.WOO_AUTO_KEY = %s"""%(woo_auto_key)
        results = selection(query, user_id=user_id,quapi=quapi)        
    result = results and results[0] or None
    stm_auto_key = result and result[0] or None
    if type(stm_auto_key) is list:
        stm_auto_key = stm_auto_key[0]
    if result and result[2] and result[2] != location_code:
        update_ok = True           
    return stm_auto_key,update_ok
    
def set_status(woo_auto_key, new_status_key, user_id='', quapi=None):
    recs = []
    error = ''
    timestamp = ''
    update_status = woo_auto_key and new_status_key and check_if_same_status(new_status_key, woo_auto_key,user_id=user_id,quapi=quapi) or False 
    if user_id and update_status and woo_auto_key:
        query = "UPDATE WO_OPERATION SET WOS_AUTO_KEY = %s WHERE WOO_AUTO_KEY = %s"%(new_status_key,woo_auto_key)
        error = updation(query, user_id=user_id,quapi=quapi)
    return str(error) 
    
def synch_record(wos_obj, user_id,woo_auto_key=None,wo_number='',new_status = None,new_location = None,update_stamp=None,quapi=None):
    if not user_id:
        msg = 'You must enter an employee ID first before updating any workorder statuses.'
        return msg 
    from polls.models import StatusSelection       
    msg = ''
    wos_status = '' 
    wos = wos_obj.objects.filter(is_racking=0, woo_auto_key=woo_auto_key, active=1, is_dashboard=0, user_id=user_id)
    right_now = datetime.now()
    right_now = right_now.strftime('%Y-%m-%d %H:%M:%S')       
    if new_status:
        stat_sel = StatusSelection.objects.filter(wos_auto_key=new_status)
        wos_status = stat_sel and stat_sel[0] and stat_sel[0].name or '-- No Status --'
        if woo_auto_key and wos:   
            wos.update(status = wos_status, update_stamp = update_stamp)           
    #if user didn't select a status and entered a WO that doesn't already
    #exist or didn't enter one at all, we create the WO locally.
    if not update_stamp: update_stamp = None
    if woo_auto_key and not wos:        
        recs = get_wo_status(woo_auto_key, user_id=user_id,quapi=quapi) 
        if recs:
            woo = recs[0]
            #due_date = woo[2] and woo[2].strftime('%Y-%m-%d') or None
            due_date = woo[2] and len(woo[2]) > 10 and woo[2][:10] or None
            status = str(woo[8]) + ' - ' + str(woo[1])
            try:
                wos = wos_obj.objects.create(
                    wo_number = wo_number,
                    supdate_msg = 'successful update',
                    status = status,
                    due_date = due_date,
                    stock_line = woo[3],
                    part_number = woo[4],
                    description = woo[5],
                    serial_number = woo[6],
                    location_code = new_location or woo[7],
                    active = 1,
                    update_stamp = update_stamp,
                    user_id = user_id,
                    is_dashboard = 0,
                    woo_auto_key=woo_auto_key,
                )
                wos.save() 
            except Exception as error:
                logger.error("Error with creation of wo locally. Message: '%s'",error.args)
        else:
            msg = "The WO you entered, '%s', doesn't exist."%wo_number
    #if user entered both WO and status to update to and wos exists locally already:
    elif wos and new_status: 
        wos.update(status = wos_status or '-- no status --', update_stamp = update_stamp)        
    elif wos and woo_auto_key and not (new_status or new_location):
        msg = 'We have this WO in the list already.  You must do one of the following:  a. enter a valid WO# and a\
        status or b. select one or more WO\'s to remove or c. enter only a status to update all workorders on this list.'
    return msg
  
def update_loc(location_code, loc_auto_key, woo_auto_key, user_id, wos_obj,quapi=None):
    msg = ''
    stm_auto_key,update_ok = check_if_same_loc(location_code, woo_auto_key, user_id=user_id,quapi=quapi) 
    if update_ok and stm_auto_key and loc_auto_key: 
        #build the query that updates 'STOCK' with the new 
        #LOC_AUTO_KEY obtained by the output from the 
        #check_if_same_loc() call.    
        query = "UPDATE STOCK SET LOC_AUTO_KEY = %s WHERE STM_AUTO_KEY = %s"%(loc_auto_key,stm_auto_key)      
        msg = updation(query, user_id=user_id,quapi=quapi)
    woo_object = wos_obj.objects.filter(woo_auto_key=woo_auto_key, is_dashboard=0, is_racking=0, active=1, user_id=user_id)
    woo_object = woo_object and woo_object.update(location_code=location_code)           
    return msg
    
def get_woo_key(wo_number, user_id='',quapi=None):
    woo_auto_key = None
    query = "SELECT WOO_AUTO_KEY FROM WO_OPERATION WHERE SI_NUMBER = '%s' ORDER BY WOO_AUTO_KEY DESC"%wo_number
    woo_auto_key = selection(query, user_id=user_id, quapi=quapi)
    woo_auto_key = woo_auto_key and woo_auto_key[0] and woo_auto_key[0][0] or None
    return woo_auto_key

@task 
def get_users_nsync(quapi_id=None,user_id=None,is_dashboard=0):
    msg = ''
    error = ''
    query = "SELECT SYSUR_AUTO_KEY,USER_NAME,PASS_KEY,EMPLOYEE_CODE,USER_ID FROM SYS_USERS WHERE ARCHIVED='F'"
    from polls.models import QuantumUser,QueryApi
    quapi = QueryApi.objects.filter(id=quapi_id)
    recs = quapi and quapi[0] and selection(query,user_id='none',quapi=quapi[0]) or []
    dj_user_id = quapi and quapi[0] and quapi[0].dj_user_id or None
    del_users = dj_user_id and QuantumUser.objects.filter(dj_user_id=dj_user_id).delete() or None
    #import pdb;pdb.set_trace()
    for user in recs:
        try:
            user_auto_key = str(user[0])
            user_name = str(user[1])
            pass_key = str(user[2])
            code = str(user[3])
            user_id = str(user[4])
            s = QuantumUser.objects.create(user_id=user_id,dj_user_id=dj_user_id,user_auto_key=user_auto_key,employee_code=code,pass_key=pass_key,user_name=user_name)
            s.save()
        except Exception as error:
            error = "\r\Django - Error with creating the user: %s"%error 
    return msg
    
@task 
def get_statuses_nsync(quapi_id=None,user_id=None,is_dashboard=0):
    #TODO: must get the user that is currently logged in down in selection/insert/update methods 
    #user links us to the API creds we need to send an API request to run a query.
    #display WO Status Table in dropdown displaying WO_STATUS[‘DESCRIPTION’] 
    # and WO_STATUS[‘SEVERITY’], but only show Open WO_STATUS[‘STATUS_TYPE’])
    error = ''
    from polls.models import StatusSelection as statsel,QueryApi
    quapi = QueryApi.objects.filter(id=quapi_id)
    query = "SELECT WOS_AUTO_KEY, SEVERITY, DESCRIPTION FROM WO_STATUS WHERE STATUS_TYPE IN ('Open','Delay','Defer') ORDER BY SEVERITY ASC"
    recs = quapi and quapi[0] and selection(query,user_id='none',quapi=quapi[0]) or []
    dj_user_id = quapi and quapi[0] and quapi[0].dj_user_id or None
    del_stats = dj_user_id and statsel.objects.filter(is_dashboard=is_dashboard,dj_user_id=dj_user_id).delete() or None
    if is_dashboard ==1 :
        wos_auto_key = 0
        severity = '0'
        name = ' - PENDING'
        try:
            sstat = statsel.objects.create(dj_user_id = dj_user_id,is_dashboard = 1,wos_auto_key = wos_auto_key, severity = severity, name = name)
            sstat.save()
        except Exception as error:
            error = "\r\nDjango - Error with creating the pending status: %s"%error 
    for status in recs:
        try:
            wos_auto_key = status[0]
            severity = status[1]
            name = str(status[1]) + ' - ' + str(status[2])
            s = statsel.objects.create(dj_user_id = dj_user_id,is_dashboard=is_dashboard, wos_auto_key = wos_auto_key, severity = severity, name = name)
            s.save()
        except Exception as error:
            error = "\r\Django - Error with creating the status: %s"%error 
    return error
    
@task
def run_updates(quapi_id=None,location='',wo_number='',new_status='',user_id='',sysur_auto_key=None, woo_key_list=[]):    
    msg,error,loc,synch,stat,trail,audit_ok,field_changed,new_val = '','','','','','',True,'',''
    from polls.models import WOStatus as wos_obj,QueryApi
    quapi = QueryApi.objects.filter(id=quapi_id)
    quapi = quapi and quapi[0] or None
    #get woo_auto_key from query and then pass it to all of these queries instead of SI_NUMBER as the key.
    woo_auto_key = wo_number and get_woo_key(wo_number, user_id=user_id, quapi=quapi) or None 
    if wo_number and not woo_auto_key:
        return 'WO#: ' + wo_number + ' does not exist in your Quantum database.',msg
    if location:
        #check here to see if valid location in Quantum
        query = "SELECT loc_auto_key FROM location WHERE location_code = '%s'"%location
        res = quapi and selection(query=query, user_id=user_id, quapi=quapi) or None
        if not res:
            return "Location does not exist.",msg     
        loc_auto_key = res and res[0] and res[0][0] or None          
        if wo_number:
            loc = update_loc(
                location, 
                loc_auto_key, 
                woo_auto_key, 
                user_id, 
                wos_obj,
                quapi=quapi, 
                )            
        elif woo_key_list:
            for wak in woo_key_list:
                loc = update_loc( 
                    location, 
                    loc_auto_key, 
                    wak, 
                    user_id, 
                    wos_obj,
                    quapi=quapi, 
                )    
    if wo_number and new_status:        
        stati = set_status(woo_auto_key, new_status, user_id=user_id, quapi=quapi)              
        timestamp = get_stamptime(woo_auto_key, new_status, user_id=user_id,quapi=quapi)  
        timestamp = timestamp and timestamp[0] or None
        if type(timestamp) is list:
            timestamp = timestamp[0]
        if type(timestamp) is datetime:
            timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        trail = update_trail(sysur_auto_key, woo_auto_key, new_status=new_status, user_id=user_id,quapi=quapi) 
        synch = synch_record(wos_obj,user_id,quapi=quapi,wo_number=wo_number,woo_auto_key=woo_auto_key,new_status=new_status, new_location=location, update_stamp=timestamp)    
    if wo_number and not new_status:
        synch = synch_record(wos_obj, user_id, wo_number=wo_number, woo_auto_key=woo_auto_key, new_location=location,quapi=quapi)        
    if not wo_number and new_status and woo_key_list: 
        synchi,stati,traili = '','',''
        count = 0
        for woo in woo_key_list:
            stati = set_status(woo, new_status, user_id=user_id,quapi=quapi)                 
            timestamp = get_stamptime(woo_key_list[count], new_status,quapi=quapi) 
            timestamp = timestamp and timestamp[0] or None
            if type(timestamp) is list:
                timestamp = timestamp[0]
            if type(timestamp) is datetime:
                timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            #get the update stamp back and pass it in synch_record
            synchi = synch_record(               
                wos_obj,
                user_id, 
                wo_number=woo, 
                woo_auto_key=woo_key_list[count],
                new_status=new_status, 
                new_location=location, 
                update_stamp=timestamp,
                quapi=quapi,
                )
            traili = update_trail(
                sysur_auto_key,
                woo_key_list[count],
                new_status=new_status, 
                user_id=user_id,                
                quapi=quapi
                )  
            count += 1                
        stat += stati
        synch += synchi
        trail += traili
    if location:
        field_changed += 'Location: '
        new_val += 'Location: %s, '%location
    if new_status:
        field_changed += 'Status: '
        from polls.models import StatusSelection as statsel
        status = statsel.objects.filter(wos_auto_key=new_status)
        new_status = status and status[0] and status[0].name or None
        new_val += new_status and 'Status: %s'%new_status or ''        
    error += str(stat) + str(trail) + str(synch) + str(loc) + str(orcl_commit(user_id=user_id,quapi=quapi))
    if field_changed and user_id:        
        from polls.models import MLApps as maps,QuantumUser as qu
        app_id = maps.objects.filter(code='barcoding')       
        user_rec = qu.objects.filter(user_id=user_id)
        user_rec = user_rec and user_rec[0] or None
        new_val += ' for WO Number(s) with ids: ' + str(woo_key_list)
        right_now = datetime.now()
        now = right_now.strftime('%Y-%m-%d %H:%M:%S')
        error += register_audit_trail(user_rec,field_changed,new_val,now,app_id)   
    return str(error),str(msg)
    
@task
def make_updates(quapi_id=None,user_id=None,rank=None,manager=None,new_due_date=None,customer=None,status=None,search_mgr=None,due_date=None,wo_number=None,session_id=None,woo_id_list=[]):   
    from dateutil.parser import parse
    woo_recs,woo_ids = None,None
    from polls.models import WOStatus as wos_obj,QueryApi
    quapi = QueryApi.objects.filter(id=quapi_id)
    quapi = quapi and quapi[0] or None
    if not woo_id_list:
        woo_recs = wos_obj.objects.filter(active=1, is_dashboard=1, user_id=user_id, session_id=session_id)
    else:
        woo_id_list = [int(i) for i in woo_id_list]
        woo_recs = wos_obj.objects.filter(pk__in=woo_id_list)
    woo_ids = woo_recs.values_list('woo_auto_key',flat=True)           
    pdue_date,sysur_auto_key,audit_ok,ins_error = None,None,False,''
    error,msg,values_str,field_changed = '','','',''
    #woo_id_list = []    
    if not woo_ids:
        return 'There are no active WOs to update.',msg 
    else:
        woo_id_list = '(' + str(woo_ids[0])
        woo_adt_list = '(' + str(woo_ids[0])
        count = 1
        for wak in woo_ids[1:]:
            woo_id_list += ',' + str(wak)
            woo_adt_list += ',' + str(wak)
            if (count+1)%995 == 0 and woo_ids[count+1]:
                woo_id_list += ') OR WOO_AUTO_KEY IN (' + str(woo_ids[count+1])
                woo_adt_list += ') OR SOURCE_AK IN (' + str(woo_ids[count+1])
            count += 1    
        woo_id_list += ')'           
        woo_adt_list += ')'
        if rank:
            try:        
                int(rank)  
            except Exception as error:
                error += "\r\nError with rank entry.  Only non-negative, natural numbers are allowed." 
                return error,msg
            field_changed += 'rank'
            values_str += "RANK = '%s'"%rank   
        if manager:      
            query = "SELECT SYSUR_AUTO_KEY FROM SYS_USERS WHERE USER_ID = '%s'"%manager
            user_mgr = quapi and selection(query, user_id=user_id, quapi=quapi) or None 
            if not user_mgr:
                error += "\r\nYou have entered a manager that doesn't exist: '%s'"%manager
                return error,msg
            sysur_auto_key = user_mgr and user_mgr[0] and user_mgr[0][0] or None 
            prefix = ''
            if rank:
                prefix = ', '
            field_changed += prefix + 'manager'
            values_str += prefix + 'SYSUR_MANAGER = %s'%sysur_auto_key           
        if new_due_date:      
            try:        
                pdue_date = parse(new_due_date)  
                new_due_date = "TO_DATE('%s', 'mm-dd-yyyy')"%new_due_date  
            except Exception as error:
                error += "\r\nError with due date entry: %s"%error 
                return error,msg            
            dd_update = False
            prefix = ''
            if rank or manager:
                prefix = ', '  
            field_changed += prefix + 'due date'                
            values_str += prefix + 'DUE_DATE = %s'%new_due_date
    where_clause = " WHERE WOO_AUTO_KEY IN %s"%woo_id_list        
    upd_query = "UPDATE WO_OPERATION SET %s"%values_str + where_clause       
    error = updation(upd_query, user_id=user_id,quapi=quapi) 
    ins_error,msg = add_wo_record(
                user_id=user_id,
                customer=customer,
                status=status,
                wo_number=wo_number,
                due_date=due_date,
                manager=search_mgr,
                new_manager=manager,
                new_rank=rank,
                new_due_date=due_date,
                refresh=True,
                session_id=session_id,
                wak_clause=woo_adt_list,
                woo_recs=woo_recs,
                quapi=quapi,
                )
    update_error = update_audit_trail(user_id,woo_adt_list=woo_adt_list,new_rank=rank,new_due_date=new_due_date,new_mgr=sysur_auto_key) 
    commit_error = orcl_commit(user_id=user_id,quapi=quapi) 
    if field_changed:
        from polls.models import MLApps as maps,QuantumUser as qu
        app_id = maps.objects.filter(code='management') 
        user_rec = qu.objects.filter(user_id=user_id)
        user_rec = user_rec and user_rec[0] or None
        new_val = values_str
        field_changed = values_str + ' | wo number(s):= ' + woo_adt_list
        right_now = datetime.now()
        now = right_now.strftime('%Y-%m-%d %H:%M:%S')
        if user_rec:
            error = register_audit_trail(user_rec,field_changed,new_val,now,app_id)
    return str(error) + str(ins_error),str(msg)
    
def update_audit_trail(user_id, woo_adt_list = '', new_status=None, new_location=None, stm_auto_key=None, new_mgr=None, new_due_date=None, new_rank=None,quapi=None):
    #parameters: user_id - integer ID for PK to the SYS_USERS table
    #            wo_number - user input WO#
    #            new_status - user input status to which to update
    #            new_location - user input locastion (converted to database id for loc_auto_key in STM table)
    from polls.models import QuantumUser
    msg = ''
    user_rec = QuantumUser.objects.filter(user_id=user_id)
    user_key = user_rec and user_rec[0] and user_rec[0].user_auto_key or None
    q1,q2 = '',''
    if not user_key:
        return 'No user is logged in and therefore no update can be made to the audit trail table.'
    if new_rank:
        query = """UPDATE AUDIT_TRAIL SET SYSUR_AUTO_KEY=%s WHERE SOURCE_AK IN %s AND SOURCE_TABLE = 'WOO' AND SOURCE_FIELD = 'RANK' AND NEW_VALUE = %s"""%(user_key, woo_adt_list, new_rank)
        updation(query,user_id=user_id,quapi=quapi)  
    #if new_mgr:
    #    query = """
    #        UPDATE AUDIT_TRAIL SET SYSUR_AUTO_KEY=%s WHERE SOURCE_AK IN %s AND SOURCE_TABLE = 'WOO' AND SOURCE_FIELD = 'SYSUR_MANAGER' AND NEW_VALUE = (SELECT USER_ID FROM SYS_USERS WHERE SYSUR_AUTO_KEY = %s)"""%(user_key, woo_adt_list, new_mgr)
    #    updation(query,user_id=user_id,quapi=quapi)   
    if new_due_date:
        #UPDATE AUDIT_TRAIL SET SYSUR_AUTO_KEY=747 WHERE SOURCE_AK IN (1351,1696,1353,1354,1355,1356,1357,1358,1359,1360,1361,1362,1363,1364,1365,1366,1367,1368,893,2722,2723,2724,2768,1453,1454,1557,1558,1352) AND SOURCE_TABLE = 'WOO' AND SOURCE_FIELD = 'DUE_DATE' AND NEW_VALUE = TO_DATE('12-08-2019', 'mm-dd-yyyy')
        query = """UPDATE AUDIT_TRAIL SET SYSUR_AUTO_KEY=%s WHERE ADT_AUTO_KEY = (SELECT MAX(ADT_AUTO_KEY) FROM AUDIT_TRAIL WHERE SOURCE_AK IN %s AND SOURCE_TABLE = 'WOO' AND SOURCE_FIELD = 'DUE_DATE')"""%(user_key, woo_adt_list)
        updation(query,user_id=user_id,quapi=quapi)        
    if new_status:
        query = """UPDATE AUDIT_TRAIL SET SYSUR_AUTO_KEY=%s WHERE SOURCE_AK IN %s AND SOURCE_TABLE = 'WOO' AND SOURCE_FIELD = 'STATUS' AND NEW_VALUE = (SELECT DESCRIPTION FROM WO_STATUS WHERE WOS_AUTO_KEY = %s)"""%(user_key, woo_adt_list, new_status)
        updation(query,user_id=user_id,quapi=quapi) 
    return str(msg)

def get_stamptime(woo_auto_key=None, new_status=None, stm_auto_key=None, location_code = None, user_id='', quapi=None):
    res = ''
    if new_status:
        #get timestamp from audit trail for output in the results table
        q_stat = """SELECT STAMPTIME FROM AUDIT_TRAIL WHERE SOURCE_TABLE = 'WOO' AND SOURCE_AK = %s AND SOURCE_FIELD = 'STATUS' AND NEW_VALUE = (SELECT DESCRIPTION FROM WO_STATUS WHERE WOS_AUTO_KEY = '%s') ORDER BY STAMPTIME DESC"""%(woo_auto_key, new_status)
        res = quapi and selection(query=q_stat,user_id=user_id,quapi=quapi) or None
    if stm_auto_key and location_code:
        q_log = """SELECT BRI_AUTO_KEY,OLD_LOC_AUTO_KEY,NEW_LOC_AUTO_KEY,OLD_LOCATION_CODE,NEW_LOCATION_CODE,TIME_STAMP FROM SA_LOG WHERE NEW_LOCATION_CODE = '%s' AND STM_AUTO_KEY = %s ORDER BY STA_AUTO_KEY DESC NULLS LAST"""%(location_code,stm_auto_key)
        res = quapi and selection(query=q_log,user_id=user_id,quapi=quapi) or None
    return res

def get_wo_mgmt(wos_obj, wo_number=None,customer=None,status=None,manager=None,due_date=None,wak_clause=None,refresh=False,user_id='',quapi=None):
    order_by = ' ORDER BY W.DUE_DATE ASC,W.RANK ASC'
    where_clause,msg = '',''
    recs = []
    pending = False
    if wak_clause:
        where_clause += ' AND W.WOO_AUTO_KEY IN ' + wak_clause
    else:
        if manager:
            query = "SELECT SYSUR_AUTO_KEY FROM SYS_USERS WHERE REGEXP_LIKE (USER_ID, '%s', 'i')"%manager
            user_mgr = selection(query, user_id=user_id,quapi=quapi) 
            if not user_mgr:
                msg+="\r\nYou have entered a manager that doesn't exist: '%s'"%manager
                return None
            sysur_auto_key = user_mgr and user_mgr[0] and user_mgr[0][0] or None 
            where_clause += " AND W.SYSUR_MANAGER = %s"%sysur_auto_key   
        #if manager:
        #    where_clause += " AND W.SYSUR_AUTO_KEY IN (SELECT SYSUR_AUTO_KEY FROM SYS_USERS WHERE REGEXP_LIKE (USER_ID, '%s', 'i'))"%manager
        if due_date:
            where_clause += " AND W.DUE_DATE <= TO_DATE('%s', 'mm-dd-yyyy')"%due_date  
        if wo_number:
            where_in = """(SELECT WOO_AUTO_KEY FROM VIEW_SPS_WO_OPERATION WHERE PARENT_WO LIKE '%s%s%s')"""%('%',wo_number,'%')
            where_clause += " AND (W.WOO_AUTO_KEY IN %s OR W.SI_NUMBER = '%s')"%(where_in,wo_number) 
        if customer:
            where_clause += " AND W.CMP_AUTO_KEY IN (SELECT CMP_AUTO_KEY FROM COMPANIES WHERE REGEXP_LIKE (COMPANY_NAME, '%s', 'i'))"%customer  
        if status and status != '0':
            where_clause += " AND W.WOS_AUTO_KEY = %s"%int(status)
        elif status and status == '0':
            pending = True
    if pending:        
        query="""SELECT W.SI_NUMBER, W.WOS_AUTO_KEY, W.DUE_DATE, S.STOCK_LINE, P.PN, P.DESCRIPTION, 
                      S.SERIAL_NUMBER, L.LOCATION_CODE, W.WOS_AUTO_KEY,
                      W.ENTRY_DATE, W.COMPANY_REF_NUMBER, W.WOO_AUTO_KEY,W.RANK,W.WOS_AUTO_KEY,S.STM_AUTO_KEY FROM WO_OPERATION W
                      LEFT JOIN STOCK_RESERVATIONS SR ON SR.WOO_AUTO_KEY = W.WOO_AUTO_KEY
                      LEFT JOIN STOCK S ON S.STM_AUTO_KEY = SR.STM_AUTO_KEY
                      LEFT JOIN PARTS_MASTER P ON P.PNM_AUTO_KEY = S.PNM_AUTO_KEY
                      LEFT JOIN LOCATION L ON L.LOC_AUTO_KEY = S.LOC_AUTO_KEY
                      WHERE W.WOS_AUTO_KEY IS NULL"""+ where_clause + order_by
    else:
        query="""SELECT W.SI_NUMBER, WS.DESCRIPTION, W.DUE_DATE, S.STOCK_LINE, P.PN, P.DESCRIPTION,S.SERIAL_NUMBER, L.LOCATION_CODE, WS.SEVERITY,W.ENTRY_DATE, W.COMPANY_REF_NUMBER, W.WOO_AUTO_KEY,W.RANK,WS.WOS_AUTO_KEY,S.STM_AUTO_KEY FROM WO_OPERATION W LEFT JOIN STOCK_RESERVATIONS SR ON SR.WOO_AUTO_KEY = W.WOO_AUTO_KEY LEFT JOIN STOCK S ON S.STM_AUTO_KEY = SR.STM_AUTO_KEY LEFT JOIN PARTS_MASTER P ON P.PNM_AUTO_KEY = S.PNM_AUTO_KEY LEFT JOIN LOCATION L ON L.LOC_AUTO_KEY = S.LOC_AUTO_KEY LEFT JOIN WO_STATUS WS ON WS.WOS_AUTO_KEY = W.WOS_AUTO_KEY WHERE (W.WOS_AUTO_KEY IS NULL OR WS.STATUS_TYPE IN ('Open','Delay','Defer'))"""+ where_clause + order_by      
    recs = selection(query, user_id=user_id,quapi=quapi)    
    return recs
    
@task
def add_wo_record(is_dashboard=1,is_racking=0,keep_recs=False,user_id=None,quapi_id=0,quapi=None,customer=None,status=None,wo_number=None,due_date=None,manager=None,new_manager=None,new_rank=None,new_due_date=None,refresh=False,session_id=None,wak_clause=None,woo_recs=None):
    msg,error = '',''
    wos_status = ''
    from polls.models import WOStatus as wos_obj,QueryApi
    if not quapi:
        quapi = QueryApi.objects.filter(id=quapi_id)
        quapi = quapi and quapi[0] or None    
    right_now = datetime.now()    
    #if user didn't select a status and entered a WO that doesn't already
    #exist or didn't enter one at all, we create the WO locally.       
    recs,active_woos,woo_records = [],[],[]
    if not woo_recs:
        woo_recs = []
    due_date_var,timestamp,time_loc,sysur_mgr,wo_type,location = '','','','','',''
    if not status or status == 'False' and status != '0': status = ''
    #periodic or triggered refresh of active_woos    
    if refresh and wak_clause and woo_recs:
        active_woos = woo_recs 
        recs = get_wo_mgmt(wos_obj,wak_clause=wak_clause,refresh=True,user_id=user_id,quapi=quapi) 
    elif woo_recs and not refresh:
        recs = woo_recs          
    elif not (woo_recs or refresh):    
        recs = get_wo_mgmt(wos_obj,wo_number=wo_number,status=status,customer=customer,due_date=due_date,manager=manager,user_id=user_id,quapi=quapi)
        active_woos = wos_obj.objects.filter(active=1, is_dashboard=is_dashboard, session_id=session_id, is_racking=0) 
    if not active_woos:
        active_woos = wos_obj.objects.filter(active=1, user_id=user_id, is_dashboard=0, is_racking=1)        
    woos_deleted = not keep_recs and active_woos and active_woos.delete() or None       
    if not recs and not refresh:
        error += 'Your search filters returned no results.  Please adjust your filters and try again.'
        return error,msg
    if recs and recs[0] and len(recs[0]) != 0 and recs[0][0] and isinstance(recs[0][0], list):
        recs = recs[0]        
    for woo in recs:
        query = "SELECT COMPANY_NAME FROM COMPANIES WHERE CMP_AUTO_KEY = (SELECT CMP_AUTO_KEY FROM WO_OPERATION WHERE WOO_AUTO_KEY = %s)"%woo[11]
        customer = woo[11] and selection(query,user_id=user_id,quapi=quapi) or None  
        if is_dashboard == 1:
            due_date = woo[2] or None
            due_date = due_date and datetime.strptime(due_date[:10], '%Y-%m-%d') or None
            #calc diff between due_date and today's date to return due_date_var
            if due_date:
                delta = right_now - due_date
                days = delta.days
                #'Time elapsed since due date
                due_date_var = str(days) + ' days'           
            #get worktype
            query = "SELECT WORK_TYPE FROM WO_WORK_TYPE WHERE WWT_AUTO_KEY = (SELECT WWT_AUTO_KEY FROM WO_OPERATION WHERE WOO_AUTO_KEY = %s)"%woo[11]
            wo_type = selection(query, user_id=user_id, quapi=quapi)
            query = "SELECT USER_ID FROM SYS_USERS WHERE SYSUR_AUTO_KEY = (SELECT SYSUR_MANAGER FROM WO_OPERATION WHERE WOO_AUTO_KEY = %s)"%woo[11]
            sysur_mgr = selection(query, user_id=user_id, quapi=quapi) 
        status = str(woo[8]) + ' - ' + str(woo[1])    
        #due_date = woo[2] and woo[2].strftime('%Y-%m-%d') or None
        due_date = woo[2][:10] or None
        #Get time of last update to this status
        si_number = woo[0]
        woo_auto_key = woo[11]
        stm_auto_key = woo[14]
        if not woo_auto_key and stm_auto_key and is_racking:
            #str_auto_key = woo[20]
            #then get the woo from the bom
            query="""SELECT SI_NUMBER,WOO_AUTO_KEY FROM WO_OPERATION
                   WHERE WOO_AUTO_KEY IN 
                     (SELECT WOO_AUTO_KEY FROM WO_BOM WHERE WOB_AUTO_KEY IN
                       (SELECT WOB_AUTO_KEY FROM STOCK_RESERVATIONS WHERE STM_AUTO_KEY = %s))
            """%stm_auto_key
            res = selection(query, user_id=user_id, quapi=quapi)
            si_number = res and res[0] and res[0][0] or None
            woo_auto_key = res and res[0] and res[0][1] or None
            woo[11] = res and woo_auto_key or None
            woo[0] = res and si_number or None        
            if not woo_auto_key:
                query = """SELECT RO_NUMBER FROM RO_HEADER 
                    WHERE ROH_AUTO_KEY IN (SELECT ROH_AUTO_KEY FROM RO_DETAIL 
                    WHERE ROD_AUTO_KEY IN (SELECT ROD_AUTO_KEY FROM STOCK_RESERVATIONS 
                    WHERE STM_AUTO_KEY = %s))
                """%stm_auto_key
                res = selection(query, user_id=user_id, quapi=quapi)
                si_number = res and res[0] and res[0][0] or None
            status = ((si_number or woo_auto_key) and 'Reserved') or 'Available'
        if woo_auto_key:
            format = '%Y-%m-%dT%H:%M:%S'
            timestamp = get_stamptime(woo_auto_key = woo[11], new_status = woo[13],user_id=user_id,quapi=quapi)
            timestamp = timestamp and timestamp[0] or None
            if type(timestamp) is list:
                timestamp = timestamp[0]
                timestamp = datetime.strptime(timestamp,format)
                if type(timestamp) is datetime:
                    delta = timestamp and (right_now - timestamp)
                    days, hours, minutes = delta.days, delta.seconds // 3600, delta.seconds // 60 % 60
                    #'Time elapsed since last status update:+[4we
                    #timestamp =  str(days) + ' days, ' + str(hours) + ' hours, ' + str(minutes) + ' minutes, ' + str(delta.seconds % 60) + ' seconds.'
                    timestamp =  str(days) + 'D:' + str(hours) + 'H'
            #get time of last update to this location
            time_loc = get_stamptime(woo_auto_key = woo_auto_key,stm_auto_key = stm_auto_key, location_code = woo[7],user_id=user_id,quapi=quapi)
            time_loc = time_loc and time_loc[0] or None
            if type(time_loc) is list:
                time_loc = time_loc[5]
                time_loc = datetime.strptime(time_loc,format)
                if type(time_loc) is datetime:
                    delta = time_loc and (right_now - time_loc)
                    days, hours, minutes = delta.days, delta.seconds // 3600, delta.seconds // 60 % 60
                    #'Time elapsed since last status update:
                    #time_loc = str(days) + ' days, ' + str(hours) + ' hours, ' + str(minutes) + ' minutes, ' + str(delta.seconds % 60) + ' seconds.'
                    time_loc =  str(days) + 'D:' + str(hours) + 'H'
        woo_data = [
            si_number,#SI Number
            status or ' - PENDING',#status with sev and desc
            timestamp or None,
            due_date or None,
            due_date_var,
            woo[3],#stock_line
            woo[4],#part_number
            woo[5],#part_desc
            woo[6],#serial_no
            woo[7],#9loc_code
            time_loc or None,#10
            customer and customer[0] and customer[0][0] or '',#11
            woo[9][:10] or None,#12 entry_date
            woo[10],#13 company_ref
            woo_auto_key or 0,#14 woo_auto_key
            wo_type and wo_type[0] and wo_type[0][0] or '',#15
            sysur_mgr and sysur_mgr[0] and sysur_mgr[0][0] or '',#16
            woo[12],#17rank
            woo[13] or 0,#18wos_auto_key
            stm_auto_key or 0,#19stm_auto_key
            1,#20 active
            is_dashboard,#21is_dashboard
            user_id or '',#22
            session_id or '',#23
            is_racking,#24
            ]
        if is_racking:
            #WH.WAREHOUSE_CODE,UDL.UDL_CODE,S.CTRL_ID,S.CTRL_NUMBER
            woo_data = woo_data + woo[15:19]
        else:
            woo_data = woo_data + ['','',0,0]
        woo_records.append(woo_data)
    create_in_bulk(woo_records,wos_obj)
    return error,msg
    
def create_in_bulk(woo_recs, wos_obj):
    objects = []
    for wo_number,status,time_status,due_date,due_date_var,stock_line,part_number,description,serial_number,location_code,time_loc,customer,entry_date,cust_ref_number,woo_auto_key,wo_type,manager,rank,wos_auto_key,stm_auto_key,active,is_dashboard,user_id,session_id,is_racking,wh_code,rack,ctrl_id,ctrl_number in woo_recs:
        objects.append(wos_obj(
                wo_number = wo_number,#0
                status = status,#1
                time_status = time_status,#2
                due_date = due_date,#3
                due_date_var = due_date_var,#4
                stock_line = stock_line,#5
                part_number = part_number,#6
                description = description,#7
                serial_number = serial_number,#8
                location_code = location_code,#9
                time_loc = time_loc,#10
                customer = customer,#11
                entry_date = entry_date,#12
                cust_ref_number = cust_ref_number,#13
                woo_auto_key = woo_auto_key,#14
                wo_type = wo_type,#15
                manager = manager,#16
                rank = rank,#17
                wos_auto_key=wos_auto_key,#18
                stm_auto_key=stm_auto_key,#19
                active = active,#20
                is_dashboard = is_dashboard,#21
                user_id = user_id or '',#22
                session_id = session_id or '',#23 
                is_racking = is_racking,#24
                wh_code = wh_code,#25
                rack = rack,#26
                ctrl_id = ctrl_id,#27
                ctrl_number = ctrl_number#28                
        ))
    wos_obj.objects.bulk_create(objects)
    return True
    
def get_wo_status(woo_auto_key,user_id='',quapi=None):  
    #assuming nothing about stock but that status is set on WO 
    query = """
        SELECT W.SI_NUMBER, WS.DESCRIPTION, W.DUE_DATE, S.STOCK_LINE, P.PN, P.DESCRIPTION, 
          S.SERIAL_NUMBER, L.LOCATION_CODE, WS.SEVERITY FROM WO_OPERATION W
          LEFT JOIN STOCK_RESERVATIONS SR ON W.WOO_AUTO_KEY = SR.WOO_AUTO_KEY
          LEFT JOIN STOCK S ON SR.STM_AUTO_KEY = S.STM_AUTO_KEY
          LEFT JOIN PARTS_MASTER P ON S.PNM_AUTO_KEY = P.PNM_AUTO_KEY
          LEFT JOIN LOCATION L ON L.LOC_AUTO_KEY = S.LOC_AUTO_KEY
          LEFT JOIN WO_STATUS WS ON W.WOS_AUTO_KEY=WS.WOS_AUTO_KEY
        WHERE
          (W.WOS_AUTO_KEY IS NULL 
          OR WS.STATUS_TYPE IN ('Open','Delay','Defer'))
          AND W.WOO_AUTO_KEY = %s"""%woo_auto_key   
    return selection(query, user_id=user_id, quapi=quapi) 
    
#====================================================GENERAL HELPER/QUERY QUANTUM METHODS================================================  
@task()
def insertion(query,table_name,auto_key,user_id='',quapi=None):
    recs = []
    message = ''
    new_auto_key = None
    query_res = "SELECT %s FROM %s ORDER BY %s DESC"%(auto_key, table_name, auto_key)
    if query and quapi:
        #must be that it is an API call so we reroute it to the API
        url = quapi.conn_str or 'http://3.16.162.44:8065/queries/run_queries/'
        url = url and url + 'insertion' or None
        params = {
            'query': query,
            'user_id': user_id,
            'table_name': table_name,
            'auto_key': auto_key,
            'type': 'insertion',
            'schema': quapi.orcl_conn_id or 0,
        }
        response = requests.post(url,json=params,params=params)
        success = (response.status_code == 200)  # 200 = SUCCESS
        json = success and response.json() or {}
        records = json and json['recs'] or [[]]
        for row in records:
            new_auto_key = row and row[0] or None
            break
    return new_auto_key,message
    
@task()   
def selection(query,table_name='',quapi=None,user_id=None):
    #import pdb;pdb.set_trace()
    recs,res,all_res = [],[],[]
    api_key,secret= '',''
    if query and quapi:
        url = quapi.conn_str or 'http://3.16.162.44:8065/queries/run_queries/'
        url = url and url + 'selection' or None
        params = {
            'query': query,
            'user_id': user_id,
            'key': api_key,#get val from db
            'secret': secret,#get val from db
            'type': 'selection',
            'schema': quapi.orcl_conn_id or 0,
        }
        response = requests.post(url,json=params,params=params)
        success = (response.status_code == 200)  # 200 = SUCCESS
        json = success and response.json() or {}
        recs = 'recs' in json and json['recs'] or None
        if recs:       
            for count,rec in enumerate(recs):
                res = ['' if (field == None or field == 'None') else field for field in rec]
                if table_name:
                    regex = re.compile('[^0-9a-zA-Z #,.-]+')
                    res = [regex.sub(' ',field) if isinstance(field, str) else field for field in res]
                all_res.append(res)
    return all_res
        
@task
def orcl_commit(user_id='',quapi=None):
    #commit the database updates
    msg=''
    if quapi:
        #must be that it is an API call so we reroute it to the API
        #url = 'http://3.16.162.44:8065/queries/run_queries/commit'
        url = quapi.conn_str or 'http://3.16.162.44:8065/queries/run_queries/'
        url = url and url + 'commit' or None        
        params = {
            'query': '',
            'user_id': user_id,
            'type': 'commit',
            'schema': quapi.orcl_conn_id or 0,
        }
        #url = requests.utils.quote(url, params=params)
        response = requests.post(url,json=params,params=params)
        success = (response.status_code == 200)  # 200 = SUCCESS
        msg = response.status_code                
    return str(msg)
    
def updation(query,user_id='',quapi=None):   
    msg = ''
    if query and quapi:
        #must be that it is an API call so we reroute it to the API
        url = quapi.conn_str or 'http://3.16.162.44:8065/queries/run_queries/'
        url = url and url + 'update' or None
        params = {
            'query': query,
            'user_id': user_id,
            'type': 'update',
            'schema': quapi.orcl_conn_id or 0,
        }
        response = requests.post(url,params=params)
        #print(response.text)
        success = (response.status_code == 200)  # 200 = SUCCESS
        msg = success and 'no errors' or response.text
    return str(msg)
#========================================================PI UPDATES CODE================================================================================
def lookup_stm_auto_key(ctrl_id,ctrl_number,user_id='',quapi=None):
    query = "SELECT STM_AUTO_KEY,PNM_AUTO_KEY,WHS_AUTO_KEY,LOC_AUTO_KEY FROM STOCK WHERE CTRL_ID = %s AND CTRL_NUMBER = %s"%(ctrl_id,ctrl_number)
    res = selection(query, user_id=user_id, quapi=quapi)
    return res  
    
def get_locations(loc_from,loc_fto,user_id='',quapi=None): 
    loc_domain,recs = '',[]
    if int(loc_from) and int(loc_to) and loc_from <= loc_to:
        count = loc_from + 1
        loc_domain = '(' + str(loc_from)
        while loc_from < count <= loc_to:
            loc_domain += ',' + str(count)
            if (count+1)%995 == 0 and count <= loc_to -1:
                loc_domain += ') OR LOC_AUTO_KEY IN (' + str(count+1)
            count += 1
        loc_domain += ')'
        query = "SELECT LOCATION_CODE FROM LOCATION WHERE LOC_AUTO_KEY IN %s"%loc_domain
        recs = selection(query, user_id=user_id, quapi=quapi)
    return recs     
    
def lookup_batch(batch_no,stm_auto_key=None,user_id='', quapi=None):
    locations = []
    loc_from,loc_to = '','' 
    pid_auto_key,pid = None,None
    #get the pih_auto_key from pi_header for that batch
    query = "SELECT PIH_AUTO_KEY,LOC_FROM,LOC_TO FROM PI_HEADER WHERE PI_NUMBER = '%s'"%batch_no
    pi_header = selection(query, user_id=user_id,quapi=quapi) 
    pih = pi_header and pi_header[0] or None
    pih_auto_key = pih and pih[0] or None
    #get the pid_auto_key from PI_DETAIL
    if pih_auto_key and stm_auto_key:
        query = "SELECT PID_AUTO_KEY,LOC_AUTO_KEY FROM PI_DETAIL WHERE PIH_AUTO_KEY= %s AND STM_AUTO_KEY = %s"%(pih_auto_key,stm_auto_key)
        pi_detail = selection(query, user_id=user_id, quapi=quapi)
        pid = pi_detail and pi_detail[0] or None
        pid_auto_key = pid and pid[0] or None
    return pid,pid_auto_key,pih,pih_auto_key
    
def get_loc_code(loc_auto_key,user_id='',quapi=None):
    query = "SELECT LOCATION_CODE FROM LOCATION WHERE LOC_AUTO_KEY=%s"%loc_auto_key
    recs = selection(query, user_id=user_id, quapi=quapi)
    return recs

def insert_detail_record(loc_auto_key,pih_auto_key,stock_rec,user_rec_id,new_qty,ctrl_id,ctrl_number,user_id='',quapi=None):
    stm_auto_key = stock_rec and stock_rec[0] or None
    pnm_auto_key = stock_rec and stock_rec[1] or None
    whs_auto_key = stock_rec and stock_rec[2] or None
    #insert a new  PID_AUTO_KEY into PI_DETAIL with the LOC_AUTO_KEY = where that LOC_AUTO_KEY = (user input for LOCATION_CODE)
    query = """INSERT INTO PI_DETAIL (STM_AUTO_KEY,PID_AUTO_KEY,SYSUR_AUTO_KEY,QTY_FOUND,CTRL_ID,CTRL_NUMBER,PIH_AUTO_KEY,PNM_AUTO_KEY,WHS_AUTO_KEY,LOC_AUTO_KEY) VALUES ('%s',G_PID_AUTO_KEY.NEXTVAL,%s,'%s','%s','%s',%s,'%s','%s','%s')"""%(stm_auto_key or '',user_rec_id,int(new_qty),ctrl_id,ctrl_number,pih_auto_key,pnm_auto_key or '',whs_auto_key or '',loc_auto_key or '')                
    new_auto_key,msg = insertion(query,'PI_DETAIL','PID_AUTO_KEY',user_id=user_id,quapi=quapi) 
    orcl_commit(user_id=user_id,quapi=quapi)  
    return msg
    
@task
def make_pi_updates(session_id,batch_no,ctrl_id,ctrl_number,new_qty,stock_label,user_id,user_rec_id,quapi_id=None,loc_input=''):
    location_key = None
    from polls.models import PILogs,QueryApi
    quapi = quapi_id and QueryApi.objects.filter(id=quapi_id) or None
    quapi = quapi and quapi[0] or None
    if loc_input:
        query = loc_input and "SELECT LOC_AUTO_KEY FROM LOCATION WHERE LOCATION_CODE='%s'"%loc_input or None
        res = query and selection(query,quapi=quapi,user_id=user_id) or {}
        location_key = res and res[0] and res[0][0] or None
        if not location_key:
            return 'show_modal'
    msg,location_code,new_auto_key,loc_auto_key,pih_auto_key,audit_ok = '','','',None,None,False 
    stock_rec = lookup_stm_auto_key(ctrl_id=ctrl_id,ctrl_number=ctrl_number,user_id=user_id, quapi=quapi)
    if not stock_rec:
        return 'Stock line doesn\'t exist'
    stock_rec = stock_rec and stock_rec[0] or None
    stm_auto_key = stock_rec and stock_rec[0] or None
    pnm_auto_key = stock_rec and stock_rec[1] or None       
    #need to check the pnm_auto_key to see if the part is serialized
    qty = new_qty and int(new_qty) or 0
    if qty and pnm_auto_key and qty > 1 or qty < -1:
        query = "SELECT SERIALIZED FROM PARTS_MASTER WHERE PNM_AUTO_KEY=%s AND SERIALIZED='T'"%pnm_auto_key
        serialized = selection(query, user_id=user_id, quapi=quapi)
        if serialized:
            return 'Serialized parts cannot have quantity > 1'
    whs_auto_key = stock_rec and stock_rec[2] or None     
    """if not location_key:
        loc_auto_key = stock_rec and stock_rec[3] or None
    location_code = loc_auto_key and get_loc_code(loc_auto_key) or None
    location_code = location_code and location_code[0] and location_code[0][0] or None"""
    if batch_no:    
        pid,pid_auto_key,pih,pih_auto_key = lookup_batch(batch_no,stm_auto_key,user_id=user_id)
        loc_auto_key = pid and pid[1] or None
        if not loc_auto_key:
            loc_auto_key = stock_rec and stock_rec[3] or None
        location_code = loc_auto_key and get_loc_code(loc_auto_key,user_id=user_id,quapi=quapi) or None
        location_code = location_code and location_code[0] and location_code[0][0] or None
    if location_key and pih_auto_key:       
        msg = insert_detail_record(location_key,pih_auto_key,stock_rec,user_rec_id,new_qty,ctrl_id,ctrl_number,user_id=user_id,quapi=quapi) 
        #if not msg:
        audit_ok=True
        pi_log = PILogs.objects.create(
            stock_label = stock_label,
            batch_no = batch_no,
            location_code = loc_input, 
            quantity = int(new_qty),
            ctrl_number = ctrl_number,
            ctrl_id = ctrl_id,
            active = 1,
            user_id = user_id,
            session_id = session_id,
        )
        pi_log.save() 
    elif pid_auto_key:
        #update the pi_detail table with the stm_auto_key    
        where_clause = 'WHERE PID_AUTO_KEY = %s'%pid_auto_key           
        #now update QTY_FOUND in PI_DETAIL
        query = "UPDATE PI_DETAIL SET QTY_FOUND = %s, SYSUR_AUTO_KEY = %s %s"%(int(new_qty),user_rec_id,where_clause)   
        msg = updation(query,user_id=user_id,quapi=quapi) 
        #if not msg:
        audit_ok = True
        pi_log = PILogs.objects.create(
            stock_label = stock_label,
            batch_no = batch_no,
            location_code = location_code, 
            quantity = int(new_qty),
            ctrl_number = ctrl_number,
            ctrl_id = ctrl_id,
            active = 1,
            user_id = user_id,
            session_id = session_id,
        )
        pi_log.save()      
    #if not pi_detail records with that stm_auto_key, then we have to prompt the user for a location
    elif not pid_auto_key and pih:
        return 'show_modal'       
    #now we log what we have just done by creating the PILogs object with all of the data.          
    else:
        msg ='No batch exists.'
    if audit_ok:        
        from polls.models import MLApps as maps,QuantumUser as qu
        app_id = maps.objects.filter(code='inventory') 
        #app_id = app_id and app_id[0] or None
        user_rec = qu.objects.filter(user_auto_key=user_rec_id)
        user_rec = user_rec and user_rec[0] or None
        new_val = 'Record (ctrl_number + 000000 + ctrl_id): '+ ctrl_number + '000000' + ctrl_id + ' location_code: ' + location_code + 'qty: ' + new_qty
        field_changed = 'quantity'
        right_now = datetime.now()
        now = right_now.strftime('%Y-%m-%d %H:%M:%S')
        msg = register_audit_trail(user_rec,field_changed,new_val,now,app_id)         
    return msg
    
def verify_loc_input(locations,loc_auto_key):
    res = loc_auto_key in (item for loc_list in locations for item in loc_list) 
    return res
   
#============================================================================Racking=====================================================================
def check_if_same_whs(whs_code, woo_auto_key, user_id='', quapi=None):
    """
    Arguments: location - code supplied by user form input
            woo_auto_key - from a lookup of SI_NUMBER (wo_number) supplied by user form input           
    Returns: results from location       
    """
    update_ok = False
    stm_auto_key = ''
    #location code is what they enter/scan => 
    #from location - lookup location table to find location code
    query = """
    SELECT S.STM_AUTO_KEY, WH.WHS_AUTO_KEY, WH.WAREHOUSE_CODE 
        FROM WO_OPERATION W, WO_STATUS WS,STOCK_RESERVATIONS SR, STOCK S, WAREHOUSE WH 
        WHERE
            W.WOO_AUTO_KEY = SR.WOO_AUTO_KEY 
            AND SR.STM_AUTO_KEY = S.STM_AUTO_KEY 
            AND S.WHS_AUTO_KEY = WH.WHS_AUTO_KEY 
            AND W.WOO_AUTO_KEY = %s"""%(woo_auto_key)
    results = selection(query, user_id=user_id, quapi=quapi)      
    result = results and results[0] or None
    stm_auto_key = result and result[0] or None
    if type(stm_auto_key) is list:
        stm_auto_key = stm_auto_key[0]
    if result and result[2] and result[2] != whs_code:
        update_ok = True           
    return stm_auto_key,update_ok        
    
def update_wh(warehouse, whs_auto_key, woo_auto_key, user_id, wos_obj, rack_auto_key=None, quapi=None):  
    stm_auto_key,update_ok = check_if_same_whs(warehouse, woo_auto_key, user_id, quapi=quapi)
    msg = ''
    if stm_auto_key and update_ok and whs_auto_key:
        where_clause = rack_auto_key and ' AND IC_UDL_005 = %s'%rack_auto_key or ''
        query = "UPDATE STOCK SET whs_auto_key = %s WHERE stm_auto_key = %s%s"%(whs_auto_key,stm_auto_key,where_clause)
        msg = updation(query, user_id=user_id, quapi=quapi)
    else: 
        msg += 'Not able to update the warehouse.'
    #if not msg and not rack_auto_key:
    #    woo_object = wos_obj.objects.filter(woo_auto_key=woo_auto_key, is_racking=0, is_dashboard=0, active=1, user_id=user_id)
    #    woo_object = woo_object and woo_object.update(wh_code=warehouse)    
    return msg
    
def get_whs_from_loc(loc_auto_key, user_id, quapi=None):
    query = "SELECT WHS_AUTO_KEY FROM WAREHOUSE_LOCATIONS WHERE LOC_AUTO_KEY=%s"%loc_auto_key
    res = selection(query, user_id=user_id, quapi=quapi)
    return res
    
def check_if_valid_whs(whs_auto_key,rack_auto_key=None,loc_auto_key=None,stm_auto_key=None,user_id='',quapi=None):
    valid_wh,error = False,''
    #check to see if we must update the warehouse because the location belongs to a different warehouse
    loc_whs_keys = get_whs_from_loc(loc_auto_key, user_id, quapi=quapi)
    loc_whs_key = loc_whs_keys and loc_whs_keys[0] and loc_whs_keys[0][0] or None
    if whs_auto_key and loc_auto_key:       
        if len(loc_whs_keys) == 1:
            if whs_auto_key and loc_whs_key != whs_auto_key:
                error = 'The warehouse is not valid for that location.  Please enter a valid one.' 
            else:
                valid_wh = True 
                loc_whs_key = whs_auto_key                
        elif len(loc_whs_keys) > 1:
            for key in loc_whs_keys:
                if key[0] == whs_auto_key:
                    valid_wh = True
                    loc_whs_key = whs_auto_key
                    break
        if not valid_wh and not error:
            error = 'The location has multiple warehouses and none match your entry.  Please enter a valid one.'
    return error,valid_wh,loc_whs_key

def update_location_from_rack(rack_auto_key=None, loc_auto_key=None, whs_auto_key=None, iq_enable='F',user_id='',quapi=None):
    #update all stock line's locations that are on the rack the users scanned in (Transer Cart mode)
    update_wh,loc_whs_key,valid_whs_key = False,'',None
    set_rack_null = iq_enable == 'T' and ", IC_UDL_005 = NULL" or ''          
    #if the loc_whs_key doesn't match the actual warehouse key on stock line, then change the warehouse
    #on stock to match that of the location's warehouse    
    #or if the stock line has a warehouse that is not tied to the location, we must change it    
    if loc_auto_key: 
        query = """UPDATE STOCK SET LOC_AUTO_KEY = %s%s WHERE IC_UDL_005 = %s AND (LOC_AUTO_KEY <> %s OR LOC_AUTO_KEY IS NULL) AND HISTORICAL_FLAG = 'F'"""%(loc_auto_key,set_rack_null,rack_auto_key,loc_auto_key)
        error = updation(query, user_id=user_id,quapi=quapi) 
        error,valid_wh,valid_whs_key = check_if_valid_whs(rack_auto_key=rack_auto_key, loc_auto_key=loc_auto_key, whs_auto_key=whs_auto_key, user_id=user_id,quapi=quapi) 
        if valid_whs_key:
            query = """UPDATE STOCK SET WHS_AUTO_KEY = %s WHERE IC_UDL_005 = %s AND (WHS_AUTO_KEY <> %s OR WHS_AUTO_KEY IS NULL) AND HISTORICAL_FLAG = 'F'"""%(valid_whs_key,rack_auto_key,valid_whs_key)
            error += updation(query, user_id=user_id,quapi=quapi) 
        #if user didn't enter the warehouse, then we have to check every record to see if we need to 
        #update the warehouse to one that is valid for the location        
        else:
            query = "SELECT WHS_AUTO_KEY,STM_AUTO_KEY FROM STOCK WHERE IC_UDL_005 = %s"%rack_auto_key
            res = selection(query, user_id=user_id,quapi=quapi) 
            for line in res:
                whs_key = line[0]
                stm_key = line[1]
                if whs_key:
                    error,valid_wh,valid_whs_key = check_if_valid_whs(whs_key, loc_auto_key=loc_auto_key,quapi=quapi) or False 
                if not valid_wh and valid_whs_key:
                    #must change it to a valid one
                    query = "UPDATE STOCK SET WHS_AUTO_KEY = %s WHERE STM_AUTO_KEY = %s"%(valid_whs_key,stm_key)
                    error = updation(query, user_id=user_id,quapi=quapi) 
    elif not loc_auto_key and whs_auto_key and rack_auto_key:
        #check that the warehouse is a valid one for each stock line on the cart 
        query = "SELECT LOC_AUTO_KEY,STM_AUTO_KEY FROM STOCK WHERE IC_UDL_005 = %s"%rack_auto_key
        res = selection(query, user_id=user_id,quapi=quapi)  
        for line in res:
            loc_key = line[0]
            stm_key = line[1]
            if loc_key:
                error,valid_wh,valid_whs_key = check_if_valid_whs(whs_auto_key=whs_auto_key, loc_auto_key=loc_key, quapi=quapi) or False 
                if valid_wh:
                    query = "UPDATE STOCK SET WHS_AUTO_KEY = %s WHERE STM_AUTO_KEY = %s"%(whs_auto_key,stm_key)
                    error += updation(query, user_id=user_id, quapi=quapi)
                    update_wh = True
                else:
                    error = "Invalid warehouse for the stock on that cart."       
    return error,update_wh
    
def get_locs_from_wh(whs_auto_key, user_id='',quapi=None):
    query = "SELECT LOC_AUTO_KEY FROM WAREHOUSE_LOCATIONS WHERE WHS_AUTO_KEY=%s"%whs_auto_key
    res = selection(query, user_id=user_id, quapi=quapi)
    return res
    
def update_whs_from_rack(rack_auto_key, whs_auto_key, user_id='', quapi=None):
    #update all stock line's warehouses that are on the rack the users scanned in
    valid_loc_keys = get_locs_from_wh(whs_auto_key)
    loc_key_list = valid_loc_keys and valid_loc_keys[0] and valid_loc_keys[0][0] and '(' + str(valid_loc_keys[0][0]) or '('
    count = 1
    for loc in valid_loc_keys[1:]:
        loc_key_list += ',' + str(loc[0])
        if (count+1)%995 == 0 and loc_key_list[count+1]:
            loc_key_list += ') OR LOC_AUTO_KEY IN (' + str(loc_key_list[count+1])
        count += 1              
    loc_key_list += ')'
    query = """UPDATE STOCK SET WHS_AUTO_KEY = %s 
                    WHERE IC_UDL_005 = %s
                   AND (WHS_AUTO_KEY <> %s OR WHS_AUTO_KEY IS NULL)
                   AND HISTORICAL_FLAG = 'F'
                   AND LOC_AUTO_KEY IN %s"""%(whs_auto_key,rack_auto_key,whs_auto_key,loc_key_list)
    msg = updation(query, user_id=user_id, quapi=quapi)  
    return msg
    
def assign_new_wh(stm_auto_key, whs_auto_key, user_id='',quapi=None):
    query = "UPDATE STOCK SET WHS_AUTO_KEY = %s WHERE STM_AUTO_KEY = %s"%(whs_auto_key,stm_auto_key)
    msg = updation(query, user_id=user_id, quapi=quapi)
    return msg
        
def assign_rack_new_wh(rack_code, whs_auto_key, user_id='',quapi=None):
    query = "UPDATE STOCK SET WHS_AUTO_KEY = %s WHERE STM_AUTO_KEY IN (SELECT STM_AUTO_KEY FROM STOCK WHERE IC_UDL_005 = (SELECT UDL_AUTO_KEY FROM USER_DEFINED_LOOKUPS WHERE UDL_CODE = '%s'))"%(whs_auto_key,rack_code)
    msg = updation(query, user_id=user_id, quapi=quapi)
    return msg
    
def get_warehouse_location(location_code,user_id='',quapi=None):
    #from location code, we will look up and get the warehouse from the rel table
    query = "SELECT WHS_AUTO_KEY FROM WAREHOUSE_LOCATIONS WHERE LOC_AUTO_KEY = (SELECT LOC_AUTO_KEY FROM LOCATION WHERE LOCATION_CODE = %s)"%location_code
    res = selection(query, user_id=user_id, quapi=quapi)
    return res
   
def get_wos_from_rack(quapi=None,rack_auto_key=None,whs_auto_key=None,loc_auto_key=None,woo_auto_key=None,stm_auto_key=None,ctrl_id=None,ctrl_number=None,wo_number=None,user_id=''):  
    res = []
    and_where=''
    if woo_auto_key:
        and_where = "AND W.WOO_AUTO_KEY = %s"%woo_auto_key
    if stm_auto_key:
        and_where = "AND S.STM_AUTO_KEY = %s"%stm_auto_key        
    elif ctrl_id and ctrl_number:
        and_where = "AND S.CTRL_ID = %s AND S.CTRL_NUMBER = %s"%(ctrl_id,ctrl_number)
    elif wo_number:
        and_where = "AND W.SI_NUMBER = '%s'"%wo_number
    else:
        if rack_auto_key:
            and_where += "AND S.IC_UDL_005 IS NOT NULL AND S.IC_UDL_005 = %s"%rack_auto_key
        if whs_auto_key:
            and_where += "AND S.WHS_AUTO_KEY IS NOT NULL AND S.WHS_AUTO_KEY = %s"%whs_auto_key
        if loc_auto_key:
            and_where += "AND S.LOC_AUTO_KEY IS NOT NULL AND S.LOC_AUTO_KEY = %s"%loc_auto_key               
    query = """
        SELECT DISTINCT W.SI_NUMBER, WS.DESCRIPTION, W.DUE_DATE, S.STOCK_LINE, P.PN, P.DESCRIPTION, 
          S.SERIAL_NUMBER, L.LOCATION_CODE, WS.SEVERITY,W.ENTRY_DATE,W.COMPANY_REF_NUMBER,
          W.WOO_AUTO_KEY,W.RANK,WS.WOS_AUTO_KEY,S.STM_AUTO_KEY,WH.WAREHOUSE_CODE,
          UDL.UDL_CODE,S.CTRL_ID,S.CTRL_NUMBER,S.IC_UDL_005,SR.STR_AUTO_KEY,S.LOC_AUTO_KEY,
          S.WHS_AUTO_KEY FROM STOCK S
            LEFT JOIN STOCK_RESERVATIONS SR ON SR.STM_AUTO_KEY = S.STM_AUTO_KEY 
            LEFT JOIN WO_OPERATION W ON W.WOO_AUTO_KEY = SR.WOO_AUTO_KEY 
            LEFT JOIN PARTS_MASTER P ON P.PNM_AUTO_KEY = S.PNM_AUTO_KEY
            LEFT JOIN LOCATION L ON L.LOC_AUTO_KEY = S.LOC_AUTO_KEY
            LEFT JOIN WAREHOUSE WH ON WH.WHS_AUTO_KEY = S.WHS_AUTO_KEY
            LEFT JOIN WO_STATUS WS ON WS.WOS_AUTO_KEY = W.WOS_AUTO_KEY 
            LEFT JOIN USER_DEFINED_LOOKUPS UDL ON UDL.UDL_AUTO_KEY = S.IC_UDL_005
        WHERE
          (W.WOS_AUTO_KEY IS NULL
          OR WS.STATUS_TYPE IN ('Open','Delay','Defer')) 
          AND S.HISTORICAL_FLAG = 'F'
          AND S.QTY_OH > 0 %s"""%and_where
    res = selection(query, user_id=user_id,quapi=quapi)
    return res
    
"""App retrieves a list of stock lines with that UDL_AUTO_KEY in IC_UDL_005 of the stock table
    - User begins scanning SI_NUMBERS or CTRL # + CTRL ID application finds the STM_AUTO_KEY and this assigns or updates the stock lines’ “Rack” (IC_UDL_005). [method done]
    - Now all stock lines scanned are assign that “Rack” (UDL_AUTO_KEY in STOCK tables’ IC_UDL_005) [DEF]
    - Entering “RACK” and updating “LOCATION” should update LOC_AUTO_KEY on all STM_AUTO_KEYs assigned to that rack (unless that STM_AUTO_KEY is already assigned to that LOC_AUTO_KEY).[DEF]
"""

def get_woo_from_stock(stm_auto_key,user_id='',quapi=None):
    query = """SELECT W.WOO_AUTO_KEY,W.SI_NUMBER FROM WO_OPERATION W
          LEFT JOIN STOCK_RESERVATIONS SR ON W.WOO_AUTO_KEY = SR.WOO_AUTO_KEY
          LEFT JOIN STOCK S ON SR.STM_AUTO_KEY = S.STM_AUTO_KEY
                  WHERE S.STM_AUTO_KEY = %s
                  AND S.HISTORICAL_FLAG = 'F'"""%stm_auto_key
    res = selection(query, user_id=user_id,quapi=quapi)
    return res
    
def get_records(ctrl_id=None,ctrl_number=None,wo_number=None,woo_auto_key=None,rack_auto_key=None,user_id='',quapi=None):
    where_clause = ''
    if ctrl_id and ctrl_number:
        where_clause = "WHERE S.CTRL_ID = %s AND S.CTRL_NUMBER = %s"%(ctrl_id,ctrl_number)
    elif wo_number:
        where_clause = "WHERE W.SI_NUMBER = '%s'"%wo_number
    elif woo_auto_key:
        where_clause = "WHERE SR.WOO_AUTO_KEY = %s"%woo_auto_key
    elif rack_auto_key:
        where_clause = "WHERE S.IC_UDL_005 = %s"%rack_auto_key    
    query = """SELECT W.SI_NUMBER,P.PN, P.DESCRIPTION,S.SERIAL_NUMBER,L.LOCATION_CODE,WH.WAREHOUSE_CODE,
    UDL.UDL_CODE,S.CTRL_ID,S.CTRL_NUMBER,W.WOO_AUTO_KEY,S.STM_AUTO_KEY,S.IC_UDL_005,
    S.LOC_AUTO_KEY,S.WHS_AUTO_KEY,W.WOS_AUTO_KEY FROM STOCK S 
    LEFT JOIN STOCK_RESERVATIONS SR ON SR.STM_AUTO_KEY = S.STM_AUTO_KEY 
    LEFT JOIN WO_OPERATION W ON W.WOO_AUTO_KEY = SR.WOO_AUTO_KEY 
    LEFT JOIN PARTS_MASTER P ON P.PNM_AUTO_KEY = S.PNM_AUTO_KEY
    LEFT JOIN LOCATION L ON L.LOC_AUTO_KEY = S.LOC_AUTO_KEY
    LEFT JOIN WAREHOUSE WH ON WH.WHS_AUTO_KEY = S.WHS_AUTO_KEY
    LEFT JOIN WO_STATUS WS ON WS.WOS_AUTO_KEY = W.WOS_AUTO_KEY
    LEFT JOIN USER_DEFINED_LOOKUPS UDL ON UDL.UDL_AUTO_KEY = S.IC_UDL_005 %s"""%where_clause       
    res = selection(query, user_id=user_id,quapi=quapi)
    return res 

def create_records(stock_recs, wos_obj, is_racking=1):
    objects = []
    for wo_number,part_number,description,serial_number,location_code,wh_code,rack,ctrl_id,ctrl_number,woo_auto_key,stm_auto_key,ic_udl_oofive,active,is_dashboard,user_id,is_racking in stock_recs:
        objects.append(wos_obj(
                wo_number = wo_number,#0 - W.SI_NUMBER
                part_number = part_number,#1- P.PN
                description = description,#2- P.DESCRIPTION
                serial_number = serial_number,#3- S.SERIAL_NUMBER
                location_code = location_code,#4- L.LOCATION_CODE
                wh_code = wh_code,#5 -WH.WAREHOUSE_CODE
                rack = rack,#6- S.IC_UDL_005
                ctrl_id = ctrl_id,#7- S.CTRL_ID
                ctrl_number = ctrl_number,#8-S.CTRL_NUMBER
                woo_auto_key = woo_auto_key,#9-W.WOO_AUTO_KEY
                stm_auto_key = stm_auto_key,#10-S.STM_AUTO_KEY
                active = active,
                is_dashboard = is_dashboard,
                user_id = user_id,  
                is_racking = is_racking,                
        ))
    msg = wos_obj.objects.bulk_create(objects)
    return msg
    
def update_stock_rack(stm_auto_key,rack_auto_key=None,whs_auto_key=None,loc_auto_key=None,iq_enable='F',user_id='',quapi=None): 
    set_where,set_rack,set_loc,set_wh,valid_wh = '','','','',False
    whrack,whloc,whware='','',''
    where = ' WHERE stm_auto_key = %s'%stm_auto_key
    if stm_auto_key and rack_auto_key:
        set_rack = "SET ic_udl_005=%s"%rack_auto_key
        whrack = where + " AND (ic_udl_005 <> %s OR ic_udl_005 IS NULL)"%rack_auto_key  
        query = "UPDATE STOCK %s "%set_rack + whrack
        msg = updation(query,user_id=user_id,quapi=quapi)
    if loc_auto_key:
        #if the user only enters location, then we just check the existing warehouse
        set_loc = "SET loc_auto_key=%s"%loc_auto_key
        whloc = where + " AND (loc_auto_key <> %s OR loc_auto_key IS NULL)"%loc_auto_key
        query = "UPDATE STOCK %s "%set_loc + whloc
        msg = updation(query,user_id=user_id,quapi=quapi) 
        error,valid_wh,valid_whs_key = check_if_valid_whs(whs_auto_key,loc_auto_key=loc_auto_key,user_id=user_id,quapi=quapi)   
        if valid_whs_key:
            whs_auto_key = valid_whs_key
        if not rack_auto_key and stm_auto_key and iq_enable == 'T':
            query = "UPDATE STOCK SET IC_UDL_005 = NULL WHERE STM_AUTO_KEY = %s"%stm_auto_key
            msg += updation(query, user_id=user_id,quapi=quapi)      
    if whs_auto_key:
        set_wh = "SET whs_auto_key=%s"%whs_auto_key
        whware = where + " AND (whs_auto_key <> %s OR whs_auto_key IS NULL)"%whs_auto_key
        query = "UPDATE STOCK %s "%set_wh + whware
        msg = updation(query, user_id=user_id,quapi=quapi)  
    #if not valid_wh and not valid_whs_key:
    #    return 'Cannot update to that warehouse and there is not another one that is valid for the location'  
    try:
        int(stm_auto_key)
    except Exception as error:
        msg += "\r\nError with stock auto key." 
        return msg
    return msg
    
def register_audit_trail(user_rec,field_changed,new_val,right_now,app_id):
    msg = ''
    ml_apps_id = app_id and app_id[0] or None
    description = 'Audit trail entry for user=%s,'%user_rec.user_id
    description += 'field(s): %s, and new value(s): %s'%(field_changed,new_val)
    description += ', app: %s'%(ml_apps_id and ml_apps_id.name or '')
    from polls.models import AuditTrail as adt
    try:
        new_log = adt.objects.create(
            field_changed = field_changed,
            description = description,
            new_val = new_val,
            create_date = right_now,
            ml_apps_id = ml_apps_id,
            user_id = user_rec,
        )
        new_log.save()
    except Exception as error:
        msg += "\r\nThere was an error with registering the change to the audit log." 
    return msg
    
@task
def run_racking(session_id,quapi_id=None,mode=0,rack='', lookup_recs = 0, warehouse='',location='',new_status='',wo_number='',user_id='',sysur_auto_key=None,woo_key_list=[],ctrl_number=None,ctrl_id=None):    
    from polls.models import WOStatus as wos_obj,QueryApi
    quapi = QueryApi.objects.filter(id=quapi_id)
    quapi = quapi and quapi[0] or None
    stm_auto_key,stock_rec,woo_auto_key,ic_udl_oofive,rack_auto_key,loc_auto_key,whs_auto_key = None,[],None,None,None,None,None
    msg,loc,synch,stat,trail,upd,error,field_changed,new_val,audit_ok = '','','','','','','','','',False
    iq_enable,stock_recs = 'F',[]
    #get woo_auto_key from query and then pass it to all of these queries instead of SI_NUMBER as the key.
    if not session_id:
        return 'Invalid session.  Please login and try again.',msg 
    if not mode or (mode in ['1','2','3'] and not wo_number) or (mode == '1' and lookup_recs not in [0,'0','False',False]):
        active_woos = wos_obj.objects.filter(active=1, is_dashboard=0, user_id=user_id, is_racking=1)    
        woos_updated = active_woos and active_woos.delete() or None 
    if rack:
        query = "SELECT UDL_AUTO_KEY FROM USER_DEFINED_LOOKUPS WHERE UDL_CODE = '%s'"%rack
        res = selection(query,user_id=user_id,quapi=quapi)
        rack_auto_key = res and res[0] and res[0][0] or None
        if not rack_auto_key:
            return 'Cart not found.',msg
        field_changed += 'rack'
        new_val += ', ' + str(rack)
    if location:
        query = "SELECT loc_auto_key,iq_enable FROM LOCATION WHERE location_code = '%s'"%location
        res = selection(query,user_id=user_id,quapi=quapi)
        loc_auto_key = res and res[0] and res[0][0] or None
        iq_enable = res and res[0] and res[0][1] or None 
        #fix for the records assigned backasswards 
        if iq_enable == 'T':
            iq_enable = 'F'        
        if not loc_auto_key:
            return 'Location not found.',msg
        field_changed += ', location'
        new_val += ', ' + str(location)
    if warehouse:
        query = "SELECT whs_auto_key FROM WAREHOUSE WHERE warehouse_code = '%s'"%warehouse
        res = selection(query,user_id=user_id,quapi=quapi)
        whs_auto_key = res and res[0] and res[0][0] or None
        if not whs_auto_key:
            return 'Warehouse not found.',msg 
        field_changed += ', warehouse'
        new_val += ', ' + str(warehouse)        
    right_now = datetime.now()
    now = right_now.strftime('%Y-%m-%d %H:%M:%S')
    nowly = right_now.strftime('%m-%d-%Y %H:%M:%S')    
    #Mode 1 - Assign stock records entered by user to rack
    if mode == '1':  #Update mode
        if wo_number:         
            stock_rec = get_wos_from_rack(ctrl_id=ctrl_id,ctrl_number=ctrl_number,wo_number=wo_number,user_id=user_id,quapi=quapi) 
            if not stock_rec:
                if ctrl_id and ctrl_number:
                    #lookup again by adding a zero to the end of the ctrl_number
                    ctrl_number = ctrl_number + '0'
                    stock_rec = get_wos_from_rack(ctrl_id=ctrl_id,ctrl_number=ctrl_number,user_id=user_id,quapi=quapi) 
                    if not stock_rec:
                        return 'No workorders nor stock lines exist for: %s'%wo_number,''
            #stock_rec = stock_rec and stock_rec[0] or []
            if stock_rec and isinstance(stock_rec[0],list):
                stm_auto_key = stock_rec[0][14]
                location_key = stock_rec[0][21]
                warehouse_key = stock_rec[0][22]
                status_key = stock_rec[0][13]
                woo_auto_key = stock_rec[0][11]  
            else:
                return 'No record found.','' 
            if new_status and woo_auto_key:              
                if status_key == new_status: 
                    return 'This record is already in that status. ',''                       
                stat = set_status(woo_auto_key,new_status,user_id=user_id,quapi=quapi)               
                timestamp = get_stamptime(woo_auto_key,new_status,user_id=user_id,quapi=quapi)  
                timestamp = timestamp and timestamp[0] or None
                if type(timestamp) is list:
                    timestamp = timestamp[0]
                if type(timestamp) is datetime:
                    timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                trail = update_trail(sysur_auto_key, woo_auto_key, new_status=new_status,user_id=user_id,quapi=quapi)    
                orcl_commit(user_id=user_id,quapi=quapi) 
                field_changed += ', status'
                new_val += str(new_status) 
                audit_ok = True               
        if not wo_number and not (rack or location or warehouse or new_status):
            return 'Enter a record to assign it to a cart, location or warehouse.',msg
        if not wo_number and new_status:
            return 'Enter a record number to assign a new status.',msg
        if stock_rec and stm_auto_key and (rack or location or warehouse or new_status):
            if rack or location or warehouse:
                msg = update_stock_rack(stm_auto_key,
                    rack_auto_key=rack_auto_key,
                    loc_auto_key=loc_auto_key or location_key,
                    whs_auto_key=whs_auto_key or warehouse_key,
                    iq_enable=iq_enable, user_id=user_id,
                    quapi=quapi,                    
                    ) 
                orcl_commit(user_id=user_id,quapi=quapi)                    
                if not msg:
                    audit_ok = True                  
            stock_recs = get_wos_from_rack(stm_auto_key=stm_auto_key,user_id=user_id,quapi=quapi) 
            error,msg = add_wo_record(session_id=session_id,is_dashboard=0,is_racking=1,keep_recs=True,user_id=user_id,woo_recs=stock_recs,quapi=quapi)             
        elif rack_auto_key or loc_auto_key or whs_auto_key:            
            stock_recs = get_wos_from_rack(whs_auto_key=whs_auto_key,loc_auto_key=loc_auto_key,rack_auto_key=rack_auto_key,user_id=user_id,quapi=quapi)                      
            #use method from WO Mgmt to bring in WO's in bulk
            if stock_recs:
                error,msg = add_wo_record(session_id=session_id,is_dashboard=0,is_racking=1,user_id=user_id,woo_recs=stock_recs,quapi=quapi)   
            else:
                return 'No records found.',''             
    #Mode 2 - Move stock on rack to another location or rack as long as the stock line is not historical.            
    elif mode == '2': #Move stock to another warehouse, location or cart as long as the stock line is not historical. 
        #if location is iq_enable = 'T', then set the cart to null          
        if not rack_auto_key:
            return 'Enter a cart to see the stock on it and a location to move stock on the cart to another location.',msg 
        elif whs_auto_key or loc_auto_key:
            error,wh_updated = update_location_from_rack(rack_auto_key=rack_auto_key, loc_auto_key=loc_auto_key, whs_auto_key=whs_auto_key, iq_enable=iq_enable,user_id=user_id,quapi=quapi) 
            if error != 'no errors':
                 return error,msg
            else:
                audit_ok = True      
        #if whs_auto_key and not wh_updated:
        #    error += update_whs_from_rack(rack_auto_key, whs_auto_key)     
        orcl_commit(user_id=user_id,quapi=quapi)  
        #wos will be a list of lists of data to create the WO's
        stock_recs = get_wos_from_rack(rack_auto_key=rack_auto_key,user_id=user_id,quapi=quapi) 
        #use method from WO Mgmt to bring in WO's in bulk
        if stock_recs:
            error,msg = add_wo_record(session_id=session_id,is_dashboard=0,is_racking=1,user_id=user_id,woo_recs=stock_recs,quapi=quapi) 
            if error:
                return error,msg   
        else:
            return 'No records found.',''                 
    #Mode 3 - Validate Location and Rack               
    elif mode == '3': #validate mode
        #if not wo_number:
        #    return error,'Enter a record to validate.'
        #when we have a list of WO's and they are scanned with no rack entered, they will be removed from the list.
        #match with existing record in SQLite
        #first check that it is on the list
        if wo_number:
            woo_to_val = wos_obj.objects.filter(is_dashboard=0, is_racking=1, user_id = user_id, wo_number = wo_number, active=1)
            if ctrl_id and ctrl_number:
                woo_to_val = wos_obj.objects.filter(is_dashboard=0, is_racking=1, user_id = user_id, ctrl_id=ctrl_id, ctrl_number=ctrl_number, active=1)                
            if woo_to_val:               
                stm_auto_key = woo_to_val and woo_to_val[0] or None
                stm_auto_key = stm_auto_key and stm_auto_key.stm_auto_key or None                    
                stock_rec = stm_auto_key and get_wos_from_rack(stm_auto_key=stm_auto_key,user_id=user_id,quapi=quapi) or None                   
                if not stock_rec:
                    return 'No workorders nor stock lines exist for: %s'%wo_number,msg
                stm_auto_key = stock_rec[0][14]
                ic_udl_oofive = stock_rec[0][19]
                location_key = stock_rec[0][21]
                warehouse_key = stock_rec[0][22]
                status_key = stock_rec[0][13]
                woo_auto_key = stock_rec[0][11] 
                if rack_auto_key:
                    if ic_udl_oofive != rack_auto_key:
                        return 'This record is not on this rack.',msg 
                elif loc_auto_key:
                    if loc_auto_key != location_key:
                        return 'This record is not in this location.',msg
                elif whs_auto_key: 
                    if whs_auto_key != warehouse_key:
                        return 'This record is not in this warehouse.',msg
                else:
                    return 'You must input a warehouse, location or cart and a record number/scan to validate.',msg                
                if stm_auto_key:
                    #update stock table loc_validated with timestamp
                    ##******TODO*******FIND WAY TO GET THE SYSTEM TIMEZONE AND SUBTRACT NUMBER OF HOURS*********                
                    query = """UPDATE STOCK SET LOC_VALIDATED = TO_TIMESTAMP('%s', 'MM-DD-YYYY HH24:MI:SS')
                               WHERE STM_AUTO_KEY = %s"""%(nowly,stm_auto_key)
                    upd=updation(query,user_id=user_id,quapi=quapi)
                    error += upd
            else:
                return "The record is already validated or is not on cart: '%s'."%rack,msg
            if error == 'no errors':             
                woo_to_val.delete()
                msg += 'Record validated. ' 
        elif rack_auto_key or loc_auto_key or whs_auto_key:
            #wos will be a list of lists of data to create the WO's
            stock_recs = get_wos_from_rack(rack_auto_key=rack_auto_key,loc_auto_key=loc_auto_key,whs_auto_key=whs_auto_key,user_id=user_id,quapi=quapi)   
            #use method from WO Mgmt to bring in WO's in bulk
            if stock_recs:
                error,msg = add_wo_record(session_id=session_id,is_dashboard=0,is_racking=1,user_id=user_id,woo_recs=stock_recs,quapi=quapi) 
            else:
                return 'No records found.',''
        else:
            return 'Enter a cart, location or warehouse to get records to validate or a record you wish to validate against your record set.',''       
    else:
        return 'Select a mode and enter a cart# to proceed.',msg
    orcl_commit(user_id=user_id,quapi=quapi)
    #must register an audit trail record locally - ADT
    #app_id = MLApps.objects.filter(name='Barcoding')
    from polls.models import MLApps as map,QuantumUser as qu
    maps = map.objects.all()
    """maps.delete()
    new= maps.create(code='piu',name='Physical Inventory Update',uri='pi_update')
    new.save()
    new= maps.create(code='wos',name='Barcoding Status',uri='barcoding')
    new.save()
    new= maps.create(code='rac',name='Barcoding Carts & Locations',uri='barcoding')
    new.save()
    new= maps.create(code='das',name='Workorder Dashboard',uri='wo-dashboard')
    new.save()"""    
    app_id = maps.filter(code='racking') 
    user_rec = qu.objects.filter(user_id=user_id)
    user_rec = user_rec and user_rec[0] or None
    stm_keys = set(rec[14] for rec in stock_recs)
    stm_key_list = list(stm_keys)
    field_changed += ', stock records(s) changed:' + str(stm_key_list)
    if user_rec and new_val and audit_ok:
        error += register_audit_trail(user_rec,field_changed,new_val,now,app_id)
    return str(error),str(msg)