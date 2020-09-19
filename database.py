#!flask/bin/python
import mysql.connector
import sys
from getConfigFile import get_ConfigFile
import time
import datetime

# env = get_ConfigFile(sys.argv[0]+'.env', 'production')
env = get_ConfigFile('webservice.py'+'.env', 'production')

dbConn = mysql.connector.connect(
    host=env["DB_URL"],
    user=env["DB_USER"],
    database=env["DB_NAME"]
)
cursor = dbConn.cursor()

def fetchData(query):
    
    cursor.execute(query)

    records = cursor.fetchall()

    return records

def insertData(query):

    cursor.execute(query)

    dbConn.commit()

    return None

def isClient(number):

    query = "select * from clients where celnumber = %s"%str(number)
    
    records = fetchData(query)

    return str(records)

def registerClient(name, number):

    query = "insert into clients (name, celnumber) values ('%s', '%s')"%(str(name), str(number))


    insertData(query)

    return None

def startChat(number):

    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    query = "insert into chat (start_date, cel_number) values ('%s', '%s')"%(str(timestamp), str(number))

    insertData(query)

    return None

def insertHistory(number, msg):
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    prequery = "select id from chat where cel_number = %s and end_date is null"%number
    chat_id = fetchData(prequery)[0][0]

    query = "insert into msg_history (chat_id, origin, destination, reg_date, msg) values ('%s', '%s', '%s', '%s', '%s')"%(str(chat_id), '0', '0', str(timestamp), msg)
    insertData(query)

    return None

def chatIsOpen(number):
    query = "select * from chat where cel_number = %s and end_date is null"%number
    chatStatus = fetchData(query)
    if chatStatus == '[]':
        return False
    else:
        return True

# chatIsOpen('5521999984171')

# insertHistory('5521999984171', 'teeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgs teeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgs \
#     teeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgs teeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgs \
#         teeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgs teeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgs teeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgs \
#             ausdhasda\n iasuhdiuashdiuashd\naushduahsd\znaushdiuashduiha\niaushdiuashduiasdh')