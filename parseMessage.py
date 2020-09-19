#!/usr/bin/python
import json
import requests
from getConfigFile import get_ConfigFile
import database
import parser_paodeacucar
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
        print('Cliente ainda não registrado, registrando...')

        database.registerClient(name, number)

        sendMsg("Olá, agora seu número está registrado em nosso sistema. \
            \nSou o VOX, e vou te ajudar com as compras hoje. Espero que você esteja em um bom dia <3 \
            \nPrecisando de informações sobre algum produto? Me fala o nome dele que eu procuro aqui rapidinho")
        database.startChat(number)
        database.insertHistory(number, message)

    else:
        # sendMsg("Você já sabe a marca que gostaria de consultar?\n Ou prefere ouvir as recomendações mesmo?")

        response = parser_paodeacucar.searchProduct(message)
        print(response)
        # sendMsg(str(response))
        # database.insertHistory(number, )

    # if database.chatIsOpen(number):
    

    return None

