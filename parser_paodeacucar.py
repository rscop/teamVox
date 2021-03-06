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

    response["name"] = product["content"]["name"]

    # response["content"]["itemMap"][0]["reference"]["currentPrice"]

    try:
        description = 'sua descrição é ' + product["content"]["shortDescription"]
    except:
        try:
            description = response["content"]["itemMap"][0]["reference"]["shortDescription"].replace('\n', '').strip()
        except:
            description = 'não apresenta descrição'

    if (product["content"]["stock"]):
    # if (product["content"]["stock"]) == 'true':
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
        'w': '%s'%product,
        'cnt': '5',
        'ref': 'www.paodeacucar.com',
        'lot': 'json',
        'ep.selected_store': '501'
        }

    r = requests.get(url, params=payload)

    products = r.json()

    productsList = {}

    try:
        products = products["results"]["product_suggestions"]["suggestions"]

        msg = ""

        count = 1

        for d in products:
            title = d["title"]

            productId = d["url"].split('/')[4]

            # rank = d["rank"]
            try:
                price = d["price"]
            except:
                price = '00.00'

            # moreInfo = getProductDescription(productId)

            msg+='%s. %s que custa %s reais.\n'%(count, title, price)

            productsList['%s'%count] = {"Name": title, "id": productId, "Price": price}

            count += 1

    except Exception as e:
        print(e)
        msg = 'Poxa, eu não consegui encontrar nada com o que você me mandou.\
            \nFaz o seguinte, tenta me mandar o nome do produto de novo, um de cada vez'

    return [msg, productsList]
