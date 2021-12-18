import cx_Oracle
import traceback
conn = None
try:
    # dsn_tns=cx_Oracle.makedsn("localhost","1521",service_name="xe")
    # conn=cx_Oracle.connect(user="mouzikka",password="music",dsn=dsn_tns)
    conn=cx_Oracle.connect("mouzikka/music@localhost")
    print("Connected Succesfully to the DB")
    print("Database Version:", conn.version)
    print("DB User:", conn.username)
except cx_Oracle.DatabaseError:
    print("DB Error")
    print(traceback.format_exc())
finally:
    if conn is not None:
        conn.close()
        print("Disconnected successfully from the DB")