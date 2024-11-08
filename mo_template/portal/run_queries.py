from queries.connector import cx_Oracle
from queries.models import OracleConnection
import logging
logger = logging.getLogger(__name__)

def orcl_connect(schema):
    cr=None
    con=None
    # Connect to Oracle
    try:
        connstr = schema.schema + '/' + schema.db_user + '@' + schema.host + ':' + str(schema.port) + '/' + schema.sid
        con = cx_Oracle.connect(connstr)
        print('successful connection to Oracle')
    except Exception as exc:
        error, = exc.args
        #message = error.message
        #print("Oracle-Error-Code:", error.code)
        #print("Oracle-Error-Message:", message)
    cr = con and con.cursor() or None
    if not con:
        return False,False
    return cr,con
    
def insertion_dir(query,schema):
    recs = []
    msg = ''
    new_auto_key = None
    cr,con_orcl = orcl_connect(schema)
    try:
        cr.execute(query) 
        #query_res = "SELECT %s FROM %s ORDER BY %s DESC"%(auto_key, table_name, auto_key)
        #cr.execute(query_res) 
        #for row in cr:
        #    new_auto_key = row[0]
        #    break        
    except Exception as exc:
        error, = exc.args
        msg = error.message
        print("Oracle-Error-Code:", error.code)
        print("Oracle-Error-Message:", msg)
    con_orcl.commit()
    return str(msg)
    
def orcl_commit(schema):
    #commit the database updates
    msg = ''
    cr,con_orcl = orcl_connect(schema) 
    try:       
        con_orcl.commit()
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        msg = error.message
        logger.error("Oracle-Error-Code: '%s'",error.code)
        logger.error("Oracle-Error-Message: '%s'",msg)      
    return msg
       
def selection_dir(query,schema,table_name=''):
    recs = []
    res = []
    all_res = []
    #from queries.models import OracleConnection as oc
    #schema = oc.objects.filter(id=schema)
    #schema = schema and schema[0] or None
    if schema:    
        cr,con_orcl = orcl_connect(schema)
        try:
            cr.execute(query)
            recs = cr.fetchall()        
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            print("Oracle-Error-Code:", error.code)
            print("Oracle-Error-Message:", error.message)
        if recs:       
            for count,rec in enumerate(recs):
                res = ['' if (field == None or field == 'None') else field for field in rec]
                if table_name:
                    regex = re.compile('[^0-9a-zA-Z #,.-]+')
                    res = [regex.sub(' ',field) if isinstance(field, str) else field for field in res]
                all_res.append(res)
    return all_res
    
def updation_dir(query,schema):   
    msg = ''
    cr,con_orcl = orcl_connect(schema)
    try:
        cr.execute(query)       
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        msg = " Oracle-Error-Message:" + str(error.message) 
    con_orcl.commit()
    msg = not msg and 'no errors' or msg
    return str(msg)