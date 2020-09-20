#!flask/bin/python
from flask import Flask, abort, request, jsonify, g, url_for, send_from_directory
import sys
import logging
import logging.handlers
import os
import json
from parseMessage import readMsg
from getConfigFile import get_ConfigFile
import json
import requests

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

def audioToText(file):

    url = 'https://zenvia-team27.herokuapp.com/speech-to-text'

    payload = {
        "audioFile": "%s"%file
    }

    headers = {
        'content-type': 'application/json'
        }

    r = requests.post(url, data=json.dumps(payload), headers=headers)

    data = r.content

    return data

def isAudioReceived(data):

    msgtype = data["message"]["contents"][1]["type"]

    msgMimeType = data["message"]["contents"][1]["fileMimeType"]

    if msgtype == 'file' and msgMimeType == 'audio/ogg; codecs=opus':

        data = audioToText(data["message"]["contents"][1]["fileUrl"])

        return data
    
    else:

        return False

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

    # audio = isAudioReceived(data)

    # if audio:

        # message = audio

    # else:

    message = data["message"]["contents"][1]["text"]

    name = data["message"]["visitor"]["name"]

    number = data["message"]["from"]

    logit('%s [%s]: %s'%((name).encode('utf-8').strip(), (number).encode('utf-8').strip(), (message).encode('utf-8').strip()))

    readMsg(data)

    response = '{"status": "Ok"}'

    return(response)

@app.route("/files/<path:path>")
def get_file(path):
    return send_from_directory(fileRepo, path, as_attachment=True)
    
if __name__ == '__main__':

    config = get_ConfigFile(sys.argv[0]+'.cfg', 'production')

    setuplog(config['logfile'],config['logfile_backup_count'],config['log_level'])

    logit('Log OK')
    logit('Config File OK')
    
    ip = config['listen_ip']

    port = config['listen_port']

    fileRepo = config['files_path']
    if not os.path.exists(fileRepo):
        os.makedirs(fileRepo)

    logit('Audio Folders Configured')

    logit('Starting WS')
    app.run(host=ip, port=port, debug=False)
    logit('WS finished')