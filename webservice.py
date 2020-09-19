#!flask/bin/python
from flask import Flask, abort, request, jsonify, g, url_for
import sys
import configparser
import logging
import logging.handlers
import os
# from autoDeploy import validatePush, rebaseBranchs

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

# Read configurationFile
def get_ConfigFile(inifile, section):

	c = configparser.ConfigParser()

	dataset = c.read(inifile)

	if len(dataset) != 1:

		raise ValueError

	try:

		c.read(inifile)

	except Exception as e:

		raise e

	# Verify keys in configuration file
	for key in c[section]:

		if len(c[section][key]) == 0:

			fatal("fatal: %s: could not find %s string" % (inifile, key), 1)

	return c[section]

# Method for data query (Verify API Integrity)
@app.route('/healthcheck', methods=['GET'])
def get():
	
	logit('Receiving GET on /healthcheck')

	# Response if OK
	response = '{"status": "Ok"}'

	logit('GET OK')
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