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
    password=env["DB_PASS"],
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

    query = "select * from clients where celnumber = %s"%(number).encode('utf-8').strip()
    
    records = fetchData(query)

    return str(records)

def registerClient(name, number):

    query = "insert into clients (name, celnumber) values ('%s', '%s')"%(name, number)

    insertData(query)

    return None

def startChat(number):

    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    query = "insert into chat (start_date, cel_number) values ('%s', '%s')"%(timestamp, number)

    insertData(query)

    return None

def insertHistory(number, msg, msg_id):
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    prequery = "select id from chat where cel_number = %s and end_date is null"%number
    chat_id = fetchData(prequery)[0][0]

    query = "insert into msg_history (chat_id, origin, destination, reg_date, msg, msg_type) values ('%s', '%s', '%s', '%s', '%s', '%s')"%(chat_id, '0', '0', timestamp, msg, msg_id)
    insertData(query)

    return None

def chatIsOpen(number):
    query = "select * from chat where cel_number = %s and end_date is null"%number
    chatStatus = fetchData(query)
    if str(chatStatus) == '[]':
        return False
    else:
        return True

def chatOpenId(number):
    query = "select id from chat where cel_number = %s and end_date is null"%number
    return fetchData(query)
     
def checkLastStatus(number):

    query = "select msg_type from msg_history where chat_id = %s order by id desc limit 1"%chatOpenId(number)[0][0]

    return fetchData(query)

def checkLastSearch(number):

    query = "select result from lastSearch where cel_number = %s"%number

    checkSearch = fetchData(query)

    if checkSearch == '[]':

        return {}

    else:

        return checkSearch

def insertSearch(number, msg):

    dataExist = checkLastSearch(number)

    if dataExist == '[]':

        query = "insert into lastSearch (number, result) values ('%s', '%s')"%(number, msg)

    else:

        query = "UPDATE lastSearch SET result='%s' WHERE cel_number = '%s';"%(number, msg)

    insertData(query)

    return None

# chatIsOpen('5521999984171')

# insertHistory('5521999984171', 'teeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgs teeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgs \
#     teeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgs teeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgs \
#         teeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgs teeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgs teeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgsteeeeeeeeeeste de msgs \
#             ausdhasda\n iasuhdiuashdiuashd\naushduahsd\znaushdiuashduiha\niaushdiuashduiasdh')