#!/usr/bin/python
import json
import requests
from getConfigFile import get_ConfigFile
import database
import sys

env = get_ConfigFile(sys.argv[0]+'.env', 'production')

def sendMsg(response):

    url = 'https://api.zenvia.com/v1/channels/whatsapp/messages'

    payload = {
        "from": "%s"%env['SECURE_STRING'],
        "to": '5521999984171',
        "contents": [{
        'type': 'text',
        'text': '%s'%response
        }]
    }

    headers = {
        'X-API-TOKEN': "%s"%env['X_API_TOKEN'], 
        'content-type': 'application/json'
        }

    r = requests.post(url, data=json.dumps(payload), headers=headers)

    
def readMsg(data):

    message = data["message"]["contents"][1]["text"].lower()

    name = data["message"]["visitor"]["name"]

    number = data["message"]["from"]

    # if 'marco' in message:
    #     sendMsg('teeeeeeeeest')

    # if isClient(number):

    if database.isClient(number) == '[]':
        print('Ainda não é cliente, registrar')
        database.registerClient(name, number)
    else:
        print('Já é cliente, seguir com validações')

    return None

