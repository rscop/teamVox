#!/usr/bin/python
import json
import requests
from getConfigFile import get_ConfigFile
import database
import parser_paodeacucar
import sys
import base64

# env = get_ConfigFile(sys.argv[0]+'.env', 'production')

def audioToText(data):
    # url = 'https://speech.googleapis.com/v1/speech:recognize?key=%s'%env['GOOGLE_API_KEY']
    url = 'https://speech.googleapis.com/v1/speech:recognize?key=AIzaSyAwuBkofALGvA4_bpbP7esiWb1WoyXGo88'

    headers = {'content-type': 'application/json'}

    payload = {
        "config": {
            "encoding": "OGG_OPUS",
            "sampleRateHeartz": 16000,
            "languageCode": "pt-BR"
        },
        "audio": {
            "content":str(data)
        }
    }

    r = requests.post(url, data=json.dumps(payload), headers=headers)

def get_as_base64(url):

    # encoded_string = base64.b64encode(requests.get(url).content)

    # r = requests.get(url)

    # with open("tts.ogg", "wb") as o:
    #     o.write(r.content)
    
    # response = open('tts.ogg', "r", encoding='latin1')
    
    # msg = response.read()
    
    # print(base64.b64encode(b'%s'%encoded_string))

    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        print(text)

get_as_base64('http://chat.zenvia.com/storage/files/9416c34b3d89838f526ff8fe924b11e904044c6ebb6352be749693b55fc8dafd.bin')

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
            \nSou o BOT, e vou te ajudar com as compras hoje. Espero que você esteja em um bom dia <3 \
            \nPrecisando de informações sobre algum produto? Me fala o nome dele que eu procuro aqui rapidinho")

    else:
        response = parser_paodeacucar.searchProduct(message)

        sendMsg(str(response))

        # database.startChat(name, number)
        # database.insertHistory(name, number)

    # if database.chatIsOpen(number):
    

    return None

