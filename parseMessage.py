#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests
from getConfigFile import get_ConfigFile
import database
import parser_paodeacucar
import sys
import difflib
import unidecode

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

    # r = requests.post(url, data=json.dumps(payload), headers=headers)

    # Print for Debug
    print(url, json.dumps(payload), (headers))

    return None

def selectItemByNumber(msg):

    words = unidecode.unidecode(msg).split()

    validationArray = 'um dois tres quatro cinco seis sete oito nove dez'

    validationArray = validationArray.split()

    for d in words:

        if d in validationArray:

            response = dict()
            response['um'] = "1"
            response['dois'] = "2"
            response['tres'] = "3"
            response['quatro'] = "4"
            response['cinco'] = "5"
            response['seis'] = "6"
            response['sete'] = "7"
            response['oito'] = "8"
            response['nove'] = "9"
            response['dez'] = "10"

            return response['%s'%d]

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

def insertOnList(number, lastitem):

    search = parser_paodeacucar.searchProduct(lastitem)

    product = dict()

    for d in search[1]:
        product['Name'] = search[1][d]['Name']
        product['Price'] = search[1][d]['Price']

    database.insertOnList(number, product)

    return None

def getProductsList(number):

    products = database.checkProductsList(number)

    count = 0
    msg = ''
    for d in products:
        msg += '%s\n'%d[2]

    return(msg)

def readMsg(data):

    message = data["message"]["contents"][1]["text"].lower()

    name = data["message"]["visitor"]["name"]

    number = data["message"]["from"]

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

            lastSearch = json.loads(database.checkLastSearch(number)[0][0])
            print('lastSearch: %s'% lastSearch)

            try:
                lastItem = json.loads(database.checkLastItem(number))
            except:
                lastItem = {}

            print('lastItem: %s'% lastItem)

            if str(lastStatus) == '0' or str(lastStatus) == '2' or str(lastStatus) == '-1' :
                print('Status 0 2 ou -1')
                # todo Lista de Produtos

                search = parser_paodeacucar.searchProduct(message)

                listaProdutos = search[0]

                actualLista = json.dumps(search[1])

                database.insertSearch(number, actualLista)

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

                if countInfo < 1 and countLista < 1:
                    print('Entrou no count menor que 2')

                    search = parser_paodeacucar.searchProduct(message)

                    listaProdutos = search[0]

                    actualLista = json.dumps(search[1])

                    database.insertSearch(number, actualLista)

                    msg = "Essa foi a lista de produtos que eu encontrei:\n%s\nO que você gostaria de fazer agora?\
                        \nPode pedir informação sobre um produto informando também o número dele.\
                        \nPara fazer fazer outra consulta é só me falar o nome de um outro produto.\
                        \nPara salvar ele em sua lista basta falar que quer adicionar o produto e o número dele."%listaProdutos.encode(encoding="utf-8",errors="strict")

                    sendMsg(msg, number)

                    database.insertHistory(number, msg, 3)
                
                elif countInfo >= countLista:
                    
                    selectedItem = selectItemByNumber(message)
                    
                    if not selectedItem or int(selectedItem) > len(lastSearch):
                        msg = "Eu não consegui entender o item que você quer consultar, pode repetir o número dele pra mim, por favor?"

                        sendMsg(msg, number)

                        database.insertHistory(number, msg, 4)

                    else:

                        infoProduct = parser_paodeacucar.getProductDescription(lastSearch['%s'%selectedItem]['id'])

                        msg = 'Eu encontrei essas informações sobre o produto:\n%s\n%s\n%s\n\nVocês gostaria de adicionar este produto na sua lista de compras?'%(infoProduct['name'], infoProduct['description'], infoProduct['disponibility'])

                        database.insertSearchItem(number, lastSearch['%s'%selectedItem]['id'])

                        sendMsg(msg, number)

                        database.insertHistory(number, msg, 8)

                    
                else:

                    selectedItem = selectItemByNumber(message)
                    
                    if not selectedItem or int(selectedItem) > len(lastSearch):
                        msg = "Eu não consegui entender o item que você quer consultar, pode repetir o número dele pra mim, por favor?"

                        sendMsg(msg, number)

                        database.insertHistory(number, msg, 5)
                    
                    else:

                        insertOnList(number, lastSearch['%s'%selectedItem]['id'])

                        msg = 'Inseri aqui pra você, ta bom? Gostaria de consultar mais algum produto?'

                        sendMsg(msg, number)

                        database.insertHistory(number, msg, 11)


            elif str(lastStatus) == '4':

                selectedItem = selectItemByNumber(message)

                if not selectedItem or int(selectedItem) > len(lastSearch):
                    msg = "Eu não consegui entender o item que você quer consultar, pode repetir o número dele pra mim, por favor?"

                    sendMsg(msg, number)

                    database.insertHistory(number, msg, 4)

                else:

                        infoProduct = parser_paodeacucar.getProductDescription(lastSearch['%s'%selectedItem]['id'])

                        msg = 'Eu encontrei essas informações sobre o produto:\n%s\n%s\n%s\n\nVocês gostaria de adicionar este produto na sua lista de compras?'%(infoProduct['name'], infoProduct['description'], infoProduct['disponibility'])

                        sendMsg(msg, number)

                        database.insertHistory(number, msg, 8)

            elif str(lastStatus) == '5':

                selectedItem = selectItemByNumber(message)
                    
                if not selectedItem or int(selectedItem) > len(lastSearch):
                    msg = "Eu não consegui entender o item que você quer consultar, pode repetir o número dele pra mim, por favor?"

                    sendMsg(msg, number)

                    database.insertHistory(number, msg, 5)
                
                else:

                    insertOnList(number, lastSearch['%s'%selectedItem]['id'])

                    msg = 'Inseri aqui pra você, ta bom? Gostaria de consultar mais algum produto?'

                    sendMsg(msg, number)

                    database.insertHistory(number, msg, 11)

            elif str(lastStatus) == '8':

                yesWords = 'sim quero si s adicionar botar na lista quero por na lista produto na lista adicionar inserir'

                countYes = checkProximityString(message, yesWords)

                print('countYes: %s'%countYes)

                if countYes >= 1:

                    insertOnList(number, lastItem)

                msg = 'Maravilha, gostaria de consultar mais algum produto?'

                sendMsg(msg, number)

                database.insertHistory(number, msg, 11)

            elif str(lastStatus) == '11':

                yesWords = 'sim quero si s adicionar botar na lista quero por na lista produto na lista adicionar inserir'

                countYes = checkProximityString(message, yesWords)

                if countYes >= 1:

                    msg = 'Tudo bem, qual produto quer consultar?'

                    sendMsg(msg, number)

                    database.insertHistory(number, msg, 2)

                else:

                    #if valida se tem lista

                    msg = 'Você gostaria de receber sua lista de compras?'

                    sendMsg(msg, number)

                    database.insertHistory(number, msg, 12)

            elif str(lastStatus) == '12':

                yesWords = 'sim quero si s adicionar botar na lista quero por na lista produto na lista adicionar inserir'

                countYes = checkProximityString(message, yesWords)

                if countYes >= 1:

                    actualList = getProductsList(number)

                    msg = 'Aqui está sua lista de hoje:\n\n %s\nConseguiu encontrar tudo que você estava precisando?'

                    sendMsg(msg, number)

                    database.insertHistory(number, actualMsg, 9)

                else:

                    msg = 'Espero que eu tenha consigo te ajudar hoje. Você pode pode contar como foi sua experiência comigo hoje? Eu ainda estou aprendendo a entender os seres humanos e isso vai me ajudar bastante!\
                        \nTenha um ótimo dia!'

                    sendMsg(msg, number)

                    database.insertHistory(number, actualMsg, 10)

            elif str(lastStatus) == '9':

                yesWords = 'sim quero si s adicionar botar na lista quero por na lista produto na lista adicionar inserir'

                countYes = checkProximityString(message, yesWords)

                if countYes >= 1:

                    msg = 'Eba, que bom que consegui te ajudar a encontrar tudo que precisava. Se você quiser, pode me falar um pouquinho como eu posso melhorar a sua experiência.\
                        \nEu ainda estou aprendendo a entender os humanos. Tenha um ótimo dia!'

                    sendMsg(msg, number)

                    database.insertHistory(number, actualMsg, 6)

                else:

                    msg = 'Poxa, sinto muito por não ter conseguido encontrar tudo o que você precisava. Estou melhorando a cada dia mais ainda é difícil pra mim\
                        \nSerá que você tem alguma dica pra me dar de como eu posso melhorar o meu entendimento dos humanos?\
                        \nEu vou ficar muito feliz em conseguir te ajudar melhor da próxima vez :)\
                        \nTenha um ótimo dia'

                    sendMsg(msg, number)

                    database.insertHistory(number, actualMsg, 7)

            elif str(lastStatus) == '6' or str(lastStatus) == '7' or str(lastStatus) == '10':

                database.insertHistory(number, message, 2)

                database.endChat(number)

                # validate time > xxxx para encerrar atendimento

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

