from django.contrib.auth.models import Group
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.decorators import api_view
from queries.serializers import UserSerializer, GroupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from queries.models import OracleConnection
import cx_Oracle
from django.contrib.auth import get_user_model
User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
        
@api_view(['GET', 'POST'])
def run_queries(request,query_type):
    res,response = [],{}
    if not query_type:
        query_type = request.GET.get('type', 'selection') or None
    query_text = request.GET.get('query', '')
    user_id = request.GET.get('user_id', 'None')
    schema = request.GET.get('schema', 0)
    schema = schema and OracleConnection.objects.filter(id=schema) or None
    schema = schema and schema[0] or None
    if schema:  
        if query_type == 'insertion':
            res = insertion(query_text,schema)
        elif query_type == 'selection': 
            res = selection(query_text,schema)
        elif query_type == 'update': 
            res = updation(query_text,schema)
        elif query_type == 'commit': 
            res = orcl_commit(schema)
    return jsonicize(res)
    
#============================GENERAL HELPER/QUERY QUANTUM METHODS TO CONNECT DIRECTLY TO ORACLE AND RUN QUERIES, ETC==================================
def jsonicize(recs):    
    from django.http import JsonResponse
    responseData = {
        'recs':recs,
    }
    return JsonResponse(responseData,safe=True)
    
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
        message = error.message
        print("Oracle-Error-Code:", error.code)
        print("Oracle-Error-Message:", message)
    cr = con and con.cursor() or None
    if not con:
        return False,False
    return cr,con
    
def insertion(query,schema):
    recs = []
    msg = ''
    cr,con_orcl = orcl_connect(schema)
    try:
        cr.execute(query)        
    except cx_Oracle.DatabaseError as exc:
        error, = exc.args
        msg = error.message
        print("Oracle-Error-Code:", error.code)
        print("Oracle-Error-Message:", msg)
    return msg
    
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
       
def selection(query,schema,table_name=''):
    recs = []
    res = []
    all_res = []
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
    
def updation(query,schema):   
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