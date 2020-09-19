#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests
import sys

def getProductDescription(product_id):

    url = 'https://api.gpa.digital/pa/v3/products/ecom/%s'%product_id

    payload = {'storeId': '501'}

    r = requests.get(url, params=payload)

    product = r.json()

    response = dict()

    try:
        description = 'sua descrição é ' + product["content"]["shortDescription"]
    except:
        description = 'não apresenta descrição'

    if str(product["content"]["stock"]).lower() == 'true':
        disponibility = "em estoque"
    else:
        disponibility = "fora de estoque"

    response["description"] = description
    response["disponibility"] = disponibility

    return response


def searchProduct(product):

    url = 'https://paodeacucar.resultspage.com/search'

    payload = {
        'ts': 'json-rac',
        'w': '%s'%str(product),
        'cnt': '5',
        'ref': 'www.paodeacucar.com',
        'lot': 'json',
        'ep.selected_store': '501'
        }

    r = requests.get(url, params=payload)

    products = r.json()

    try:
        products = products["results"]["product_suggestions"]["suggestions"]

        msg = "Está é a listinha de produtos que conseguir encontrar para você no Pão de Açúcar.\n"
        for d in products:
            title = d["title"]
            productId = d["url"].split('/')[4]
            rank = d["rank"]
            price = d["price"]
            moreInfo = getProductDescription(productId)
            msg+='%s que custa %s reais. Atualmente ele está %s e %s \n'%(title, price, moreInfo['disponibility'], moreInfo['description'])

        msg = msg.replace("<b>","").replace("</b>", "").replace("<p>", "").replace("</p>", "").replace("<br>", "")
    except:
        msg = 'Poxa, eu não consegui encontrar nada com o que você me mandou. \
            \nFaz o seguinte, tenta me mandar o nome do produto de novo, um de cada vez'

    return msg
