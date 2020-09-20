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

def endChat(number):

    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    query = "update chat set end_date = '%s' where cel_number = '%s' and end_date is null"%(timestamp, number)

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

    print('checkLastSearch')

    print(checkSearch)

    if str(checkSearch) == '[]' or str(checkSearch) == '{}' or len(checkSearch) == 0:

        return {}

    else:

        return checkSearch

def checkProductsList(number):

    prequery = "select id from chat where cel_number = %s and end_date is null"%number

    chat_id = fetchData(prequery)[0][0]

    query = 'select * from client_product_list where chat_id = %s order by id desc'%chat_id

    result = fetchData(query)

    if str(result) == '[]':

        return False

    else:

        return result

def insertOnList(number, product):

    prequery = "select id from chat where cel_number = %s and end_date is null"%number

    chat_id = fetchData(prequery)[0][0]
    
    query = "insert into client_product_list (chat_id, product) values ('%s', '%s - %s reais')"%(chat_id, product["Name"], product["Price"])

    insertData(query)

    return None

def checkLastItem(number):

    query = "select item from lastSearch where cel_number = %s"%number

    checkSearch = fetchData(query)

    if str(checkSearch[0][0]) == 'None':

        return {}

    else:

        return checkSearch[0][0]

def insertSearch(number, msg):
    print('Insert Search')
    print('number: %s \nMessage: %s')%(number, msg)

    dataExist = checkLastSearch(number)

    if str(dataExist) == '[]' or str(dataExist) == '{}' or len(dataExist) == 0:

        query = "insert into lastSearch (cel_number, result) values ('%s', '%s')"%(number, msg)

    else:

        query = "UPDATE lastSearch SET result='%s' WHERE cel_number = '%s';"%(msg, number)

    insertData(query)

    return None

def insertSearchItem(number, msg):

    dataExist = checkLastSearch(number)

    if dataExist == {}:

        query = "insert into lastSearch (cel_number, item) values ('%s', '%s')"%(number, msg)

    else:

        query = "UPDATE lastSearch SET item='%s' WHERE cel_number = '%s';"%(msg, number)

    insertData(query)

    return None

def getChatTime(number):

    query = "\
    select\
        msh.id as msg_id,\
        SEC_TO_TIME(TIME_TO_SEC(msh.reg_date)) as last_msg,\
        SEC_TO_TIME(TIME_TO_SEC(CURRENT_TIMESTAMP)) as time_now,\
        TIME_TO_SEC(ch.start_date) as time_ini_sec,\
        TIME_TO_SEC(msh.reg_date) as time_last_msg_sec\
    from\
        chat as ch inner join msg_history as msh on ch.id = msh.chat_id\
    where \
        ch.cel_number = '%s'\
        and ch.end_date is null\
        and msh.id = (\
            select max(id) from\
            msg_history msg where msg.chat_id = ch.id);"%number

    return fetchData(query)