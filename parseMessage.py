#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests
from getConfigFile import get_ConfigFile
import database
import parser_paodeacucar
import sys
import difflib

env = get_ConfigFile(sys.argv[0]+'.env', 'production')

def sendMsg(response, number):

    url = 'https://api.zenvia.com/v1/channels/whatsapp/messages'

    payload = {
        "from": "%s"%env['SECURE_STRING'],
        "to": '%s'%number,
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

    return None

def selectItemByNumber(msg):

    words = msg.split()

    validationArray = 'um dois três tres quatro cinco seis sete oito nove dez'

    validationArray = validationArray.split()

    for d in words:

        if d in validationArray:
            
            response = {
            'um': "1",
            'dois': "2",
            'três' "3",
            'tres': "3",
            'quatro': "4",
            'cinco': "5",
            'seis': "6",
            'sete': "7",
            'oito': "8",
            'nove': "9",
            'dez': "10"
            }
            
            return response[d]

    return False

def checkProximityString(msg, listWords):

    words = listWords.encode(encoding="utf-8",errors="strict")

    words = words.split()

    string = msg.split()

    matches = 0

    for d in string:

        if str(difflib.get_close_matches(d.encode(encoding="utf-8",errors="strict"),words)) != '[]':

            matches += 1

    return matches

def readMsg(data):

    message = data["message"]["contents"][1]["text"].lower()

    name = data["message"]["visitor"]["name"]

    number = data["message"]["from"]

    # if 'marco' in message:
    #     sendMsg('teeeeeeeeest', number)

    # if isClient(number):

    if database.isClient(number) == '[]':
        print('Cliente ainda não registrado, registrando...')

        database.registerClient(name, number)

        actualMsg = "Olá, agora seu número está registrado em nosso sistema. \
            \nSou o VOX, e vou te ajudar com as compras hoje. Espero que você esteja em um bom dia <3 \
            \nPrecisando de informações sobre algum produto? Me fala o nome dele que eu procuro aqui rapidinho"

        sendMsg(actualMsg, number)

        database.startChat(number)

        database.insertHistory(number, message, -1)

        database.insertHistory(number, actualMsg, 0)

    else:

        if database.chatIsOpen(number):
            
            lastStatus = database.checkLastStatus(number)[0][0]
            print('lastStatus: %s'%lastStatus)

            database.insertHistory(number, message, -1)

            lastSearch = database.checkLastSearch(number)
            print('lastSearch: %s'% lastSearch)

            if str(lastStatus) == '0' or str(lastStatus) == '2' or str(lastStatus) == '-1' :
                print('Status 0 2 ou -1')
                # todo Lista de Produtos

                search = parser_paodeacucar.searchProduct(message)

                listaProdutos = search[0]

                database.insertSearch(number, listaProdutos)

                actualLista = search[1]

                msg = "Essa foi a lista de produtos que eu encontrei:\n%s\nO que você gostaria de fazer agora?\
                    \nPode pedir informação sobre um produto informando também o número dele.\
                    \nPara fazer fazer outra consulta é só me falar o nome de um outro produto.\
                    \nPara salvar ele em sua lista basta falar que quer adicionar o produto e o número dele."%listaProdutos.encode(encoding="utf-8",errors="strict")

                sendMsg(msg, number)
                database.insertHistory(number, msg, 3)

            elif str(lastStatus) == '3':
                print('Status 3')

                infoWords = 'eu gostaria de mais informações sobre o produto eu quero mais informações sobre dados sobre descrição ingredientes o a\
                    informação do produto informação sobre eu quero informação do info mais infos quero saber sobre o\
                    descrição do produto descrever falar sobre o que é o produto que produto é esse info + eu quero ver'

                infoLista = 'eu gostaria de adicionar o produto na lista eu quero adicionar o produto na lista eu quero\
                    botar na lista quero adicionar na lista colocar produto na lista eu quero por o produto na lista botar o\
                    produto na lista adicionar na lista lista add adicionar adc'

                countInfo = checkProximityString(message, infoWords)
                print('countInfo: %s'%countInfo)
                countLista = checkProximityString(message, infoLista)
                print('countLista: %s'%countLista)

                if countInfo < 2 and countLista < 2:
                    print('Entrou no count menor que 3')

                    search = parser_paodeacucar.searchProduct(message)

                    listaProdutos = search[0]

                    database.insertSearch(number, listaProdutos)

                    actualLista = search[1]

                    msg = "Essa foi a lista de produtos que eu encontrei:\n%s\nO que você gostaria de fazer agora?\
                        \nPode pedir informação sobre um produto informando também o número dele.\
                        \nPara fazer fazer outra consulta é só me falar o nome de um outro produto.\
                        \nPara salvar ele em sua lista basta falar que quer adicionar o produto e o número dele."%listaProdutos.encode(encoding="utf-8",errors="strict")

                    sendMsg(msg, number)

                    database.insertHistory(number, msg, 3)
                
                elif countInfo >= countLista:
                    
                    # lastSearch = json.loads(checkLastSearch(number)[0][0])

                    # print(lastSearch)

                    selectedItem = selectItemByNumber(message, lastSearch)

                    print('selectedItem: %s'%selectedItem)

                    infoProduct = parser_paodeacucar.getProductDescription(lastSearch['%s'%selectedItem])

                    msg = 'Eu encontrei essas informações sobre o produto:\n%s\n%s\n%s\n\nVocês gostaria de adicionar este produto na sua lista de compras?'%(infoProduct['name'], infoProduct['description'], infoProduct['disponibility'])

                    sendMsg(msg, number)

                    database.insertHistory(number, msg, 8)

                    if not selectedItem:
                        msg = "Eu não consegui entender o item que você quer consultar, pode repetir o número dele pra mim, por favor?"

                        sendMsg(msg, number)

                        database.insertHistory(number, msg, 4)

                    
                # else:
                    #Adicionar na lista

                # Valida se quer mais informação, outra consulta ou salvar na lista

            elif str(lastStatus) == '4':

                # lastSearch = json.loads(checkLastSearch(number)[0][0])

                # print(lastSearch)

                selectedItem = selectItemByNumber(message, lastSearch)

                print('selectedItem: %s'%selectedItem)

                if not selectedItem:
                    msg = "Eu não consegui entender o item que você quer consultar, pode repetir o número dele pra mim, por favor?"

                    sendMsg(msg, number)

                    database.insertHistory(number, msg, 4)

            return None

        else:

            database.startChat(number)

            database.insertHistory(number, message, -1)

            actualMsg = "Oi de novo, ficou muito feliz em poder te ajudar em mais um dia.\nO que você precisa hoje?"

            sendMsg(actualMsg, number)

            database.insertHistory(number, actualMsg, 2)

            return None

        # sendMsg("Você já sabe a marca que gostaria de consultar?\n Ou prefere ouvir as recomendações mesmo?", number)

        response = parser_paodeacucar.searchProduct(message)
        print(response)    

    return None

