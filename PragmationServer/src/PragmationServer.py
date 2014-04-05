#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 04/04/2014

PragmationServer

@author: Juan Carlos Hdez. (programaando@gmail.com) para CirculoOfij, proyecto Pragmation. 

'''
from flask import Flask
from flask import make_response
from flask import render_template
from flask import request
from flask import jsonify
from Logs import Logs
import json
import requests
import sys
import os
import urllib
import argparse
import traceback



### Static common variables
VERSION = "0.1.0"

### STATIC Variables
CONTEXT_ROOT = "/pragmation/patient"
PACIENTE = "idPaciente"
CONTESTADOS = "numContestadas"
ACERTADOS = "numAcertadas"
EJERCICIOS = "ejercicios"
SEGUNDOS = "segundos"

'''
ejemplo request
# URL 
     http://130.206.82.202:5500/pragmation/patient

# BODY
{
    "idPaciente": "valorId",
    "ejercicios": [
        {
            "idCategoria": 1,
            "idEjercicio": 1,
            "segundos": 15
        }
    ],
    "numContestadas": 2,
    "numAcertadas": 1
}
'''

#######
# Configuration DEFAULTS
SERVER_NAME = '0.0.0.0'
SERVER_PORT = 5500

NOTIFICATION_ENDPOINT = "http://130.206.82.216:1026/NGSI10/updateContext"

NOTIFICATION_TIMEOUT=5.0

DEBUG = False

### Override with environment variables
DEBUG = os.getenv('DEBUG', DEBUG)

### Initialisation
app = Flask(__name__)

### Run Logger
logger = Logs()


def PARSE_JSON_FLOAT(f):
    value = 0.0  # float value
    if 'str' == type(f).__name__:
        value = float(f)
    else:
        value = f

    return float("{0:.2f}".format(value))


def send_context_broker_info(paciente, porcentaje):
    resp = 200
    #logger.info_log(paciente +' ' + porcentaje)
    notification_body = {
        "contextElements": [
            {
                "type": "pragmation",
                "isPattern": "false",
                "id": paciente,
                "attributes": [
                {
                    "name": "aciertos",
                    "type": "porcentaje",
                    "value": porcentaje
                }
                ]
            }
        ],
        "updateAction": "APPEND"
    }
    
 
    headers = {"Content-Type": "application/json", "X-Auth-Token": "Em_RZ3UvtN9EJedfQrJCX-sA60NSwr9mk6tNhT1wxbx0HjZnLg8w8xqWs1-tVfLkyUWMfcp_ta5n3EsmZypfLQ"}
    try:

        #logger.info_log('Message broker request: ' + json.dumps(notification_body))
        
        response = requests.post(NOTIFICATION_ENDPOINT,
                  data=json.dumps(notification_body),
                  headers=headers,
                  timeout=NOTIFICATION_TIMEOUT)                                                            

        logger.warning_log('Message broker response: (' + str(response.status_code) + ') ' + response.text)
        resp = response.status_code
        

    except requests.exceptions.Timeout:
        logger.warning_log('Connection timeout with message broker.')
        resp = 500

    except  requests.exceptions.RequestException:
        logger.warning_log('Connection failure with message broker.')
        resp = 500
        
    return resp

def send_context_broker_time(paciente, tiempo):
    resp = 200
    #logger.info_log(paciente +' ' + porcentaje)
    notification_body = {
        "contextElements": [
            {
                "type": "pragmationTime",
                "isPattern": "false",
                "id": paciente,
                "attributes": [
                {
                    "name": "tiempo",
                    "type": "porcentaje",
                    "value": tiempo
                }
                ]
            }
        ],
        "updateAction": "APPEND"
    }
    
 
    headers = {"Content-Type": "application/json", "X-Auth-Token": "Em_RZ3UvtN9EJedfQrJCX-sA60NSwr9mk6tNhT1wxbx0HjZnLg8w8xqWs1-tVfLkyUWMfcp_ta5n3EsmZypfLQ"}
    try:

        #logger.info_log('Message broker request: ' + json.dumps(notification_body))
        
        response = requests.post(NOTIFICATION_ENDPOINT,
                  data=json.dumps(notification_body),
                  headers=headers,
                  timeout=NOTIFICATION_TIMEOUT)                                                            

        logger.warning_log('Message broker response: (' + str(response.status_code) + ') ' + response.text)
        resp = response.status_code
        

    except requests.exceptions.Timeout:
        logger.warning_log('Connection timeout with message broker.')
        resp = 500

    except  requests.exceptions.RequestException:
        logger.warning_log('Connection failure with message broker.')
        resp = 500
        
    return resp

# Create a new subscription
@app.route(CONTEXT_ROOT, methods=['POST'])
def register_info():
    '''
    Service that registers a new result

    '''
    resp = 200
           
    # Parse JSON
    request_body = None
    try:
        ### Log request
        logger.info_log(request.data)

        request_body = json.loads(request.data, parse_float=PARSE_JSON_FLOAT)

   
        # get info
        paciente = request_body[PACIENTE]
        contestados = request_body[CONTESTADOS]
        acertados = request_body[ACERTADOS]
        tiempo = request_body[EJERCICIOS][0][SEGUNDOS]
        
        porcentaje = None
        
        if (contestados != None and acertados != None):
            porcentaje = str(float((acertados * 100) / contestados))

        #logger.info_log('porcentaje ' + porcentaje)
        resp = send_context_broker_info(paciente, porcentaje)
        
        if(resp <300):
            resp = send_context_broker_time(paciente, tiempo)
        
    except:
        logger.warning_log("some is wrong in the request:" + str(sys.exc_info()[0]))
        logger.warning_log("some is wrong in the request2:" + str(traceback.format_exc()))
        resp = 500


    return '',resp


@app.errorhandler(404)
def page_not_found(error):
    #resp = create_error_response(code="SVC1006", text="Resource does not exist", HTTPcode=500)
    return 404


if __name__ == '__main__':

    ### Default value from environment
    SERVER_NAME = os.getenv('SERVER_NAME', SERVER_NAME)
    SERVER_PORT = int(os.getenv('SERVER_PORT', SERVER_PORT))
    DEBUG = os.getenv('DEBUG', DEBUG)

    ### Parse arguments
    parser = argparse.ArgumentParser(description='Server side of Pragmation application')
    parser.add_argument('--host', '-o', dest='host',
                        default=SERVER_NAME, help='SERVER_NAME', required=False)
    parser.add_argument('--port', '-p', dest='port',
                        default=SERVER_PORT, help='SERVER_PORT', required=False)
    parser.add_argument('--debug', '-d', dest='debug_flag',
                        default=DEBUG, help='DEBUG',
                        choices=['True', 'False'], required=False)
    args = parser.parse_args()

    ### Initiate configuration from ENVIRONMENT VARIABLES
    SERVER_NAME = str(args.host)
    SERVER_PORT = int(args.port)
    DEBUG = bool(args.debug_flag)

    ### App Running
    app.run(host=SERVER_NAME, port=SERVER_PORT, debug=DEBUG)
