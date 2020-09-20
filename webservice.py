#!flask/bin/python
from flask import Flask, abort, request, jsonify, g, url_for
import sys
import logging
import logging.handlers
import os
import json
from parseMessage import readMsg
from getConfigFile import get_ConfigFile

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)

def logStart():
    logit('===================================================')
    logit('===================================================')
    logit('[         INICIANDO SERVICO DE WEBSERVICE         ]')
    logit('===================================================')
    logit('===================================================')

# SetupLOG Funnction
def setuplog(lf,lfBkpCnt,logLevel):

    global gtwlogger

    gtwlogger = logging.getLogger('GTW_LOG')

    gtwlogger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s-%(message)s')

    # Add the log message handler to the logger
    handler = logging.handlers.TimedRotatingFileHandler(lf, when='midnight', interval=1, backupCount=lfBkpCnt)

    handler.setFormatter(formatter)

    gtwlogger.addHandler(handler)
    
    logStart()

def logit(m):
    if config['log_mode']=='2':
        print(m)
    gtwlogger.debug(m)


# Method for data query (Verify API Integrity)
@app.route('/healthcheck', methods=['GET'])
def get():
    
    logit('Receiving GET on /healthcheck')

    # Response if OK
    response = '{"status": "Ok"}'

    logit('GET OK')
    return(response)

@app.route('/receiveMsg', methods=['POST'])
def receiveMsg():

    data = json.loads(request.data)

    message = data["message"]["contents"][1]["text"]

    name = data["message"]["visitor"]["name"]

    number = data["message"]["from"]

    logit('%s [%s]: %s'%((name).encode('utf-8').strip(), (number).encode('utf-8').strip(), (message).encode('utf-8').strip()))

    readMsg(data)

    response = '{"status": "Ok"}'

    return(response)


if __name__ == '__main__':

    config = get_ConfigFile(sys.argv[0]+'.cfg', 'production')

    setuplog(config['logfile'],config['logfile_backup_count'],config['log_level'])

    logit('Log OK')
    logit('Config File OK')
    
    ip = config['listen_ip']

    port = config['listen_port']

    logit('Starting WS')
    app.run(host=ip, port=port, debug=False)
    logit('WS finished')