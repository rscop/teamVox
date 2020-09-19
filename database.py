#!flask/bin/python
import mysql.connector
import sys
from getConfigFile import get_ConfigFile

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

# def startChat(name):
#     query = "insert into chat (name, start_date, cel_number) values ('%s', '%s')"%(str(name), str(xxxxxx), str(number))

#     return None

# def insertHistory(name, number):
#     query = "insert into clienxts (name, celnumber) values ('%s', '%s')"%(str(name), str(number))

#     return None
