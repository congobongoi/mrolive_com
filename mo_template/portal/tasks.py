#!/usr/bin/env python3
import requests
import importlib
import dateparser
import os
os.environ[ 'DJANGO_SETTINGS_MODULE' ] = "mo_template.settings"
from celery import Celery,shared_task
from celery.schedules import crontab
from datetime import datetime,timedelta
import sys
sys.path.append(os.getcwd())
import logging
logger = logging.getLogger(__name__)
#for Memurai
#celery_app = Celery('tasks', broker='redis://localhost:6373/0', backend="rpc://")
celery_app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
celery_app.conf.update(broker_transport_options={"max_retries": 0, "interval_start": 0, "interval_step": 0.2, "interval_max": 0.5}, accept_content = ['json','pickle'],accept_results = ['json','pickle'],broker_heartbeat = 15,acks_late=False)
from django.conf import settings
FILE_PATH = settings.MEDIA_URL


#====================================================GENERAL HELPER/QUERY QUANTUM METHODS================================================

import cx_Oracle
def jsonicize(recs):    
    from django.http import JsonResponse
    #responseData = {
    #    'recs':recs,
    #}
    return JsonResponse(recs,safe=False)
    
def orcl_connect(schema):
    cr=None
    con=None
    if schema:
        try:
            #import pyodbc
            #con_str = 'DSN=QCTL;pwd=quantum'
            #con = pyodbc.connect(con_str)
            #pool = cx_Oracle.SessionPool(schema.schema, schema.db_user, schema.host + ':' + str(schema.port) + '/' + schema.sid, min=1, max=3, increment=1, encoding="UTF-8")
            #con = pool.acquire()
            if schema.db_pwd and schema.db_pwd != 'none':
                con = cx_Oracle.connect(user=schema.db_user,\
                    password=schema.db_pwd,\
                    dsn=schema.host+':'+str(schema.port)+'/'+schema.sid)
            else:
                connstr = schema.schema + '/' + schema.db_user + '@' + schema.host + ':' + str(schema.port) + '/' + schema.sid
                con = cx_Oracle.connect(connstr)
            """from django.contrib.auth.models import User
            from django.contrib.sessions.models import Session
            from django.utils import timezone
            active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
            #active_sessions = Session.objects.all()
            num_sessions = len(active_sessions)
            if num_sessions > 2:
                pool = cx_Oracle.SessionPool(schema.schema, schema.db_user, schema.host + ':' + str(schema.port) + '/' + schema.sid, min=2, max=3, increment=1, encoding="UTF-8")
                con = pool.acquire()"""
            #print('successful connection to Oracle')
        except Exception as exc:
            error, = exc.args
    cr = con and con.cursor() or None
    if not con:
        return False,False
    return cr,con
    
def insertion_dir(query,cr,quapi=None):
    recs = []
    msg = ''
    if not cr and quapi:
        
        from polls.models import OracleConnection as oc
        orcl_conn = quapi and quapi.orcl_conn_id and oc.objects.filter(id=quapi.orcl_conn_id) or None
        orcl_conn = orcl_conn and orcl_conn[0] or None
        if orcl_conn:
            cr,con = orcl_connect(orcl_conn)
        if not (cr and con):
            return 'Cannot connect to Oracle.'
    try:
        cr.execute(query)      
    except Exception as exc:
        error, = exc.args
        msg = error.message
        print("Oracle-Error-Code:", error.code)
        print("Oracle-Error-Message:", msg)
    return str(msg)
       
def selection_dir(query,cr):
    recs = []
    res = []
    all_res = []  
    try:
        cr.execute(query)
        recs = cr.fetchall()        
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        print("Oracle-Error-Code:", error.code)
        print("Oracle-Error-Message:", error.message)
    if recs:       
        for count,rec in enumerate(recs):
            res = ['' if (field == None or field == 'None' or field == 'Null' or field == 'null' or field=='none') else field for field in rec]
            all_res.append(res)
    import json
    all_res = json.dumps(all_res,default=str)
    import ast
    recs = ast.literal_eval(all_res)
    return recs
    
def updation_dir(query,cr):   
    msg = ''
    try:
        cr.execute(query)                  
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        msg = " Oracle-Error-Message:" + str(error.message) 
    msg = not msg and '{"recs": ""}' or msg
    return str(msg)   
      
def updation(query,user_id='',quapi=None):
    msg = ''  
    if query and quapi:
        from polls.models import OracleConnection as oc
        orcl_conn = quapi and quapi.orcl_conn_id and oc.objects.filter(id=quapi.orcl_conn_id) or None
        orcl_conn = orcl_conn and orcl_conn[0] or None
        if orcl_conn:
            cr,con = orcl_connect(orcl_conn)
        if not (cr and con):
            return 'Cannot connect to Oracle' 
        else:
            msg = updation_dir(query,cr) 
    return msg
    
def insertion(query,user_id='',quapi=None):
    recs = []
    message = ''
    new_auto_key = None
    if query and quapi:
        #must be that it is an API call so we reroute it to the API
        url = quapi.conn_str
        url = url and url + 'insertion' or None
        params = {
            'query': query,
            'user_id': user_id,
            'type': 'insertion',
            'schema': quapi.orcl_conn_id or 0,
        }
        response = requests.post(url,json=params,params=params)
        success = (response.status_code == 200)  # 200 =  Success
        json =  success and response.json() or {}
        records = json and json['recs'] or [[]]
        for row in records:
            new_auto_key = row and row[0] or None
            break
    return response and response.text or ''
                       
def selection(query,table_name='',quapi=None,user_id=None):
    recs = []
    if query and quapi:
        from polls.models import OracleConnection as oc
        orcl_conn = quapi and quapi.orcl_conn_id and oc.objects.filter(id=quapi.orcl_conn_id) or None
        orcl_conn = orcl_conn and orcl_conn[0] or None
        if orcl_conn:
            cr,con = orcl_connect(orcl_conn)
        if not (cr and con):
            return 'Cannot connect to Oracle' 
        else:
            recs = selection_dir(query,cr)              
    return recs

def orcl_commit(user_id='',quapi=None, con=None):
    #commit the database updates
    msg = ''
    if quapi and not con:
        from polls.models import OracleConnection as oc
        orcl_conn = quapi and quapi.orcl_conn_id and oc.objects.filter(id=quapi.orcl_conn_id) or None
        orcl_conn = orcl_conn and orcl_conn[0] or None
        cr,con = orcl_connect(orcl_conn)
    if not con:
        return 'Cannot connect to Oracle' 
    try:    
        con.commit()
        con.close()
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        msg = error.message
        logger.error("Oracle-Error-Code: '%s'",error.code)
        logger.error("Oracle-Error-Message: '%s'",msg)          
    return msg
        
def benchmark_test(benchmark,query,quapi):
    msg = ''
    quapi = QueryApi.objects.filter(id=1)
    query = "UPDATE STOCK SET LOC_AUTO_KEY=1 WHERE STM_AUTO_KEY=2605"
    benchmark(updation(query,quapi=quapi))
    return msg  

#=========================================STOCK PICKING=================================
    
@shared_task
def stock_picking(quapi_id,sysur_auto_key,session_id,wo_number,exact_match=True,wob_id_list=[]):
    error,msg,stock_msg = '','',''
    from polls.models import QueryApi    
    quapi = QueryApi.objects.filter(id=quapi_id)
    quapi = quapi and quapi[0] or None
    cr,con = get_cursor_con(quapi)
    if not (cr and con):
        return 'Cannot connect to Oracle',msg      
    where_wo = exact_match and "W.SI_NUMBER = '%s'"%wo_number or ''
    where_wo = not exact_match and "W.SI_NUMBER LIKE '%s%s%s'"%('%',wo_number,'%') or where_wo
    where_clause = "AND %s"%where_wo 
    """
    next retrieve all WOB  and STM 
    where wob.woo_auto_key = (si_number input by user) and  wob.qty_needed <> wob.qty_issued + wob.qty_reserved and 
    wob.activity not in ( 'Turn-In', 'Work Order', 'Repair')
    group by wob.pn, stm.loc
    order by wob.pn, stm.loc
    GROUP BY P.PN,L.LOCATION_CODE
    WOBS: [3352, 4478]"""
    if wob_id_list:
        from polls.models import WOStatus as wos
        wostatus_list = wos.objects.filter(id__in = wob_id_list)

        for wob in wostatus_list:
            query = """SELECT WOB.QTY_NEEDED,S.STM_AUTO_KEY,
                S.CTRL_NUMBER, S.CTRL_ID FROM WO_BOM WOB, 
                PARTS_MASTER P, STOCK S
                WHERE WOB.WOB_AUTO_KEY = %s
                AND S.PNM_AUTO_KEY = P.PNM_AUTO_KEY
                AND P.PNM_AUTO_KEY = WOB.PNM_AUTO_KEY      
            """%(wob.wob_auto_key)
            stm_list = selection_dir(query,cr)
            for stm in stm_list:
                squery = """INSERT INTO STOCK_RESERVATIONS 
                    (STR_AUTO_KEY,STM_AUTO_KEY,WOB_AUTO_KEY,QTY_RESERVED,SYSUR_AUTO_KEY) 
                    VALUES(G_STR_AUTO_KEY.NEXTVAL,'%s','%s',%s,%s)"""%(stm[1],wob.wob_auto_key,stm[0],sysur_auto_key)
                error = insertion_dir(squery,cr)
                if not error:
                    stock_msg += str(stm[2]) + '000000' + str(stm[3]) + '| '
            if stock_msg:
                msg += '\r\nBOM: ' + str(wob.wob_auto_key) + ' - reserved stock lines: ' + stock_msg
    else:    
        query = """SELECT W.SI_NUMBER, P.PN, P.DESCRIPTION, WB.QTY_NEEDED, WB.WOB_AUTO_KEY, 
            S.SERIAL_NUMBER, S.STOCK_LINE, S.CTRL_NUMBER, S.CTRL_ID, S.QTY_AVAILABLE 
            FROM WO_OPERATION W, PARTS_MASTER P, WO_BOM WB, STOCK S, LOCATION L
            WHERE S.PNM_AUTO_KEY = P.PNM_AUTO_KEY
            AND P.PNM_AUTO_KEY = WB.PNM_AUTO_KEY
            AND WB.WOO_AUTO_KEY = W.WOO_AUTO_KEY
            AND L.LOC_AUTO_KEY = S.LOC_AUTO_KEY
            AND S.QTY_AVAILABLE > 0
            AND WB.QTY_NEEDED <> WB.QTY_ISSUED + WB.QTY_RESERVED
            AND WB.ACTIVITY NOT IN ( 'Turn-In', 'Work Order', 'Repair')
            %s 
            ORDER BY P.PN,L.LOCATION_CODE"""%where_clause
        recs = selection_dir(query,cr)
        wo_parts = {}

        for row in recs:   
            wo_part = row[0] + '_' + row[1] + '_' + row[2] + '_' + str(row[3]) + '_' + str(row[4])
            if wo_part not in wo_parts:
                wo_parts[wo_part] = [[row[5],row[6],row[7],row[8],row[9]]]
            else:
                wo_parts[wo_part].append([row[5],row[6],row[7],row[8],row[9]])
        if wo_parts:    
            error = synch_stock_picking(session_id,wo_parts)
        else:
            error = 'No records found.'    
    return error,msg
    
#=========================================SHIPPING======================================
@shared_task
def get_priorities(quapi_id,session_id,app=''):
    error = ''
    from polls.models import QueryApi,OracleConnection as oc
    quapi = QueryApi.objects.filter(id=quapi_id)
    quapi = quapi and quapi[0] or None
    orcl_conn = quapi and quapi.orcl_conn_id\
        and oc.objects.filter(id=quapi.orcl_conn_id) or None
    orcl_conn = orcl_conn and orcl_conn[0] or None
    if orcl_conn:
        cr,con = orcl_connect(orcl_conn)
    if not (cr and con):
        return 'Cannot connect to Oracle',msg

    query = """
        SELECT PRIORITY_CRITICAL FROM QUANTUM
        UNION
        SELECT PRIORITY_URGENT FROM QUANTUM
        UNION
        SELECT PRIORITY_ROUTINE FROM QUANTUM

    """
    
    recs = selection_dir(query,cr)
    from polls.models import Priority
    req_data,error = [],''
    for row in recs:       
        req_data.append(Priority(
            code = row[0],
            description = row[0],
            session_id = session_id,            
        ))
    if req_data:     
        try:
            delete = Priority.objects.filter(session_id=session_id).delete()
            rec = Priority.objects.bulk_create(req_data) or []    
        except Exception as exc:
            error += "Error, %s, with synching priorities. %s"%(exc,row[0])
    return error,app

@shared_task
def get_ship_vias(quapi_id,session_id,app=''):
    error = ''
    from polls.models import QueryApi,OracleConnection as oc
    quapi = QueryApi.objects.filter(id=quapi_id)
    quapi = quapi and quapi[0] or None
    orcl_conn = quapi and quapi.orcl_conn_id\
        and oc.objects.filter(id=quapi.orcl_conn_id) or None
    orcl_conn = orcl_conn and orcl_conn[0] or None
    if orcl_conn:
        cr,con = orcl_connect(orcl_conn)
    if not (cr and con):
        return 'Cannot connect to Oracle',msg

    query = """SELECT SVC_AUTO_KEY,SHIP_VIA_CODE,DESCRIPTION FROM 
        SHIP_VIA_CODES
    """
    recs = selection_dir(query,cr)
    from polls.models import ShipVia
    req_data,error = [],''
    for row in recs:       
        req_data.append(ShipVia(
            svc_auto_key = row[0],
            ship_via_code = row[1],
            description = row[2],
            session_id = session_id,            
        ))
    if req_data:     
        try:
            delete = ShipVia.objects.filter(session_id=session_id).delete()
            rec = ShipVia.objects.bulk_create(req_data) or []    
        except Exception as exc:
            error += "Error, %s, with synching ship via codes. %s"%(exc,row[0])
    return error,app
    
@shared_task
def get_shipping_status(quapi_id,session_id,app=''):
    error=''
    from polls.models import QueryApi,OracleConnection as oc
    quapi = QueryApi.objects.filter(id=quapi_id)
    quapi = quapi and quapi[0] or None
    orcl_conn = quapi and quapi.orcl_conn_id and oc.objects.filter(id=quapi.orcl_conn_id) or None
    orcl_conn = orcl_conn and orcl_conn[0] or None
    if orcl_conn:
        cr,con = orcl_connect(orcl_conn)
    if not (cr and con):
        return 'Cannot connect to Oracle',msg

    query = """SELECT SMS_AUTO_KEY,STATUS_CODE FROM 
        SM_STATUS
    """
    recs = selection_dir(query,cr)
    from polls.models import StatusSelection
    req_data,error = [],''
    for row in recs:       
        req_data.append(StatusSelection(
            wos_auto_key = row[0],
            text_wos = str(row[0]),
            name = row[1],
            session_id = session_id,            
        ))
    if req_data:     
        try:
            delete = StatusSelection.objects.filter(session_id=session_id).delete()
            rec = StatusSelection.objects.bulk_create(req_data) or []    
        except Exception as exc:
            error += "Error, %s, with synching shipping statuses. %s"%(exc,row[0])
    
    return error,app
    
@shared_task
def update_shipping(quapi_id,session_id,\
    sysur_auto_key,user_update,smds_list,tote,notes):
    error,msg = '',''
    from polls.models import QueryApi,OracleConnection as oc
    quapi = QueryApi.objects.filter(id=quapi_id)
    quapi = quapi and quapi[0] or None
    orcl_conn = quapi and quapi.orcl_conn_id 

    if orcl_conn:
        orcl_conn = oc.objects.filter(id=quapi.orcl_conn_id)
        orcl_conn = orcl_conn and orcl_conn[0]
        cr,con = orcl_conn and orcl_connect(orcl_conn)
        
    if not (cr and con):
        return 'Cannot connect to Oracle',msg
        
    from polls.models import WOStatus
    smds = WOStatus.objects.filter(id__in=smds_list)
    smds_list = smds.values_list('str_auto_key',flat=True)
    upd_smds_list = construct_akl(smds_list)    
    smhs_list = smds.values_list('si_number',flat=True)
    upd_smhs_list = construct_text(smhs_list) 
    upd_clause = ''
    
    if tote:
    
        if upd_clause:
            upd_clause += ', '
        upd_clause += """IC_UDL_005 = (SELECT UDL_AUTO_KEY 
            FROM USER_DEFINED_LOOKUPS 
            WHERE UPPER(UDL_CODE) = UPPER('%s'))"""%tote
            
    if notes:
    
        for upd_smds in upd_smds_list:
            upd_query = """UPDATE SM_DETAIL SET NOTES = NOTES || '; ' || '%s'
            WHERE SMD_AUTO_KEY IN (SELECT SMD_AUTO_KEY FROM STOCK_RESERVATIONS
            WHERE STR_AUTO_KEY IN %s)"""%(notes,upd_smds)
            error = updation_dir(upd_query,cr)
            if error != '{"recs": ""}':
                break
        
    if upd_clause:
    
        for upd_smds in upd_smds_list:
            query = """UPDATE STOCK SET %s
            WHERE STM_AUTO_KEY IN (SELECT STM_AUTO_KEY FROM STOCK_RESERVATIONS
            WHERE STR_AUTO_KEY IN %s)"""%(upd_clause,upd_smds)
            error = updation_dir(query,cr)
            if error != '{"recs": ""}':
                break
                
    if user_update:    
 
        for upd_smds in upd_smds_list:
            query = """UPDATE STOCK_RESERVATIONS 
                SET SYSUR_AUTO_KEY_SCAN = 
                (SELECT SYSUR_AUTO_KEY FROM 
                SYS_USERS WHERE USER_NAME = '%s')
                WHERE STR_AUTO_KEY IN %s
                """%(user_update,upd_smds) 
            error = updation_dir(query,cr)
            if error != '{"recs": ""}':
                break
    
    aud_status = 'failure'  
    
    if error == '{"recs": ""}':     
        orcl_commit(con=con)
        error = ''
        msg = 'Succcessful Update.'
        aud_status = 'success'
        
    #register audit trail record            
    from polls.models import MLApps as maps,QuantumUser as qu
    app_id = maps.objects.filter(code='smd-management')   
    user_rec = qu.objects.filter(user_auto_key=sysur_auto_key)
    user_rec = user_rec and user_rec[0] or None
    
    if user_rec:
        field_changed = 'User changed: ' + user_update 
        field_changed += ', notes added: ' + notes 
        field_changed += ', tote update: ' + tote 
        new_val = 'Update to stock record and/or reservation'
        if error:             
            aud_status = 'failure'
            new_val = error
            field_changed = 'Nothing changed.'
        right_now = datetime.now()
        now = right_now.strftime('%Y-%m-%d %H:%M:%S')  
        error += register_audit_trail(user_rec,field_changed,new_val,now,app_id,quapi,status=aud_status)
    else:
        error = 'Incorrect Quantum User ID.'
        
    return error,msg
     
def add_smd_stock(wos_obj,session_id,stock_recs):
    #Cust. Order	Due Date	Status	Part Number	Description	Qty	Seial	Loc
    """SOH.SO_NUMBER, SOD.DUE_DATE, SMS.STATUS_CODE, 
        SMH.SM_NUMBER, 
        STR.QTY_RESERVED, STR.DATE_SCAN, PNM.PN, PNM.DESCRIPTION, 
        CMP.COMPANY_NAME, SYSUR.USER_NAME, 
        STM.STOCK_LINE, STM.STM_AUTO_KEY, STM.SERIAL_NUMBER, 
        LOC.LOCATION_CODE, WHS.WAREHOUSE_CODE, STR.STR_AUTO_KEY
    """
    smd_data,error,msg = [],'',''

    for rec in stock_recs:
        smd_data.append(wos_obj(
            session_id=session_id,
            wo_number = rec[0],#so_number
            due_date = rec[1] and rec[1][:10] or None,
            status = rec[2],#SM Status
            si_number = rec[3],#SM_NUMBER
            qty_reserved = rec[4] or 0,
            start_date = rec[5] and rec[5][:10] or None,#date_scan
            part_number = rec[6],
            description = rec[7],
            customer = rec[8],
            user_id = rec[9],
            stock_line = rec[10],
            stm_auto_key = rec[11] or 0,
            serial_number = rec[12],
            location_code = rec[13],
            wh_code = rec[14], 
            str_auto_key = rec[15],
            priority = rec[16] != '0' and rec[16] or '',
            cart = rec[17],
            notes = rec[18],       
            )
        )
    try:
        
        delete = wos_obj.objects.filter(session_id=session_id).delete()
        wos_obj.objects.bulk_create(smd_data) or None
    except Exception as err:
        logger.error("Error with creation of records for the grid. Message: '%s'",err.args)           
    return error,msg
    

@shared_task
def search_shipping(quapi_id,session_id,sysur_auto_key,filter_list=[],\
    smds_list=[],is_dashboard=False):
    error,msg = '',''
    from polls.models import WOStatus as wos_obj
    stock_recs = get_smd_stock(quapi_id,session_id,sysur_auto_key,\
        filter_list=filter_list,smds_list=smds_list,is_dashboard=is_dashboard)
    if stock_recs:             
        error,msg = add_smd_stock(wos_obj,session_id,stock_recs)        
    elif not error:
        error = 'No records found.'   
    return error,msg

def get_smd_stock(quapi_id,session_id,sysur_auto_key,\
    filter_list = [],smds_list = [],is_dashboard=False):
    error,msg,where_clause = '','',''
    from polls.models import QueryApi,OracleConnection as oc
    quapi = QueryApi.objects.filter(id=quapi_id)
    quapi = quapi and quapi[0] or None
    orcl_conn = quapi and quapi.orcl_conn_id and oc.objects.filter(id=quapi.orcl_conn_id) or None
    orcl_conn = orcl_conn and orcl_conn[0] or None
    
    if orcl_conn:
        cr,con = orcl_connect(orcl_conn)
    if not (cr and con):
        return 'Cannot connect to Oracle',msg

    where_clause = " STM.QTY_OH > 0"

    if smds_list:
        from polls.models import WOStatus
        smds = WOStatus.objects.filter(id__in=smds_list)
        strs_list = smds.values_list('str_auto_key',flat=True)
        upd_strs_list = construct_akl(strs_list)
        
        for strs_in in upd_strs_list:
            where_clause += " AND STR.STR_AUTO_KEY IN %s"%strs_in
    
    if not is_dashboard and filter_list:

        if filter_list[0]:#customer
            cmp = filter_list[0] + '%'
            where_clause += " AND UPPER(CMP.COMPANY_NAME) LIKE UPPER('%s')"%cmp
            
        if filter_list[1]:#SM Order#
            order = filter_list[1] + '%'     
            where_clause += " AND UPPER(SMH.SM_NUMBER) LIKE UPPER('%s')"%order
            
        if filter_list[2]:#entry date
            entry_date = filter_list[2]
            where_clause += " AND (STR.DATE_SCAN <= TO_DATE('%s','MM/DD/YYYY') OR STR.DATE_SCAN IS NULL)"%entry_date
            
        if filter_list[3]:#status
            if filter_list[3] == '0':
                where_clause += " AND SMS.SMS_AUTO_KEY IS NULL"
            else:
                where_clause += " AND SMS.SMS_AUTO_KEY='%s'"%filter_list[3]
                
        if filter_list[4]:#pn
            pn = filter_list[4] + '%'
            #Part Number same filter as RO Edit, but PNM for the STM        
            where_clause += """ AND UPPER(PNM.PN) LIKE UPPER('%s')"""%pn
            
        if filter_list[5]:#description
            desc = filter_list[5] + '%'
            #Part description        
            where_clause += """ AND UPPER(PNM.DESCRIPTION) LIKE UPPER('%s')"""%desc
            
        if filter_list[6]:#ship_via
            ship_via = filter_list[6]
            where_clause += """ AND SVC.SHIP_VIA_CODE = '%s'"""%ship_via
            
        if filter_list[8]:#location
            location = filter_list[8] + '%'
            where_clause += """ AND UPPER(LOC.LOCATION_CODE) LIKE UPPER('%s')"""%location
            
        if filter_list[9]:#whs
            whs = filter_list[9] + '%'     
            where_clause += """ AND UPPER(WHS.WAREHOUSE_CODE) LIKE UPPER('%s')"""%whs
            
        if filter_list[10]:#user
            if filter_list[10] == 'unassigned':
                where_clause += " AND SYSUR.USER_NAME IS NULL"
            else:                
                user = filter_list[10] + '%'
                where_clause += " AND UPPER(SYSUR.USER_NAME) LIKE UPPER('%s')"%user
                
        if filter_list[7]:#priority
            priority = filter_list[7] + '%'
            where_clause += " AND UPPER(SYSUR.USER_NAME) LIKE UPPER('%s')"%priority

    query = """SELECT DISTINCT SOH.SO_NUMBER AS ORDER_NUM, SOD.DUE_DATE AS DUE_DATE, SMS.STATUS_CODE, 
        SMH.SM_NUMBER, STR.QTY_RESERVED, STR.DATE_SCAN, PNM.PN, 
        PNM.DESCRIPTION, CMP.COMPANY_NAME, SYSUR.USER_NAME AS USER_NAME, 
        STM.STOCK_LINE, STM.STM_AUTO_KEY, STM.SERIAL_NUMBER, 
        LOC.LOCATION_CODE AS LOC, WHS.WAREHOUSE_CODE AS WHS, STR.STR_AUTO_KEY, SOH.PRIORITY,
        UDL.UDL_CODE, TO_CHAR(SMD.NOTES)        

        FROM SO_DETAIL SOD

        JOIN SO_HEADER SOH ON SOH.SOH_AUTO_KEY = SOD.SOH_AUTO_KEY
        JOIN STOCK_RESERVATIONS STR ON SOD.SOD_AUTO_KEY = STR.SOD_AUTO_KEY
        JOIN SM_DETAIL SMD ON STR.SMD_AUTO_KEY = SMD.SMD_AUTO_KEY
        JOIN SM_HEADER SMH ON SMD.SMH_AUTO_KEY = SMH.SMH_AUTO_KEY
        JOIN SM_STATUS SMS ON SMH.SMS_AUTO_KEY = SMS.SMS_AUTO_KEY
        JOIN STOCK STM ON STR.STM_AUTO_KEY = STM.STM_AUTO_KEY
        JOIN LOCATION LOC ON STM.LOC_AUTO_KEY = LOC.LOC_AUTO_KEY
        JOIN WAREHOUSE WHS ON STM.WHS_AUTO_KEY = WHS.WHS_AUTO_KEY
        JOIN COMPANIES CMP ON SMH.CMP_AUTO_KEY = CMP.CMP_AUTO_KEY
        JOIN PARTS_MASTER PNM ON STM.PNM_AUTO_KEY = PNM.PNM_AUTO_KEY
        LEFT JOIN USER_DEFINED_LOOKUPS UDL ON UDL.UDL_AUTO_KEY = STM.IC_UDL_005
        LEFT JOIN SYS_USERS SYSUR ON STR.SYSUR_AUTO_KEY_SCAN = SYSUR.SYSUR_AUTO_KEY
        WHERE 
        %s
        
        UNION

        SELECT DISTINCT ROH.RO_NUMBER AS ORDER_NUM, SMH.SHIP_DATE AS DUE_DATE, SMS.STATUS_CODE, 
        SMH.SM_NUMBER, STR.QTY_RESERVED, STR.DATE_SCAN, PNM.PN, 
        PNM.DESCRIPTION, CMP.COMPANY_NAME, SYSUR.USER_NAME AS USER_NAME, 
        STM.STOCK_LINE, STM.STM_AUTO_KEY, STM.SERIAL_NUMBER, 
        LOC.LOCATION_CODE AS LOC, WHS.WAREHOUSE_CODE AS WHS, STR.STR_AUTO_KEY, 0,
        UDL.UDL_CODE, TO_CHAR(SMD.NOTES)

        FROM RO_DETAIL ROD
        
        JOIN RO_HEADER ROH ON ROH.ROH_AUTO_KEY = ROD.ROH_AUTO_KEY
        JOIN STOCK_RESERVATIONS STR ON ROD.ROD_AUTO_KEY = STR.ROD_AUTO_KEY
        JOIN SM_DETAIL SMD ON STR.SMD_AUTO_KEY = SMD.SMD_AUTO_KEY
        JOIN SM_HEADER SMH ON SMD.SMH_AUTO_KEY = SMH.SMH_AUTO_KEY
        JOIN SM_STATUS SMS ON SMH.SMS_AUTO_KEY = SMS.SMS_AUTO_KEY
        JOIN STOCK STM ON STR.STM_AUTO_KEY = STM.STM_AUTO_KEY
        JOIN LOCATION LOC ON STM.LOC_AUTO_KEY = LOC.LOC_AUTO_KEY
        JOIN WAREHOUSE WHS ON STM.WHS_AUTO_KEY = WHS.WHS_AUTO_KEY
        JOIN COMPANIES CMP ON SMH.CMP_AUTO_KEY = CMP.CMP_AUTO_KEY
        JOIN PARTS_MASTER PNM ON STM.PNM_AUTO_KEY = PNM.PNM_AUTO_KEY
        LEFT JOIN USER_DEFINED_LOOKUPS UDL ON UDL.UDL_AUTO_KEY = STM.IC_UDL_005
        LEFT JOIN SYS_USERS SYSUR ON STR.SYSUR_AUTO_KEY_SCAN = SYSUR.SYSUR_AUTO_KEY
        WHERE
        %s
        
        UNION

        SELECT DISTINCT POH.PO_NUMBER AS ORDER_NUM, SMH.SHIP_DATE AS DUE_DATE, SMS.STATUS_CODE, 
        SMH.SM_NUMBER, STR.QTY_RESERVED, STR.DATE_SCAN, PNM.PN, 
        PNM.DESCRIPTION, CMP.COMPANY_NAME, SYSUR.USER_NAME AS USER_NAME, 
        STM.STOCK_LINE, STM.STM_AUTO_KEY, STM.SERIAL_NUMBER, 
        LOC.LOCATION_CODE AS LOC, WHS.WAREHOUSE_CODE AS WHS, STR.STR_AUTO_KEY, 0,
        UDL.UDL_CODE, TO_CHAR(SMD.NOTES)

        FROM PO_DETAIL POD

        LEFT JOIN PO_HEADER POH ON POH.POH_AUTO_KEY = POD.POH_AUTO_KEY
        JOIN STOCK_RESERVATIONS STR ON POD.POD_AUTO_KEY = STR.POD_AUTO_KEY
        JOIN SM_DETAIL SMD ON STR.SMD_AUTO_KEY = SMD.SMD_AUTO_KEY
        JOIN SM_HEADER SMH ON SMD.SMH_AUTO_KEY = SMH.SMH_AUTO_KEY
        JOIN SM_STATUS SMS ON SMH.SMS_AUTO_KEY = SMS.SMS_AUTO_KEY
        JOIN STOCK STM ON STR.STM_AUTO_KEY = STM.STM_AUTO_KEY
        JOIN LOCATION LOC ON STM.LOC_AUTO_KEY = LOC.LOC_AUTO_KEY
        JOIN WAREHOUSE WHS ON STM.WHS_AUTO_KEY = WHS.WHS_AUTO_KEY
        JOIN COMPANIES CMP ON SMH.CMP_AUTO_KEY = CMP.CMP_AUTO_KEY
        JOIN PARTS_MASTER PNM ON STM.PNM_AUTO_KEY = PNM.PNM_AUTO_KEY
        LEFT JOIN USER_DEFINED_LOOKUPS UDL ON UDL.UDL_AUTO_KEY = STM.IC_UDL_005
        LEFT JOIN SYS_USERS SYSUR ON STR.SYSUR_AUTO_KEY_SCAN = SYSUR.SYSUR_AUTO_KEY
        WHERE
        %s
        ORDER BY USER_NAME, WHS, LOC, DUE_DATE ASC, ORDER_NUM
    """%(where_clause,where_clause,where_clause)
    recs = selection_dir(query,cr)   
    return recs
    
#=========================================RO MGMT======================================
@shared_task 
def get_users_nsync_beta(quapi_key,dj_user_id,is_dashboard=0,app=''):
    msg,user_data = '',[]
    error = ''
    query = "SELECT SYSUR_AUTO_KEY,USER_NAME,EMPLOYEE_CODE,USER_ID FROM SYS_USERS WHERE ARCHIVED='F'"
    from polls.models import QuantumUser,QueryApi as qa
    quapi = qa.objects.filter(id=quapi_key)
    quapi_id = quapi and quapi[0] or None  
    from polls.models import OracleConnection as oc
    orcl_conn = quapi_id and quapi_id.orcl_conn_id and oc.objects.filter(id=quapi_id.orcl_conn_id) or None
    orcl_conn = orcl_conn and orcl_conn[0] or None
    if orcl_conn:
        cr,con = orcl_connect(orcl_conn)
    if not (cr and con):
        return 'Cannot connect to Oracle',app
    recs = quapi_id and selection_dir(query,cr) or []
    del_users = dj_user_id and QuantumUser.objects.filter(quapi_id=quapi_key,dj_user_id=dj_user_id).delete() or None
    
    for rec in recs:
        user_data.append(QuantumUser(
                user_auto_key = rec[0],
                user_name = rec[1],
                employee_code = rec[2],
                user_id=rec[3],
                dj_user_id = dj_user_id,
                quapi_id = quapi_id,
                )
            )
    try:
        new_user = user_data and QuantumUser.objects.bulk_create(user_data) or None
    except Exception as exc:
        error = "\r\Django - Error with creating the status: %s"%exc 
    return error,app
    
@shared_task
def get_companies_n_sync(quapi_key,dj_user_id,is_vendor=False,is_customer=False,is_acc_co=False):
    error  = ''
    #get all vendors
    #get quapi object first
    where_cust,where_vend = '',''
    if is_vendor:
        where_vend = "VENDOR_FLAG = 'T' AND"
    if is_customer:
        where_cust = "CUSTOMER_FLAG = 'T' AND "   
    from polls.models import QueryApi as qa, Companies
    query = "SELECT COMPANY_NAME,CMP_AUTO_KEY FROM COMPANIES WHERE %s %s HISTORICAL = 'F'"%(where_vend,where_cust)
    quapi = qa.objects.filter(id=quapi_key)   
    quapi_id = quapi and quapi[0] or None
    recs = quapi_id and selection(query,quapi=quapi_id) or []
    if recs:   
        companies = Companies.objects.filter(quapi_id=quapi_id,dj_user_id=dj_user_id)
        del_vendors = companies and companies.delete() or None
    else:
        return 'Error with creating companies locally.',''    
    error = recs and create_bulk_companies(recs,quapi_id,dj_user_id,is_acc_co=is_acc_co,is_customer=is_customer,is_vendor=is_vendor) or ''
    return error

    
@shared_task 
def get_statuses_nsync_beta(quapi_key,dj_user_id,is_dashboard=0,app='',object_type=''):
    #TODO: must get the user that is currently logged in down in selection/insert/update methods 
    #user links us to the API creds we need to send an API request to run a query.
    #display WO Status Table in dropdown displaying WO_STATUS[‘DESCRIPTION’] 
    # and WO_STATUS[‘SEVERITY’], but only show Open WO_STATUS[‘STATUS_TYPE’])
    error,stat_data = '',[]
    from polls.models import StatusSelection as statsel,QueryApi
    quapi = QueryApi.objects.filter(id=quapi_key)
    quapi_id = quapi and quapi[0] or None  
    from polls.models import OracleConnection as oc
    orcl_conn = quapi_id and quapi_id.orcl_conn_id and oc.objects.filter(id=quapi_id.orcl_conn_id) or None
    orcl_conn = orcl_conn and orcl_conn[0] or None
    if orcl_conn:
        cr,con = orcl_connect(orcl_conn)
    if not (cr and con):
        return 'Cannot connect to Oracle',app

    if object_type and object_type == 'SO':
        query = "SELECT SOS_AUTO_KEY, SEQUENCE, 'SO - ' || DESCRIPTION FROM SO_STATUS WHERE STATUS_TYPE IN ('Open','Delay','Defer') ORDER BY SEQUENCE ASC"
    elif object_type and object_type == 'RO':
        query = "SELECT RST_AUTO_KEY, SEQUENCE, DESCRIPTION FROM RO_STATUS WHERE STATUS_TYPE IN ('Open','Delay','Defer') ORDER BY SEQUENCE ASC"
    else:
        query = "SELECT WOS_AUTO_KEY, SEVERITY, DESCRIPTION FROM WO_STATUS WHERE STATUS_TYPE IN ('Open','Delay','Defer') ORDER BY SEVERITY ASC"
        
    recs = selection_dir(query,cr)
    if app and app in ['ro-management','smd-management'] and object_type and object_type == 'SO':
        query = "SELECT WOS_AUTO_KEY, SEVERITY, 'WO - ' || DESCRIPTION FROM WO_STATUS WHERE STATUS_TYPE IN ('Open','Delay','Defer') ORDER BY SEVERITY ASC"
        recs += selection_dir(query,cr)
    del_stats = dj_user_id and statsel.objects.filter(quapi_id=quapi_key,is_dashboard=is_dashboard,dj_user_id=dj_user_id).delete() or None
    if is_dashboard == 1:
        wos_auto_key = 0
        severity = '0'
        name = 'PENDING'
        try:
            sstat = statsel.objects.create(quapi_id=quapi_id,dj_user_id = dj_user_id,is_dashboard = 1,wos_auto_key = wos_auto_key, severity = severity, name = name)
            sstat.save()
        except Exception as exc:
            error = "\r\nDjango - Error with creating the pending status: %s"%exc 
    for status in recs:
        wos_auto_key = status[0]
        severity = status[1]
        if object_type in ['RO','SO']:
            name = str(status[2])
        else:
            name = str(status[1]) + '-' + str(status[2])
        stat_data.append(statsel( 
            quapi_id=quapi_id,
            dj_user_id = dj_user_id,
            is_dashboard=is_dashboard,
            wos_auto_key = wos_auto_key,
            severity = severity,
            name = name,
            )
        )
    try:
        new_statii = stat_data and statsel.objects.bulk_create(stat_data) or None
    except Exception as exc:
        error = "\r\Django - Error with creating the statuses: %s"%exc 
    return error,app   
   
def format_start_date(start_date,new_format=None):
    date_formats = ["%m-%d-%y","%m-%d-%Y","%Y-%m-%d","%y-%m-%d","%m/%d/%y"]
    date_formats += ["%m/%d/%Y","%Y/%m/%d","%y/%m/%d",'%d %B %Y','%d %B %y']
    date_formats += ['%d %b %Y','%d %b %y','%d %B, %Y','%d %B, %y','%d %b, %Y','%d %b, %y']
    date_formats += ['%b %d %Y','%b %d %y','%B %d, %Y','%B %d, %y','%b %d, %Y','%b %d, %y']
    date_formats += ['%B %d %Y','%B %d %y']
    date = dateparser.parse(start_date, date_formats=date_formats)
    if not new_format:
        new_format = '%m/%d/%Y'
    start_date = date and datetime.strftime(date,new_format) or None
    return start_date
  
def create_ros_bulk(quapi,session_id,ro_recs):
    from polls.models import WOStatus
    ro_data,error,msg = [],'',''
    for rec in ro_recs:
        ro_data.append(WOStatus(
            quapi_id=quapi,
            session_id=session_id,
            is_repair_order=True,
            wo_number = rec[0],
            vendor = rec[1],
            item_number = rec[2],
            part_number = rec[3],
            description = rec[4],
            serial_number = rec[5],
            next_dlv_date = rec[6] and rec[6][:10] or None,
            condition_code = rec[7],
            total_cost = rec[21],
            rod_auto_key = rec[9], 
            parts_cost = rec[10],
            labor_cost = rec[11],
            misc_cost = rec[12],
            approved_date = rec[13] and rec[13][:10] or None,
            quoted_date = rec[14] and rec[14][:10] or None, 
            notes = rec[15], 
            airway_bill = rec[16],
            pnm_modify = rec[17], 
            stm_auto_key = rec[18], 
            qty_reserved = rec[19], 
            si_number = rec[22],
            cust_ref_number = rec[23],
            quantity = rec[24],
            entry_date = rec[25] and rec[25][:10] or None, 
            arrival_date = rec[26] and rec[26][:10] or None,#SMH.SHIP_DATE
            rack = rec[27],#SMH.AIRWAY_BILL
            po_number = rec[28],#SMH.SM_NUMBER
            time_status = rec[29],#SMS.STATUS_CODE
            loc_validated_date = rec[30] or None,#ROD.RO_UDF_001 (QUOTE DATE from ROD)
            customer = rec[31],#SOH.CMP_AUTO_KEY
            wo_type = rec[32],#SMD.ROUTE_CODE
            priority = rec[33],#ROD.QTY_RESERVED*SOD.UNIT_PRICE (SO Value)
            due_date = rec[34] and rec[34][:10] or None,#SOD.DUE_DATE
            )
        )
    try:
        WOStatus.objects.bulk_create(ro_data) or None
    except Exception as err:
        logger.error("Error with creation of repair order locally. Message: '%s'",err.args)           
    return error,msg
    
def get_ro_details(cr,ro_id_list='',\
    ro_number=None,wo_number=None,\
    vendor=None,part_number=None,\
    entry_date=None,rst_auto_key=None,
    uda_status=None):
    add_where = ''
    if ro_id_list:
        add_where += "AND ROD.ROD_AUTO_KEY IN %s"%ro_id_list
    if ro_number:
        add_where += "AND REGEXP_LIKE (ROH.RO_NUMBER, '%s', 'i') "%ro_number
    if wo_number:
        add_where += """AND ROD.WOO_AUTO_KEY IN 
        (SELECT WOO_AUTO_KEY FROM WO_OPERATION WHERE REGEXP_LIKE 
        (SI_NUMBER, '%s', 'i'))"""%wo_number
    if rst_auto_key:
        if rst_auto_key == '0':
            add_where += "AND ROH.RST_AUTO_KEY IS NULL"
        else:
            add_where += "AND ROH.RST_AUTO_KEY = '%s'"%rst_auto_key
    if vendor:
        add_where += "AND REGEXP_LIKE (C.COMPANY_NAME, '%s', 'i') "%vendor
    if part_number:
        add_where += "AND REGEXP_LIKE (P.PN, '%s', 'i') "%part_number
    if entry_date:
        add_where += "AND ROD.ENTRY_DATE >= TO_DATE('%s','mm-dd-yyyy') "%entry_date    
    #QTY_REPAIR = 1 <>  would be an open item in the RO_DETAIL table. 
    #We only really care if the ro detail is closed.
   
    if uda_status:
        add_where += """AND (ROH.ROH_AUTO_KEY IN (SELECT AUTO_KEY FROM
        UDA_CHECKED WHERE ATTRIBUTE_VALUE = '%s' AND UDA_AUTO_KEY=64))
        """%(uda_status)
        
    query = """SELECT DISTINCT ROH.RO_NUMBER,C.COMPANY_NAME,ROD.ITEM_NUMBER,
        P.PN,P.DESCRIPTION,S.SERIAL_NUMBER,ROD.NEXT_DELIVERY_DATE,
        PCC.CONDITION_CODE,ROH.TOTAL_COST,ROD.ROD_AUTO_KEY,ROD.PARTS_COST,
        ROD.LABOR_COST,ROD.MISC_COST,ROD.MSG_QUOTE_APPR_DATE,ROD.MSG_QUOTE_REC_DATE,
        TO_CHAR(ROD.REPAIR_NOTES),ROD.MSG_AIRWAY_BILL,PT.PN,S.STM_AUTO_KEY,SR.QTY_RESERVED,
        WO.SI_NUMBER,(ROD.PARTS_COST + ROD.LABOR_COST+ ROD.MISC_COST)*ROD.QTY_REPAIR,
        SOH.COMPANY_REF_NUMBER,SOH.SO_NUMBER,ROD.QTY_REPAIR,ROD.ENTRY_DATE,
        SMH.SHIP_DATE,
        SMH.AIRWAY_BILL,
        SMH.SM_NUMBER,
        SMS.STATUS_CODE,
        ROD.RO_UDF_001,
        SOC.COMPANY_NAME,
        SMD.ROUTE_CODE,
        ROD.QTY_RESERVED*SOD.UNIT_PRICE,
        SOD.DUE_DATE
        FROM RO_DETAIL ROD
        LEFT JOIN RO_HEADER ROH ON ROH.ROH_AUTO_KEY = ROD.ROH_AUTO_KEY
        LEFT JOIN COMPANIES C ON C.CMP_AUTO_KEY = ROH.CMP_AUTO_KEY
        LEFT JOIN PARTS_MASTER P ON P.PNM_AUTO_KEY = ROD.PNM_AUTO_KEY
        LEFT JOIN PART_CONDITION_CODES PCC ON PCC.PCC_AUTO_KEY = ROD.PCC_AUTO_KEY
        LEFT JOIN STOCK_RESERVATIONS SR ON SR.ROD_AUTO_KEY = ROD.ROD_AUTO_KEY
        LEFT JOIN STOCK S ON S.STM_AUTO_KEY = SR.STM_AUTO_KEY
        LEFT JOIN PARTS_MASTER PT ON PT.PNM_AUTO_KEY = ROD.PNM_MODIFY
        LEFT JOIN WO_OPERATION WO ON WO.WOO_AUTO_KEY = ROD.WOO_AUTO_KEY
        LEFT JOIN SO_DETAIL SOD ON SOD.SOD_AUTO_KEY = ROD.ROD_AUTO_KEY
        LEFT JOIN SO_HEADER SOH ON SOH.SOH_AUTO_KEY = SOD.SOH_AUTO_KEY 
        LEFT JOIN COMPANIES SOC ON SOC.CMP_AUTO_KEY = SOH.CMP_AUTO_KEY        
        LEFT JOIN SM_DETAIL SMD ON SMD.ROD_AUTO_KEY = ROD.ROD_AUTO_KEY
        LEFT JOIN SM_HEADER SMH ON SMH.SMH_AUTO_KEY = SMD.SMH_AUTO_KEY
        LEFT JOIN SM_STATUS SMS ON SMS.SMS_AUTO_KEY = SMH.SMH_AUTO_KEY        
        WHERE
        ((ROD.QTY_REPAIR <> ROD.QTY_REPAIRED + ROD.QTY_SCRAPPED) OR ROD.QTY_REPAIR = 0)
        AND S.HISTORICAL_FLAG = 'F'
        AND S.QTY_OH > 0
        AND SR.QTY_RESERVED > 0
        AND ROH.OPEN_FLAG = 'T'
        AND ROH.HISTORICAL_FLAG = 'F'
        AND ROH.NUMBER_OF_ITEMS > 0 
        """+ add_where

    recs = selection_dir(query,cr)
    return recs

@shared_task
def run_ro_mgmt(session_id,\
            wo_number=None,\
            part_number=None,\
            customer=None,\
            location=None,\
            condition_code=None,\
            socond_code=None,\
            user_id=None,\
            sysur_auto_key=None,\
            stock_label = None,\
            ctrl_id = None,\
            ctrl_number = None,\
            quapi_id = None,\
            clear_cart = None,\
            dj_user_id = None,\
            wos_auto_key = None,\
            stock_status = ''):
    from polls.models import WOStatus as wos_obj,QueryApi
    quapi = QueryApi.objects.filter(id=quapi_id)
    quapi = quapi and quapi[0] or None
    if not wo_number and not ctrl_id and stock_label:
        ctrl_number = stock_label[:6]
        ctrl_id = stock_label[7:]
    msg,loc,synch,stat,trail,upd = '','','','','',''
    error,field_changed,new_val,audit_ok,fields_changed = '','','','',False
    stock_recs,updates,updated_stock_recs,strecs = [],{},[],[]
    if not session_id:
        return 'Invalid session.  Please login and try again.',msg 
    #1. send params to stock query method, get_stock_recs()
    #2. take stock lines and bulk create locally using add_wo_record()
    #3. pass back success msg or any error messages   
    stock_recs = get_ro_stock(stock_status=stock_status,wos_auto_key=wos_auto_key,inexact=True,ctrl_id=ctrl_id,ctrl_number=ctrl_number,location=location,customer=customer,wo_number=wo_number,part_number=part_number,quapi=quapi,cond_code=condition_code,socond_code=socond_code)
    if stock_recs:
        del_rows = wos_obj.objects.filter(session_id=session_id).delete() or None
        error,msg = add_ro_stock(session_id,quapi,user_id=user_id,stock_recs=stock_recs)        
    elif not error:
        error = 'No records found.'   
    return error,msg

#0.number,1.due_date,2.PN,3.part_desc,4.serial,5. cond_code,
#6. status,7. loc,8. whs,9.'',10.stm_auto_key,11.owner,
#12.stock_line,13.woo_auto_key,     
def add_ro_stock(session_id,quapi,user_id='',stock_recs=[]):
    from polls.models import WOStatus
    ro_data,error,msg = [],'',''
    for rec in stock_recs:
        #if rec[15] and rec[15] > 0 and not rec[16]:
        ro_data.append(WOStatus(
            quapi_id=quapi,
            session_id=session_id,
            is_repair_order=True,
            wo_number = rec[0],
            due_date = rec[1] and rec[1][:10] or None,
            part_number = rec[2],
            description = rec[3],
            serial_number = rec[4],
            condition_code = rec[5],
            status = rec[6],
            location_code = rec[7],
            wh_code = rec[8],
            customer = rec[9],
            stm_auto_key = rec[10],   
            stock_owner = rec[11],
            stock_line = rec[12], 
            woo_auto_key = rec[13] or 0,
            vendor_key = rec[23] or rec[14] or 0,
            quantity = rec[15] or 0,
            pnm_auto_key = rec[17] or 0,
            vendor = rec[22] or '',
            cond_level_gsix = rec[18] or '', 
            rack = rec[19],
            sub_wo_gate = rec[20] or rec[21],            
            )
        )
    try:
        WOStatus.objects.bulk_create(ro_data) or None
    except Exception as err:
        logger.error("Error with creation of stock records locally. Message: '%s'",err.args)           
    return error,msg
    
def get_ro_stock(stock_status='',wos_auto_key=None,inexact=True,ctrl_id=None,ctrl_number=None,location=None,customer=None,wo_number=None,part_number=None,quapi=None,cond_code=None,socond_code=None):
    from polls.models import OracleConnection as oc
    orcl_conn = quapi and quapi.orcl_conn_id and oc.objects.filter(id=quapi.orcl_conn_id) or None
    orcl_conn = orcl_conn and orcl_conn[0] or None
    if orcl_conn:
        cr,con = orcl_connect(orcl_conn)
    if not (cr and con):
        return 'Cannot connect to Oracle',msg
    and_where = ''
    if ctrl_id and ctrl_number:
        and_where = "AND S.CTRL_ID = '%s' AND S.CTRL_NUMBER = '%s' "%(ctrl_id,ctrl_number)
    else:
        if wo_number:
            if not inexact:
                and_where = """AND (WO.SI_NUMBER = '%s' 
                OR WV.SI_NUMBER = '%s'
                OR W.SI_NUMBER = '%s'
                OR SOH.SO_NUMBER = '%s'
                OR STH.SO_NUMBER = '%s'
                ) 
                """%(wo_number,wo_number,wo_number,wo_number,wo_number)
            else:
                and_where = """AND (REGEXP_LIKE (WO.SI_NUMBER, '%s', 'i') 
                   OR REGEXP_LIKE (WV.SI_NUMBER, '%s', 'i') 
                   OR REGEXP_LIKE (W.SI_NUMBER, '%s', 'i') 
                   OR REGEXP_LIKE (SOH.SO_NUMBER, '%s', 'i')
                   OR REGEXP_LIKE (STH.SO_NUMBER, '%s', 'i'))
                   """%(wo_number,wo_number,wo_number,wo_number,wo_number)
        if cond_code:
            cond_reg = "REGEXP_LIKE (CONDITION_CODE, '%s', 'i')"%cond_code
            cond_code_where = "(SELECT PCC_AUTO_KEY FROM PART_CONDITION_CODES WHERE %s)"%cond_reg
            and_where += "AND (S.PCC_AUTO_KEY IN %s "%cond_code_where
            and_where += "OR ST.PCC_AUTO_KEY IN %s) "%cond_code_where
        if socond_code:
            socond_reg = "REGEXP_LIKE (CONDITION_CODE, '%s', 'i')"%socond_code
            socond_code_where = "(SELECT PCC_AUTO_KEY FROM PART_CONDITION_CODES WHERE %s)"%socond_reg
            and_where += "AND (SOD.PCC_AUTO_KEY IN %s "%socond_code_where
            and_where += "OR STD.PCC_AUTO_KEY IN %s) "%socond_code_where
        if customer:
            cust_where = "REGEXP_LIKE (COMPANY_NAME, '%s', 'i') "%customer
            cust_in = "SELECT CMP_AUTO_KEY FROM COMPANIES WHERE %s"%cust_where
            and_where += "AND (WO.CMP_AUTO_KEY IN (%s) OR WV.CMP_AUTO_KEY IN (%s) OR W.CMP_AUTO_KEY IN (%s)) "%(cust_in,cust_in,cust_in)
        if location:
            loc_reg = "REGEXP_LIKE (LOCATION_CODE, '%s', 'i') "%location
            loc_where = "(SELECT LOC_AUTO_KEY FROM LOCATION WHERE %s)"%loc_reg
            and_where += "AND (S.LOC_AUTO_KEY IN %s "%loc_where
            and_where += "OR ST.LOC_AUTO_KEY IN %s) "%loc_where
        if part_number:
            #pn_reg = "REGEXP_LIKE (PN, '%s', 'i') "%part_number
            #pn_where = "(SELECT PNM_AUTO_KEY FROM PARTS_MASTER WHERE %s)"%pn_reg
            #and_where += "AND (S.PNM_AUTO_KEY IN %s "%pn_where
            #and_where += "OR ST.PNM_AUTO_KEY IN %s) "%pn_where
            and_where += """AND (UPPER(P.PN) LIKE UPPER('%s%s') 
            OR UPPER(PT.PN) LIKE UPPER('%s%s')) """%(part_number,'%',part_number,'%')
        if wos_auto_key:
            if wos_auto_key == 'PENDING':
                and_where += """AND SOH.SOS_AUTO_KEY IS NULL 
                    AND STH.SOS_AUTO_KEY IS NULL AND (WO.WOS_AUTO_KEY IS NULL
                    AND W.WOS_AUTO_KEY IS NULL AND WV.WOS_AUTO_KEY IS NULL) """
            else:
                #rows - attribute name matches user selection
                and_where += """AND (RH.ROH_AUTO_KEY IN (SELECT AUTO_KEY FROM
                UDA_CHECKED WHERE ATTRIBUTE_VALUE = '%s' AND UDA_AUTO_KEY=64) OR
                RTH.ROH_AUTO_KEY IN (SELECT AUTO_KEY FROM
                UDA_CHECKED WHERE ATTRIBUTE_VALUE = '%s' AND UDA_AUTO_KEY=64))
                """%(wos_auto_key,wos_auto_key)
                #wos_sub = """(SELECT WOS_AUTO_KEY FROM WO_STATUS
                #    WHERE DESCRIPTION = '%s')"""%wos_auto_key[5:]
                #sos_sub = """(SELECT SOS_AUTO_KEY FROM SO_STATUS
                #    WHERE DESCRIPTION = '%s')"""%wos_auto_key[5:]
                """if wos_auto_key[:2] == 'SO':
                    and_where += """"""AND (SOH.SOS_AUTO_KEY = %s 
                    OR STH.SOS_AUTO_KEY = %s)""""""%(sos_sub,sos_sub)
                elif wos_auto_key[:2] == 'WO':
                    and_where += """"""AND
                    (WO.WOS_AUTO_KEY = %s 
                    OR W.WOS_AUTO_KEY = %s
                    OR WV.WOS_AUTO_KEY = %s) """"""%(wos_sub,wos_sub,wos_sub)"""
        if stock_status:
            #and_where += """AND (CASE WHEN S.STM_AUTO_KEY IS 
            #NOT NULL THEN S.IC_UDL_004 ELSE ST.IC_UDL_004 END) = %s"""%(stock_status)
            and_where += """AND (S.IC_UDL_004 = %s OR ST.IC_UDL_004 = %s) """%(stock_status,stock_status)
            
    order_by = " ORDER BY S.STM_AUTO_KEY DESC"
    query = """SELECT DISTINCT
        CASE WHEN SOH.SO_NUMBER IS NOT NULL THEN SOH.SO_NUMBER ELSE 
        (CASE WHEN STH.SO_NUMBER IS NOT NULL THEN STH.SO_NUMBER ELSE
        (CASE WHEN RH.RO_NUMBER IS NOT NULL THEN RH.RO_NUMBER ELSE
        (CASE WHEN RTH.RO_NUMBER IS NOT NULL THEN RTH.RO_NUMBER ELSE
        (CASE WHEN WO.SI_NUMBER IS NOT NULL THEN WO.SI_NUMBER ELSE 
        (CASE WHEN W.SI_NUMBER IS NOT NULL THEN W.SI_NUMBER ELSE
        (CASE WHEN WV.SI_NUMBER IS NOT NULL THEN WV.SI_NUMBER ELSE '' END)
        END) END) END) END) END) END,		
        WO.DUE_DATE,
        CASE WHEN PT.PN IS NOT NULL THEN PT.PN ELSE P.PN END,
        CASE WHEN PT.PN IS NOT NULL THEN PT.DESCRIPTION ELSE P.DESCRIPTION END,
         CASE WHEN ST.SERIAL_NUMBER IS NOT NULL THEN ST.SERIAL_NUMBER ELSE S.SERIAL_NUMBER END,
          CASE WHEN PTC.CONDITION_CODE IS NOT NULL THEN PTC.CONDITION_CODE ELSE PCC.CONDITION_CODE END,
           CASE WHEN SOS.SOS_AUTO_KEY IS NOT NULL THEN SOS.DESCRIPTION ELSE 
           CASE WHEN STS.SOS_AUTO_KEY IS NOT NULL THEN STS.DESCRIPTION ELSE
           CASE WHEN WOS.WOS_AUTO_KEY IS NOT NULL THEN WOS.DESCRIPTION ELSE
           CASE WHEN WS.WOS_AUTO_KEY IS NOT NULL THEN WS.DESCRIPTION ELSE
           CASE WHEN WVS.WOS_AUTO_KEY IS NOT NULL THEN WVS.DESCRIPTION END END END END END,
           CASE WHEN LT.LOCATION_CODE IS NOT NULL THEN LT.LOCATION_CODE ELSE L.LOCATION_CODE END,
           CASE WHEN WHT.WAREHOUSE_CODE IS NOT NULL THEN WHT.WAREHOUSE_CODE ELSE WH.WAREHOUSE_CODE END,
           CASE WHEN COH.COMPANY_NAME IS NOT NULL THEN COH.COMPANY_NAME ELSE 
           (CASE WHEN CTH.COMPANY_NAME IS NOT NULL THEN CTH.COMPANY_NAME ELSE
           (CASE WHEN C.COMPANY_NAME IS NOT NULL THEN C.COMPANY_NAME ELSE
           (CASE WHEN CO.COMPANY_NAME IS NOT NULL THEN CO.COMPANY_NAME ELSE
           (CASE WHEN CV.COMPANY_NAME IS NOT NULL THEN CV.COMPANY_NAME ELSE '' END) 
           END) END) END) END,
           CASE WHEN ST.STM_AUTO_KEY IS NOT NULL THEN ST.STM_AUTO_KEY ELSE S.STM_AUTO_KEY END,
           CASE WHEN ST.OWNER IS NOT NULL THEN ST.OWNER ELSE S.OWNER END,
           CASE WHEN ST.STOCK_LINE IS NOT NULL THEN ST.STOCK_LINE ELSE S.STOCK_LINE END,
           CASE WHEN WO.WOO_AUTO_KEY IS NOT NULL THEN WO.WOO_AUTO_KEY ELSE
           (CASE WHEN W.WOO_AUTO_KEY IS NULL THEN WV.WOO_AUTO_KEY ELSE 
           W.WOO_AUTO_KEY END) END,
           CASE WHEN CMTP.CMP_AUTO_KEY IS NOT NULL THEN CMTP.CMP_AUTO_KEY ELSE CMP.CMP_AUTO_KEY END,
           CASE WHEN ST.STM_AUTO_KEY IS NOT NULL THEN ST.QTY_OH ELSE S.QTY_OH END,
        CASE WHEN ST.STM_AUTO_KEY IS NOT NULL THEN STR.ROD_AUTO_KEY ELSE SR.ROD_AUTO_KEY END,
		CASE WHEN PT.PNM_AUTO_KEY IS NOT NULL THEN PT.PNM_AUTO_KEY ELSE P.PNM_AUTO_KEY END,
        CASE WHEN SOD.SOD_AUTO_KEY IS NOT NULL THEN PSD.CONDITION_CODE ELSE PSTD.CONDITION_CODE END,
        CASE WHEN ST.STM_AUTO_KEY IS NOT NULL THEN UDL.UDL_CODE 
        ELSE UDLT.UDL_CODE END,
        UDC.ATTRIBUTE_VALUE,
        UDCH.ATTRIBUTE_VALUE
        FROM STOCK S
        LEFT JOIN USER_DEFINED_LOOKUPS UDL ON UDL.UDL_AUTO_KEY = S.IC_UDL_004
        LEFT JOIN STOCK ST ON ST.STM_LOT = S.STM_AUTO_KEY
            LEFT JOIN (SELECT RD.PNM_AUTO_KEY,RH.CMP_AUTO_KEY,
                    ROW_NUMBER() OVER (PARTITION BY RD.PNM_AUTO_KEY ORDER BY RH.ENTRY_DATE DESC) RN
                FROM RO_DETAIL RD
                LEFT JOIN RO_HEADER RH
                    ON RH.ROH_AUTO_KEY = RD.ROH_AUTO_KEY) LASTCMP
                    ON LASTCMP.PNM_AUTO_KEY = S.PNM_AUTO_KEY
                    AND LASTCMP.RN = 1                
                LEFT JOIN COMPANIES CMP
                    ON CMP.CMP_AUTO_KEY = LASTCMP.CMP_AUTO_KEY
                LEFT JOIN (SELECT RTD.PNM_AUTO_KEY,RTH.CMP_AUTO_KEY,
                    ROW_NUMBER() OVER (PARTITION BY RTD.PNM_AUTO_KEY ORDER BY RTH.ENTRY_DATE DESC) RN
                FROM RO_DETAIL RTD
                LEFT JOIN RO_HEADER RTH
                    ON RTH.ROH_AUTO_KEY = RTD.ROH_AUTO_KEY) LASTCMTP
                    ON LASTCMTP.PNM_AUTO_KEY = ST.PNM_AUTO_KEY
                    AND LASTCMTP.RN = 1                
                LEFT JOIN COMPANIES CMTP
                    ON CMTP.CMP_AUTO_KEY = LASTCMTP.CMP_AUTO_KEY      
		LEFT JOIN USER_DEFINED_LOOKUPS UDLT ON UDLT.UDL_AUTO_KEY = ST.IC_UDL_004					
        LEFT JOIN WAREHOUSE WH ON WH.WHS_AUTO_KEY = S.WHS_AUTO_KEY
        LEFT JOIN LOCATION L ON L.LOC_AUTO_KEY = S.LOC_AUTO_KEY
        LEFT JOIN PARTS_MASTER P ON P.PNM_AUTO_KEY = S.PNM_AUTO_KEY
        LEFT JOIN PART_CONDITION_CODES PCC ON PCC.PCC_AUTO_KEY = S.PCC_AUTO_KEY
        LEFT JOIN STOCK_RESERVATIONS SR ON SR.STM_AUTO_KEY = S.STM_AUTO_KEY
        LEFT JOIN WO_OPERATION WO ON WO.WOO_AUTO_KEY = SR.WOO_AUTO_KEY
        LEFT JOIN WO_STATUS WOS ON WOS.WOS_AUTO_KEY = WO.WOS_AUTO_KEY
        LEFT JOIN COMPANIES CO ON CO.CMP_AUTO_KEY = WO.CMP_AUTO_KEY
        LEFT JOIN WO_BOM WB ON WB.WOB_AUTO_KEY = SR.WOB_AUTO_KEY
        LEFT JOIN WO_OPERATION W ON W.WOO_AUTO_KEY = WB.WOO_AUTO_KEY
        LEFT JOIN WO_STATUS WS ON WS.WOS_AUTO_KEY = W.WOS_AUTO_KEY
        LEFT JOIN SO_DETAIL SOD ON SOD.SOD_AUTO_KEY = SR.SOD_AUTO_KEY
        LEFT JOIN PART_CONDITION_CODES PSD ON PSD.PCC_AUTO_KEY = SOD.PCC_AUTO_KEY
        LEFT JOIN SO_HEADER SOH ON SOH.SOH_AUTO_KEY = SOD.SOH_AUTO_KEY
        LEFT JOIN COMPANIES COH ON COH.CMP_AUTO_KEY = SOH.CMP_AUTO_KEY
        LEFT JOIN SO_STATUS SOS ON SOS.SOS_AUTO_KEY = SOH.SOS_AUTO_KEY       
        LEFT JOIN COMPANIES C ON C.CMP_AUTO_KEY = W.CMP_AUTO_KEY
        LEFT JOIN VIEW_SPS_WO_OPERATION VW ON VW.STM_AUTO_KEY = S.STM_AUTO_KEY
        LEFT JOIN WO_OPERATION WV ON WV.WOO_AUTO_KEY = VW.WOO_AUTO_KEY
        LEFT JOIN WO_STATUS WVS ON WVS.WOS_AUTO_KEY = WV.WOS_AUTO_KEY        
        LEFT JOIN COMPANIES CV ON CV.CMP_AUTO_KEY = WV.CMP_AUTO_KEY
        LEFT JOIN LOCATION LT ON LT.LOC_AUTO_KEY = ST.LOC_AUTO_KEY
        LEFT JOIN WAREHOUSE WHT ON WHT.WHS_AUTO_KEY = ST.WHS_AUTO_KEY
        LEFT JOIN PARTS_MASTER PT ON PT.PNM_AUTO_KEY = ST.PNM_AUTO_KEY
        LEFT JOIN PART_CONDITION_CODES PTC ON PTC.PCC_AUTO_KEY = ST.PCC_AUTO_KEY
        LEFT JOIN STOCK_RESERVATIONS STR ON STR.STM_AUTO_KEY = ST.STM_AUTO_KEY
        LEFT JOIN SO_DETAIL STD ON STD.SOD_AUTO_KEY = STR.SOD_AUTO_KEY
        LEFT JOIN PART_CONDITION_CODES PSTD ON PSTD.PCC_AUTO_KEY = STD.PCC_AUTO_KEY
        LEFT JOIN SO_HEADER STH ON STH.SOH_AUTO_KEY = STD.SOH_AUTO_KEY
        LEFT JOIN COMPANIES CTH ON CTH.CMP_AUTO_KEY = STH.CMP_AUTO_KEY
        LEFT JOIN SO_STATUS STS ON STS.SOS_AUTO_KEY = STH.SOS_AUTO_KEY
        LEFT JOIN RO_DETAIL RD ON RD.ROD_AUTO_KEY = S.STM_AUTO_KEY
        LEFT JOIN RO_HEADER RH ON RH.ROH_AUTO_KEY = RD.ROH_AUTO_KEY
        LEFT JOIN RO_DETAIL RTD ON RTD.ROD_AUTO_KEY = ST.ROD_AUTO_KEY
        LEFT JOIN RO_HEADER RTH ON RTH.ROH_AUTO_KEY = RTD.ROH_AUTO_KEY
        LEFT JOIN UDA_CHECKED UDC ON UDC.AUTO_KEY = RH.ROH_AUTO_KEY
        LEFT JOIN UDA_CHECKED UDCH ON UDCH.AUTO_KEY = RTH.ROH_AUTO_KEY  
        WHERE S.QTY_OH > 0 %s
        AND (CASE WHEN SOD.SOD_AUTO_KEY IS NOT NULL THEN 
        (CASE WHEN S.PCC_AUTO_KEY <> SOD.PCC_AUTO_KEY THEN 1 ELSE
        0 END) ELSE (CASE WHEN STD.SOD_AUTO_KEY IS NOT NULL THEN 
        (CASE WHEN ST.PCC_AUTO_KEY <> STD.PCC_AUTO_KEY THEN 1 ELSE 
        0 END) ELSE 1 END) END)=1
        AND (CASE WHEN ST.STR_AUTO_KEY IS NOT NULL THEN 
        (CASE WHEN ST.QTY_RESERVED > 0 THEN 1 ELSE 0 END) ELSE
        (CASE WHEN STR.STR_AUTO_KEY IS NOT NULL THEN 
        (CASE WHEN STR.QTY_RESERVED > 0 THEN 1 ELSE 0 END) ELSE 1 END) END)=1
        AND (CASE WHEN ST.STR_AUTO_KEY IS NOT NULL THEN 
        (CASE WHEN ST.ROD_AUTO_KEY IS NULL THEN 1 ELSE 0 END) ELSE
        (CASE WHEN STR.STR_AUTO_KEY IS NOT NULL THEN 
        (CASE WHEN STR.ROD_AUTO_KEY IS NULL THEN 1 ELSE 0 END) ELSE 1 END) END)=1       
    """%(and_where)
    recs = selection_dir(query,cr)
    counter = 0
    stm_list = []
    ro_recs = []
    
    for stock in recs:
        pnm_auto_key = stock[17]
        stm_auto_key = stock[10]
        stock += ['','']
        
        if stm_auto_key in stm_list: 
            counter+=1        
            continue
            
        if part_number:
            if stock[2] != part_number:
                query = """SELECT PNM_AUTO_KEY,
                PN,DESCRIPTION FROM PARTS_MASTER
                WHERE UPPER(PN) = '%s'
                """%part_number
                part = selection_dir(query,cr)
                part = part and part[0]
                if part:
                    pnm_auto_key = part[0]
                    stock[2] = part[1]
                    stock[3] = part[2]
                    stock[17] = pnm_auto_key
                
        stm_list.append(stm_auto_key)
        
        if pnm_auto_key:
            query="""SELECT CMP.COMPANY_NAME,CMP.CMP_AUTO_KEY            
                FROM COMPANIES CMP,
                RO_HEADER ROH, 
                RO_DETAIL ROD, 
                PARTS_MASTER PNM
                WHERE CMP.CMP_AUTO_KEY = ROH.CMP_AUTO_KEY 
                AND ROH.ROH_AUTO_KEY = ROD.ROH_AUTO_KEY 
                AND ROD.PNM_AUTO_KEY = PNM.PNM_AUTO_KEY 
                AND PNM.PNM_AUTO_KEY = %s 
                ORDER BY ROD.ROD_AUTO_KEY DESC"""%pnm_auto_key
                
            last_vendor = selection_dir(query,cr)
            last_vendor = last_vendor and last_vendor[0]           
            #last_vendor = last_vendor and last_vendor[0] or ''
            stock[22] = last_vendor and last_vendor[0] or ''
            stock[23] = last_vendor and last_vendor[1] or 0
            
        ro_recs.append(stock)
        counter+=1
        
    return ro_recs
    
def get_stock_ros(cr,stm_auto_key=None,ro_number=None,stm_keys=[]):
    recs = []
    if stm_auto_key:
        where = 'S.STM_AUTO_KEY = %s'%stm_auto_key
        query = form_stock_ro(where)
        recs += selection_dir(query,cr)
    for skey in stm_keys:
        where = 'S.STM_AUTO_KEY IN %s'%skey        
        query = form_stock_ro(where)
        recs += selection_dir(query,cr)
    return recs
    
def form_stock_ro(where): 
    trial_left_joins = """
    LEFT JOIN (SELECT ROW_NUMBER() OVER (PARTITION BY ROD.PNM_AUTO_KEY ORDER BY ROH.ENTRY_DATE DESC) RON,
        ROD.PNM_AUTO_KEY,ROH.CMP_AUTO_KEY FROM RO_HEADER ROH 
        LEFT JOIN RO_DETAIL ROD
        ON ROH.ROH_AUTO_KEY = ROD.ROH_AUTO_KEY) LAST_V
        ON LAST_V.PNM_AUTO_KEY = S.PNM_AUTO_KEY
        AND LAST_V.RON = 1
        LEFT JOIN COMPANIES C ON LAST_V.CMP_AUTO_KEY = C.CMP_AUTO_KEY
        LEFT JOIN (
            SELECT SR.STM_AUTO_KEY FROM STOCK_RESERVATIONS SR
            WHERE ROD_AUTO_KEY IS NULL AND QTY_RESERVED > 0
            GROUP BY SR.STM_AUTO_KEY) STRO
            ON STRO.STM_AUTO_KEY = S.STM_AUTO_KEY
        LEFT JOIN RO_DETAIL ROD ON ROD.ROD_AUTO_KEY = S.ROD_AUTO_KEY
        LEFT JOIN RO_HEADER ROH ON ROH.ROH_AUTO_KEY = ROD.ROH_AUTO_KEY
    """    
    left_joins="""left join         ( select          rd.pnm_auto_key, rh.cmp_auto_key,
                                    row_number() over (partition by rd.pnm_auto_key order by rh.entry_date desc) rn 
                    from            ro_detail rd 
                    left join       ro_header rh 
                    on              rh.roh_auto_key = rd.roh_auto_key
                  ) lastcmp
                on                lastcmp.pnm_auto_key = s.pnm_auto_key
                                  and lastcmp.rn = 1                    
                left join	        companies cmp 
                on                cmp.cmp_auto_key = lastcmp.cmp_auto_key 

                left join         ( select          r.stm_auto_key
                                    from            stock_reservations r
                                    where           rod_auto_key is not null
                                                    and qty_reserved > 0
                                    group by        r.stm_auto_key
                                  ) resro
                on                resro.stm_auto_key = s.stm_auto_key

                left join         ro_detail rd 
                on                rd.rod_auto_key = s.rod_auto_key
                left join         ro_header rh 
                on                rh.roh_auto_key = rd.roh_auto_key
    """
    query = """SELECT DISTINCT
        S.PNM_AUTO_KEY,
        S.PCC_AUTO_KEY,
        S.CMP_AUTO_KEY,
        S.QTY_OH,
        S.SERIAL_NUMBER,
        S.CMP_AUTO_KEY,
        CP.CMP_AUTO_KEY,
        S.CMP_AUTO_KEY,
        S.STM_AUTO_KEY,
        SR.STR_AUTO_KEY,
        S.DPT_AUTO_KEY,
        S.SYSUR_AUTO_KEY,
        S.SYSCM_AUTO_KEY,
        CASE WHEN WH.SHIP_ADDRESS1 IS NOT NULL THEN WH.SHIP_ADDRESS1 ELSE 
            (CASE WHEN DP.ADDRESS_LINE1 IS NOT NULL THEN DP.ADDRESS_LINE1 ELSE
                SCM.SHIP_ADDRESS1 END) END,
        CASE WHEN WH.SHIP_ADDRESS1 IS NOT NULL THEN WH.SHIP_ADDRESS1 ELSE 
            (CASE WHEN DP.ADDRESS_LINE1 IS NOT NULL THEN DP.ADDRESS_LINE2 ELSE
                SCM.SHIP_ADDRESS2 END) END,
        CASE WHEN WH.SHIP_ADDRESS1 IS NOT NULL THEN WH.SHIP_ADDRESS3 ELSE 
            (CASE WHEN DP.ADDRESS_LINE1 IS NULL THEN SCM.SHIP_ADDRESS3 END) END,
        CASE WHEN WH.SHIP_ADDRESS1 IS NOT NULL THEN WH.SHIP_ADDRESS4 ELSE 
            (CASE WHEN DP.ADDRESS_LINE1 IS NOT NULL THEN DP.CITY ||','|| DP.STATE ||','|| DP.ZIP_CODE ELSE
                 SCM.SHIP_CITY ||','|| SCM.SHIP_STATE ||','|| SCM.SHIP_ZIP_CODE END) END,
        CASE WHEN WH.SHIP_ADDRESS1 IS NOT NULL THEN WH.SHIP_ADDRESS5 ELSE SCM.SHIP_COUNTRY END,
        CASE WHEN WH.SHIP_ADDRESS1 IS NOT NULL THEN WH.SHIP_NAME ELSE 
            (CASE WHEN DP.ADDRESS_LINE1 IS NOT NULL THEN DP.DEPT_NAME ELSE
             SCM.SHIP_NAME END) END,
        CP.SHIP_ADDRESS1,
        CP.SHIP_ADDRESS2,
        CP.SHIP_ADDRESS3,
        CP.SHIP_CITY ||','|| CP.SHIP_STATE ||','|| CP.SHIP_ZIP_CODE,
        CP.SHIP_COUNTRY END,
        CP.SHIP_NAME END,
        CASE WHEN SR.WOB_AUTO_KEY IS NULL THEN VW.WOB_AUTO_KEY ELSE SR.WOB_AUTO_KEY END,
        CASE WHEN SR.SOD_AUTO_KEY IS NULL THEN VW.SOD_AUTO_KEY ELSE SR.SOD_AUTO_KEY END,
        CASE WHEN SR.WOO_AUTO_KEY IS NULL THEN VW.WOO_AUTO_KEY ELSE SR.WOO_AUTO_KEY END,
        TO_CHAR(S.NOTES)
        FROM STOCK S
        LEFT JOIN STOCK_RESERVATIONS SR ON SR.STM_AUTO_KEY = S.STM_AUTO_KEY
        LEFT JOIN COMPANIES CP ON CP.CMP_AUTO_KEY = S.CMP_AUTO_KEY
        LEFT JOIN SYS_COMPANIES SCM ON SCM.SYSCM_AUTO_KEY = S.SYSCM_AUTO_KEY
        LEFT JOIN DEPARTMENT DP ON DP.DPT_AUTO_KEY = S.DPT_AUTO_KEY
        LEFT JOIN WAREHOUSE WH ON WH.WHS_AUTO_KEY = S.WHS_AUTO_KEY
        LEFT JOIN VIEW_SPS_WO_OPERATION VW ON VW.STM_AUTO_KEY = S.STM_AUTO_KEY
        WHERE %s"""%(where)
    return query  

def insert_ro_header(cr,sysur_auto_key,vendor_key,right_now,srecs):
    ship_address1 = ''
    ship_address2 = ''
    ship_address3 = ''
    ship_address4 = ''
    ship_address5 = ''
    ship_name = '' 
    v_address1 = ''
    v_address2 = ''
    # v_address3 = ''
    v_address4 = ''
    v_address5 = ''
    v_name = '' 
    """GET THE SYS_COMPANIES SHIPPING ADDRESS"""
    query="""SELECT SYS.ADDRESS1, SYS.ADDRESS2, 
    SYS.ADDRESS3, SYS.CITY, SYS.STATE, SYS.ZIP_CODE,
    SYS.COMPANY_NAME FROM SYS_COMPANIES SYS
    WHERE SYS.SYSCM_AUTO_KEY = '%s'   
    """%srecs[12]
    rec = selection_dir(query,cr)        
    ship_add = rec and rec[0]
    if ship_add:
        ship_address1 = ship_add[0] or ''
        ship_address2 = ship_add[1] or ''
        ship_address3 = ship_add[2] or ''
        ship_address4 = ship_add[3] + ', ' + ship_add[4]
        ship_address4 += ' ' + ship_add[5]
        ship_address5 = ''
        ship_name = ship_add[6]
    """GET THE VENDOR ADDRESS"""
    query="""SELECT C.ADDRESS1, C.ADDRESS2, 
    C.ADDRESS3, C.CITY, C.STATE, C.ZIP_CODE,
    C.COMPANY_NAME FROM COMPANIES C
    WHERE C.CMP_AUTO_KEY = '%s'
    """%vendor_key
    rec = selection_dir(query,cr)
    v_add = rec and rec[0]  
    if v_add:
        v_address1 = v_add[0] or ''
        v_address2 = v_add[1] or ''
        v_address3 = v_add[2] or ''
        v_address4 = v_add[3] + ', ' + v_add[4]
        v_address4 += ' ' + v_add[5]
        v_address5 = ''
        v_name = v_add[6]
    
    error = ''
    rohs_created = 0
    #query = "SELECT RO_NUMBER FROM RO_HEADER ORDER BY ROH_AUTO_KEY DESC FETCH NEXT 1 ROWS ONLY"            
    #ro_num_recs = selection(query,cr=cr)
    #ro_number = ro_num_recs and ro_num_recs[0] and ro_num_recs[0][0] or ''
    #ro_number = ro_number and int(ro_number.split('-')[0]) or None
    #ro_number = ro_number and ro_number + 1 or 'None'
    #q1 = "SELECT RO_NUMBER FROM RO_HEADER ORDER BY ROH_AUTO_KEY DESC FETCH NEXT 1 ROWS ONLY"
    #ro_number = (TO_NUMBER(%s) + 1)%q1
    num_query = """select sl.last_number + 1, sl.sysnl_auto_key, sl.number_prefix
      from            sys_number_log sl
      left join       sys_number_log_codes lc
      on              lc.sysnlc_auto_key = sl.sysnlc_auto_key
      where           (lc.log_type_code = 'RO')"""
    sysnum = selection_dir(num_query,cr)    
    sysnum = sysnum and sysnum[0] or ''
    last_num_mas1 = sysnum and sysnum[0] or ''
    sysnl_auto_key = sysnum and sysnum[1] or 0
    number_prefix = sysnum and sysnum[2] or 'RO'
    if last_num_mas1:
        #adding new fields into insert 
        query = """INSERT INTO RO_HEADER (RO_NUMBER, CMP_AUTO_KEY,
          SYSUR_AUTO_KEY,ENTRY_DATE, SYSCM_AUTO_KEY, DPT_AUTO_KEY, OPEN_FLAG,
          ship_address1, ship_address2, ship_address3, ship_address4,
          ship_address5, ship_name,
          vendor_address1, vendor_address2, vendor_address3, 
          vendor_address4, vendor_address5, vendor_name) 
          VALUES('%s','%s','%s',TO_DATE('%s','MM-DD-YYYY'),'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
          """%(str(number_prefix) + str(last_num_mas1),vendor_key,sysur_auto_key,right_now[:10],
          srecs[12],srecs[10],'T',ship_address1,ship_address2,ship_address3,ship_address4,
          ship_address5,ship_name,v_address1,v_address2,v_address3,v_address4,v_address5,v_name)
        try:
            insertion_dir(query,cr)
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            error = error.message
            logger.error("Error with inserting new RO: '%s'",error)               
    if (not error or error == '{"recs": ""}') and sysnl_auto_key:
        query ="""UPDATE sys_number_log snl 
          SET snl.last_number = '%s'
          WHERE snl.sysnl_auto_key = '%s'"""%(last_num_mas1,sysnl_auto_key)
        rohs_created = str(number_prefix) + str(last_num_mas1)
        error = updation_dir(query,cr)       
    return error,rohs_created
    
def insert_ro_detail(cr,stock_recs,right_now,sysur_auto_key,roh_auto_key=None): 
    """we do have an issue with RO Management though. When in stock search and creating an ro with a stm, 
        it creates an RO Detail with QTY_RESERVED = 0, this might be causing the receiving issues i'm having. 
        ROD['QTY_RESERVED'] = WOB/WOO/SOD['QTY_RESERVED'] where the STM came from or if STM['QTY_RESERVED'] = 0 
        THEN ROD['QTY_RESERVED'] = STM['QTY_AVAILABLE']
    """
    qty_reserved = 0
    query = stock_recs and """INSERT INTO RO_DETAIL 
    (PNM_AUTO_KEY,PCC_AUTO_KEY,ROH_AUTO_KEY,SYSUR_AUTO_KEY,
    ENTRY_DATE,QTY_REPAIR,QTY_REPAIRED,SERIAL_NUMBER,
    RO_TYPE,WOB_AUTO_KEY,SOD_AUTO_KEY,WOO_AUTO_KEY,QTY_RESERVED,
    REPAIR_NOTES) 
    VALUES('%s','%s','%s','%s',TO_DATE('%s','MM-DD-YYYY'),%s,0,'%s','Overhaul','%s','%s','%s','%s','%s')
    """%(stock_recs[0] or '',stock_recs[1] or '',roh_auto_key or stock_recs[2],sysur_auto_key or '',right_now[:10],stock_recs[3],stock_recs[4],stock_recs[25],stock_recs[26],stock_recs[27],qty_reserved,stock_recs[28])
    rods_created = 0
    error = insertion_dir(query,cr) 
    if error == '{"recs": ""}' or error == '':
        error = ''
        rods_created += 1
    #else:
    #   'No stock records to add.  Check your selection.'
    #now we must add the rod_auto_key to the reservation
    """ S.PNM_AUTO_KEY,0
        S.PCC_AUTO_KEY,1
        S.CMP_AUTO_KEY,2
        S.QTY_OH,3
        S.SERIAL_NUMBER,4
        S.CMP_AUTO_KEY,5
        CP.CMP_AUTO_KEY,6
        S.CMP_AUTO_KEY,7
        S.STM_AUTO_KEY,8
        SR.STR_AUTO_KEY,9
        S.DPT_AUTO_KEY,10
        S.SYSUR_AUTO_KEY,11
        S.SYSCM_AUTO_KEY,12"""
        
    query = """UPDATE STOCK SET IC_UDL_004 = NULL
        WHERE STM_AUTO_KEY = %s"""%stock_recs[8]
    error = updation_dir(query,cr)
    query = "select qty_reserved,qty_available,qty_oh from stock where stm_auto_key = '%s'"%stock_recs[8]
    stock_q = selection_dir(query,cr)
    qty_reserved = stock_q and stock_q[0] and stock_q[0][0] or 0
    if qty_reserved == 0:
        qty_reserved = stock_q and stock_q[0] and stock_q[0][1] or 0
    if qty_reserved == 0:
        qty_reserved = stock_q and stock_q[0] and stock_q[0][2] or 0
    str_auto_key = stock_recs and stock_recs[9] or None 
    query = """SELECT ROD_AUTO_KEY FROM RO_DETAIL WHERE  
        ROH_AUTO_KEY = %s AND SYSUR_AUTO_KEY = %s AND
        ENTRY_DATE = TO_DATE('%s','MM-DD-YYYY') ORDER BY ROD_AUTO_KEY DESC"""%(roh_auto_key,sysur_auto_key,right_now)
    rod = selection_dir(query,cr)
    rod_auto_key = rod and rod[0] and rod[0][0] or None
    if str_auto_key and qty_reserved > 0:
        query = "DELETE FROM STOCK_RESERVATIONS WHERE STR_AUTO_KEY = %s"%str_auto_key
        #query = "UPDATE STOCK_RESERVATIONS SET ROD_AUTO_KEY = %s WHERE STR_AUTO_KEY = %s"%(sub_query,str_auto_key)
        res = updation_dir(query,cr)           
    #else:
        #rod_new = "SELECT ROD_AUTO_KEY FROM RO_DETAIL WHERE SYSUR_AUTO_KEY"
    if rod_auto_key:
        new_res = """INSERT INTO STOCK_RESERVATIONS (STR_AUTO_KEY,STM_AUTO_KEY,ROD_AUTO_KEY,QTY_RESERVED) VALUES (G_STR_AUTO_KEY.NEXTVAL,%s,%s,%s)"""%(stock_recs[8],rod_auto_key,stock_recs[3])
        newrs = insertion_dir(new_res,cr)
        query = "UPDATE RO_DETAIL SET QTY_RESERVED = %s WHERE ROD_AUTO_KEY = %s"%(qty_reserved,rod_auto_key)
        res = updation_dir(query,cr)
    return rods_created
    
def get_ro_vendor(srec,session_id,wos_obj):
    moves = wos_obj.objects.filter(session_id=session_id,stm_auto_key=srec[8])
    last_vendor_key = None
    for move in moves:
        if move.vendor_key:
            last_vendor_key = move.vendor_key
            break
    return last_vendor_key
    
def get_new_roh(cr,vendor_key,right_now,sysur_auto_key=''):
    sysur_auto_key = sysur_auto_key and 'AND SYSUR_AUTO_KEY = %s '%sysur_auto_key or '' 
    entry_date = ''   
    if sysur_auto_key:
        entry_date = ''
    else:
        entry_date = "AND ENTRY_DATE=TO_DATE('%s','MM-DD-YYYY')"%right_now  
    query = """SELECT ROH_AUTO_KEY FROM RO_HEADER WHERE 
        CMP_AUTO_KEY = %s 
        %s
        %s
        ORDER BY ROH_AUTO_KEY 
        DESC"""%(vendor_key,entry_date,sysur_auto_key)
    roh = selection_dir(query,cr)
    roh_auto_key = roh and roh[0] or None
    roh_auto_key = roh_auto_key and roh_auto_key[0] or None
    return roh_auto_key
    
@shared_task
def add_new_ro(quapi_id,session_id,sysur_auto_key,ro_number=None,stm_keys=[],vendor=None,last_vendor=False,woo_keys=[]):
    error,msg,rods_created = '','',0
    from polls.models import WOStatus as wos_obj,QueryApi,MLApps as maps,QuantumUser as qu
    quapi = QueryApi.objects.filter(id=quapi_id)
    quapi = quapi and quapi[0] or None
    #1. If not vendor, then get vendor from roh.last_vendor field
    #2. If vendor, then add the new ROH, RO_DETAIL
    #3. If ro_number entered in text field by user, 
    #then we look it up and add (create RO_DETAIL lines) under the RO_HEADER
    #Any selected stock lines get added to the new RO as detail lines.s
    from polls.models import OracleConnection as oc
    orcl_conn = quapi and quapi.orcl_conn_id and oc.objects.filter(id=quapi.orcl_conn_id) or None
    orcl_conn = orcl_conn and orcl_conn[0] or None 
    if orcl_conn:
        cr,con = orcl_connect(orcl_conn)
    if not (cr and con):
        return 'Cannot connect to Oracle.'      
    if stm_keys:
        stm_key_list = construct_akl(stm_keys)
        right_now = datetime.now()
        right_now = right_now.strftime('%m-%d-%Y') 
        if not vendor and last_vendor:
            #1. get last vendor from stock lines
            #2. add RO_HEADER row
            #3. Create a row for RO_DETAIL for each stock line 
            #get the last vendor from the stock line
            recs = []
            roh_msg = 'RO#(s) created: '
            count = 0
            
            vendor_rohs = {}
            ro_header_ids = []            
            #loop through and create one RO Header per last vendor and create RO_DETAIl lines for each stock line 
            
            for stm_key in stm_keys:                     
                srec = get_stock_ros(cr,stm_auto_key=stm_key)
                srec = srec and srec[0] or []
                vendor_key = get_ro_vendor(srec,session_id,wos_obj)
                #stock_recs[6] is the last vendor
                #create the RO_DETAIL line.
                #get the user from the form and lookup sysur_auto_key
                if not vendor_key:
                    return 'No vendor found.',''
                elif vendor_key not in vendor_rohs:
                    error,rohs_created = insert_ro_header(cr,sysur_auto_key,vendor_key,right_now,srec)
                    if roh_msg != 'RO#(s) created: ':
                        roh_msg += ', ' + str(rohs_created)
                    else:
                        roh_msg += str(rohs_created)
                    roh_auto_key = get_new_roh(cr,vendor_key,right_now,sysur_auto_key=sysur_auto_key)   
                    vendor_rohs[vendor_key] = [roh_auto_key]
                elif vendor_key in vendor_rohs:
                    roh_auto_key = get_new_roh(cr,vendor_key,right_now,sysur_auto_key=sysur_auto_key) 
                    vendor_rohs[vendor_key].append(roh_auto_key) 
                rods_created += insert_ro_detail(cr,srec,right_now,sysur_auto_key,roh_auto_key=roh_auto_key)                      
                count += 1                       
            msg = str(roh_msg) + ' along with one detail line each.'
        elif ro_number:
            #1. look up RO from RO# entered.
            ro_header = get_ro_header(cr,ro_number=ro_number)
            #2. Insert RO_DETAIL LINES (with detail line from stock line in question)
            #into existing (user-entered RO from step #1) 
            #Loop through the stock lines and add an RO_DETAIL for each of the stock lines.
            #for stm_auto_key in stm_keys:
            #error,rohs_created = insert_ro_header(cr,vendor_key,right_now,stock_recs)
            if ro_header:
                ro_number = ro_header[0] and ro_header[0][0] or None
                roh_auto_key = ro_header[0] and ro_header[0][1] or None   
                if roh_auto_key:
                    count = 0
                    for stm_key in stm_keys:
                        srec = get_stock_ros(cr,stm_auto_key=stm_key)
                        srec = srec and srec[0] or []
                        #vendor_key = srec and get_ro_vendor(srec,session_id,wos_obj) or None
                        #if not vendor_key:
                        #    return 'No vendor found.',''
                        #get vendor from stock record
                        rods_created += insert_ro_detail(cr,srec,right_now,sysur_auto_key,roh_auto_key=roh_auto_key)
                        count += 1
                    msg = str(rods_created) + ' detail line(s) created and added to RO# '+ str(ro_number) + '.'
            else:
                error = 'RO not found.'
                              
        elif vendor:
            #1. Simply create RO_HEADER FROM the vendor that the user entered in the pop-up
            #2. Insert RO_DETAIL LINES (with detail line from stock line in question)
            #     into existing (user-entered RO from step #1) 
            #Loop through the stock lines and add an RO_DETAIL to the 
            #vendors need to be created and accessed in dropdown on pop-up form
            #stock_recs = get_stock_ros(cr,stm_auto_key=stm_keys[0])
            #srec = stock_recs and stock_recs[0] or [] 
            #syscm_auto_key,dpt_auto_key
            #ship_address1, ship_address2, ship_address3, ship_address4,
            #ship_address5, ship_name,
            #vendor_address1, vendor_address2, vendor_address3, 
            #vendor_address4, vendor_address5, vendor_name
            #srecs[12],srecs[10],srecs[13],srecs[14],srecs[15],srecs[16],srecs[17],srecs[18],srecs[19],srecs[20],srecs[21],srecs[22],srecs[23],srecs[24]
            vendor_key = vendor
            if not vendor_key:
                return 'No vendor found.',''
            else:
                query = """
                SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,
                SYSCM_AUTO_KEY,SHIP_ADDRESS1,SHIP_ADDRESS2,SHIP_ADDRESS3,NULL,NULL,
                SHIP_NAME,ADDRESS1,ADDRESS2,ADDRESS3,NULL,NULL,COMPANY_NAME
                FROM COMPANIES WHERE CMP_AUTO_KEY = %s
                """%vendor_key
                vendor_info = selection_dir(query,cr)
                vrec = vendor_info and vendor_info[0] or [] 
            if vendor_key:
                error,rohs_created = insert_ro_header(cr,sysur_auto_key,vendor_key,right_now,vrec) or ''
                roh_auto_key = get_new_roh(cr,vendor_key,right_now,sysur_auto_key=sysur_auto_key)
                rods_created = 0
                if error == '{"recs": ""}':
                    error = ''                
                if not error and roh_auto_key:
                    count = 0
                    for stm_key in stm_keys:                     
                        srec = get_stock_ros(cr,stm_auto_key=stm_key)
                        srec = srec and srec[0] or []                          
                        #get vendor from stock record
                        rods_created += insert_ro_detail(cr,srec,right_now,sysur_auto_key,roh_auto_key=roh_auto_key)
                        count += 1
                    msg = 'RO#(s): ' + str(rohs_created) + ', created with ' + str(rods_created) + ' detail line(s).'                  
            else:
                error = "'%s' is not a vendor id in the database."%vendor            
        else:
            #get vendor in a pop-up
            return '','show_modal' 
    #register audit trail record
    if msg and msg != 'show_modal' and (not error or error == '{"recs": ""}'):
        orcl_commit(con=con)      
        error = ''        
        stock_lines_del = wos_obj.objects.filter(session_id=session_id,stm_auto_key__in = stm_keys)
        stock_lines_del = stock_lines_del and stock_lines_del.delete()
    aud_status = 'success'
    app_id = maps.objects.filter(code='repair-order-mgmt')   
    user_rec = qu.objects.filter(user_auto_key=sysur_auto_key)
    user_rec = user_rec and user_rec[0] or None
    if user_rec:
        field_changed = 'Added new RO.'
        new_val = 'Added new RO.'
        if error:             
            aud_status = 'failure'
            new_val = error
            field_changed = 'Nothing changed.'
        right_now = datetime.now()
        now = right_now.strftime('%Y-%m-%d %H:%M:%S')  
        error += register_audit_trail(user_rec,field_changed,new_val,now,app_id,quapi,status=aud_status)
    else:
        error = 'Incorrect Quantum User ID.'        
    return error,msg
 
def get_ro_vendor(srec,session_id,wos_obj):
    moves = wos_obj.objects.filter(session_id=session_id,stm_auto_key=srec[8])
    last_vendor_key = None
    for move in moves:
        if move.vendor_key:
            last_vendor_key = move.vendor_key
            break
    return last_vendor_key
    
def get_new_roh(cr,vendor_key,right_now,sysur_auto_key=''):
    sysur_auto_key = sysur_auto_key and 'AND SYSUR_AUTO_KEY = %s '%sysur_auto_key or '' 
    entry_date = ''   
    if sysur_auto_key:
        entry_date = ''
    else:
        entry_date = "AND ENTRY_DATE=TO_DATE('%s','MM-DD-YYYY')"%right_now  
    query = """SELECT ROH_AUTO_KEY FROM RO_HEADER WHERE 
        CMP_AUTO_KEY = %s 
        %s
        %s
        ORDER BY ROH_AUTO_KEY 
        DESC"""%(vendor_key,entry_date,sysur_auto_key)
    roh = selection_dir(query,cr)
    roh_auto_key = roh and roh[0] or None
    roh_auto_key = roh_auto_key and roh_auto_key[0] or None
    return roh_auto_key
      
def get_stored_vendor(vendor_id):
    #method that takes a user-entered vendor auto key and looks it up in local db
    from polls.models import Companies as comp
    recs = comp.objects.filter(cmp_auto_key = vendor_id)
    vendor = recs and recs[0] or []
    vendor = vendor and vendor.cmp_auto_key or None
    return vendor
   
  

    