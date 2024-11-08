import cx_Oracle

cursor=None
con=None
# Connect to Oracle database
try:
    connstr= 'qctl/quantum@18.188.56.36:1521/CCTL'
    #LGT's TRAIN schema CONNSTR
    #connstr= 'train/quantum@192.168.1.11:1521/CCTL'
    #LGT's LIVE schema CONNSTR
    #connstr= 'qctl/quantum@192.168.1.11:1521/CCTL'
    #dsn_tns = cx_Oracle.makedsn(ip, port, service_name=sid)
    #con = cx_Oracle.connect('train', 'quantum', dsn_tns)
    #import pdb;pdb.set_trace()
    con = cx_Oracle.connect(connstr)
    print('successful connection to Oracle')
except Exception as exc:
    error, = exc.args
    message = error.message
    print("Oracle-Error-Code:", error.code)
    print("Oracle-Error-Message:", message)
