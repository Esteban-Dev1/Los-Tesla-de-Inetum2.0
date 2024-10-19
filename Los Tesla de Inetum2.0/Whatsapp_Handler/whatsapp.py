from flask import Flask, request
import json
import requests
import logging
import time
from concurrent.futures import ThreadPoolExecutor
import imagecontrol
import asyncio


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.json_util import dumps
import datetime
import pytz

#Inicio actualizado

uri = "mongodb+srv://inetumlab:inetumlab@cluster0.f7bgdlj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
mydb = client["whatsappdb"]
mycol = mydb["mensajes"]

executor = ThreadPoolExecutor(2)


logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

WHATSAPP_URL = 'https://graph.facebook.com/v17.0/450468534817177/messages'
WHATSAPP_TOKEN = 'Bearer EAAE7seqacosBO5ASqpnQjdRNyhObOaIGDq40Q811R7PzfRmq2YZCbnNZCXiC32uSbxz7WfohaZABolEIxi2hyCNCQImGCPE2z6VyujWe7mZCFZANjdlaiKqZAdemJMgybaRBoA7YmArJ3TqNiywIdQJ9cGJuu8zvZAq0T8fZCbFNQS8sujOnyoSFOq6ZCogRwZBgU1mQZDZD'


def borrartodo():
    mycol.delete_many({})



def logoimg(phoneNumber):
    headers = {"Authorization": WHATSAPP_TOKEN}
    payload = {"messaging_product": "whatsapp",
               "recipient_type": "individual",
               "to": phoneNumber,
               "type": "image",
                   "image": {
                       "link": "https://inetumlab.lat/static/img/belcorp.jpg"
                   }
               }

    logging.debug(json.dumps(payload, indent=2))
    requests.post(WHATSAPP_URL, headers=headers, json=payload)
    return True


def sticker(phoneNumber):
    headers = {"Authorization": WHATSAPP_TOKEN}
    payload = {"messaging_product": "whatsapp",
               "recipient_type": "individual",
               "to": phoneNumber,
               "type": "sticker",
                   "sticker": {
                       "link": "https://inetumlab.lat/static/img/oxxo2.webp",
                   }
               }

    logging.debug(json.dumps(payload, indent=2))
    requests.post(WHATSAPP_URL, headers=headers, json=payload)
    return True
def sendmapa(phoneNumber):
    headers = {"Authorization": WHATSAPP_TOKEN}
    payload = { "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": phoneNumber,
                "type": "location",
                "location": {
                    "longitude": -77.029100,
                    "latitude": -12.091800,
                    "name": "inetum",
                    "address": "Avenida Javier Prado Este 444 San Isidro, Lima, Peru"
                }
               }

    logging.debug(json.dumps(payload))
    requests.post(WHATSAPP_URL, headers=headers, json=payload)
    return True

def sendcontact (phoneNumber):
    headers = {"Authorization": WHATSAPP_TOKEN}
    payload = { "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": phoneNumber,
                "type": "contacts",
                "contacts": [
                {
                    "addresses": [
                        {
                            "city": "Lima",
                            "country": "Peru",
                            "country_code": "pe",
                            "street": "Calle amador reyna",
                            "type": "WORK"
                        }
                    ],
                    "emails": [
                        {
                            "email": "carmen.rodriguez@belcorp.com",
                            "type": "WORK"
                        }
                    ],
                    "name": {
                        "first_name": "Carmen",
                        "formatted_name": "Carmen Rodriguez",
                        "last_name": "Rodriguez"
                    },
                    "org": {
                        "company": "Belcorp",
                        "department": "Digital Business",
                        "title": "Ventas"
                    },
                    "phones": [
                        {
                            "phone": "+51955190949",
                            "type": "WORK"
                        }
                    ],
                    "urls": [
                        {
                             "url": "https://www.belcorp.com",
                             "type": "WORK"
                        }
                    ]
                }
            ]
               }

    logging.debug(json.dumps(payload))
    requests.post(WHATSAPP_URL, headers=headers, json=payload)
    return True

def setstatus(phoneNumber, estado):
    my_date = datetime.datetime.now(pytz.timezone('America/Lima'))
    filer = {}
    filer["whatsappnum"] = phoneNumber
    addings = {}
    addings["status"] = estado
    addings["lastchattimestamp"] = my_date.isoformat()
    newvalues = {"$set": addings}
    mycol.update_one(filer, newvalues)


def buscawhatsappnum(phoneNumber):
    query = {}
    query ["whatsappnum"] = phoneNumber
    mydoc = mycol.find(query)
    cant = len(list(mydoc.clone()))
    if cant == 1 :
        logging.debug(" Hubo respuesta")
        logging.debug(dumps(mydoc.clone()))
        for doc in mydoc:
            return doc

    return None



def registradetalle(phoneNumber,det):
    my_date = datetime.datetime.now(pytz.timezone('America/Lima'))
    filer = {}
    filer["whatsappnum"] = phoneNumber
    addings = {}
    addings["detalle"] = det
    addings["lastchattimestamp"] = my_date
    addings["status"] = "waitingproductos"
    newvalues = {"$set": addings}
    mycol.update_one(filer, newvalues)

def registraedad(phoneNumber,tech):
    my_date = datetime.datetime.now(pytz.timezone('America/Lima'))
    filer = {}
    filer["whatsappnum"] = phoneNumber
    addings = {}
    addings["tech"] = tech
    addings["lastchattimestamp"] = my_date
    addings["status"] = "waitingubicacion"
    newvalues = {"$set": addings}
    mycol.update_one(filer, newvalues)

def registraubicacion(phoneNumber,ubicacion):
    my_date = datetime.datetime.now(pytz.timezone('America/Lima'))
    filer = {}
    filer["whatsappnum"] = phoneNumber
    addings = {}
    addings["ubiccacion"] = ubicacion
    addings["lastchattimestamp"] = my_date
    addings["status"] = "waitingfoto"
    newvalues = {"$set": addings}
    mycol.update_one(filer, newvalues)

def registranombre(phoneNumber,nombre):
    my_date = datetime.datetime.now(pytz.timezone('America/Lima'))
    filer = {}
    filer["whatsappnum"] = phoneNumber
    addings = {}
    addings["nombre"] = nombre
    addings["lastchattimestamp"] = my_date
    addings["status"] = "waitingedad"
    newvalues = {"$set": addings}
    mycol.update_one(filer, newvalues)


def registraWhatsappnum(phoneNumber):
    my_date = datetime.datetime.now(pytz.timezone('America/Lima'))
    query = {}
    query["whatsappnum"] = phoneNumber
    query["lastchattimestamp"] = my_date
    query["nombre"] = "null"
    query["status"] = "waitingnombre"
    mycol.insert_one(query)

def sendWhastAppMessage(phoneNumber, message):
    headers = {"Authorization": WHATSAPP_TOKEN}
    payload = { "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": phoneNumber,
                "type": "text",
                "text": {"body": message}
               }

    logging.debug(json.dumps(payload))
    requests.post(WHATSAPP_URL, headers=headers, json=payload)
    return True

def showlistaedad(phoneNumber):
    headers = {"Authorization": WHATSAPP_TOKEN}
    payload = {"messaging_product": "whatsapp",
               "recipient_type": "individual",
               "to": phoneNumber,
               "type": "interactive",
               "interactive": {

                   "type": "list",
                   "body": {
                       "text": "Ahora por favor SELECCIONA tu rango de edad"
                   },
                   "action": {
                       "button": "Selecion",
                       "sections": [
                           {
                               "title": "SECTION_1_TITLE",
                               "rows": [
                                   {
                                       "id": "EDAD_R_1",
                                       "title": "18 - 22"
                                   },
                                   {
                                       "id": "EDAD_R_2",
                                       "title": "23  - 28"
                                   },
                                   {
                                       "id": "EDAD_R_3",
                                       "title": "28 - 35"
                                   },
                                   {
                                       "id": "EDAD_R_4",
                                       "title": "35 a Mas"
                                   }
                               ]
                           }
                       ]
                   }


                 }
               }

    logging.debug(json.dumps(payload, indent=2))
    requests.post(WHATSAPP_URL, headers=headers, json=payload)
    return True

def showlistadetalles(phoneNumber):
    headers = {"Authorization": WHATSAPP_TOKEN}
    payload = {"messaging_product": "whatsapp",
               "recipient_type": "individual",
               "to": phoneNumber,
               "type": "interactive",
               "interactive": {

                   "type": "list",
                   "header": {
                       "type": "text",
                       "text": "Eleje un detalle"
                   },
                   "body": {
                       "text": "Ahora por favor SELECCIONA una de las opciones"
                   },
                   "action": {
                       "button": "Selecion",
                       "sections": [
                           {
                               "title": "Estilo",
                               "rows": [
                                   {
                                       "id": "DET_1",
                                       "title": "Reunion Formal"
                                   },
                                   {
                                       "id": "DET_2",
                                       "title": "Reunion informal"
                                   }
                               ]
                           },
                           {
                               "title": "Locacion",
                               "rows": [
                                   {
                                       "id": "DET_3",
                                       "title": "Lugar cerrado"
                                   },
                                   {
                                       "id": "DET_4",
                                       "title": "Aire libre"
                                   }
                               ]
                           },
                           {
                               "title": "Ambiente",
                               "rows": [
                                   {
                                       "id": "DET_3",
                                       "title": "Para noche"
                                   },
                                   {
                                       "id": "DET_4",
                                       "title": "para dia"
                                   }
                               ]
                           }

                       ]
                   }


                 }
               }

    logging.debug(json.dumps(payload, indent=2))
    requests.post(WHATSAPP_URL, headers=headers, json=payload)
    return True


def retornaimagen(phoneNumber):
    headers = {"Authorization": WHATSAPP_TOKEN}
    payload = {"messaging_product": "whatsapp",
               "recipient_type": "individual",
               "to": phoneNumber,
               "type": "image",
                   "image": {
                       "link": "https://inetumlab.lat/static/fotos/output_image2.jpg"
                   }
               }

    logging.debug(json.dumps(payload, indent=2))
    requests.post(WHATSAPP_URL, headers=headers, json=payload)
    return True

def retornaproducto(phoneNumber):
    headers = {"Authorization": WHATSAPP_TOKEN}
    payload = {"messaging_product": "whatsapp",
               "recipient_type": "individual",
               "to": phoneNumber,
               "type": "image",
                   "image": {
                       "link": "https://inetumlab.lat/static/fotos/prod1.jpg"
                   }
               }

    logging.debug(json.dumps(payload, indent=2))
    requests.post(WHATSAPP_URL, headers=headers, json=payload)
    return True

def retornaproducto2(phoneNumber):
    headers = {"Authorization": WHATSAPP_TOKEN}
    payload = {"messaging_product": "whatsapp",
               "recipient_type": "individual",
               "to": phoneNumber,
               "type": "image",
                   "image": {
                       "link": "https://inetumlab.lat/static/fotos/prod2.jpg"
                   }
               }

    logging.debug(json.dumps(payload, indent=2))
    requests.post(WHATSAPP_URL, headers=headers, json=payload)
    return True
def handleWhatsAppMessage(fromId, text):
    ##Long function goes here
    pass


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hola desde Peru</h1>"

@app.route('/webhook', methods=['GET', 'POST'])
def whatsAppWebhook():
    if request.method == 'GET':
        VERIFY_TOKEN = 'inetum'
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return 'error', 403

    if request.method == 'POST':
        data = request.json


        if 'object' in data and 'entry' in data:
            logging.debug(json.dumps(data, indent=2))
            if data['object'] == 'whatsapp_business_account':
                if 'statuses' not in data['entry'][0]['changes'][0]['value']:
                    logging.debug("mensaje de entrada")
                    for entry in data['entry']:

                        msgType = entry['changes'][0]['value']['messages'][0]['type']
                        fromId = entry['changes'][0]['value']['messages'][0]['from']
                        if msgType != "interactive" and msgType != "image" and msgType != "location":

                            fromId = entry['changes'][0]['value']['messages'][0]['from']
                            text = entry['changes'][0]['value']['messages'][0]['text']['body']
                            if str(text).lower() == "borrar todo":
                                borrartodo()
                                sendWhastAppMessage(fromId,f"base de datos borrada")

                            else:

                                resp = buscawhatsappnum(fromId)

                                if resp != None:
                                    nombre = resp["nombre"]
                                    estado = resp["status"]

                                    logging.debug("nombre :" + nombre)
                                    logging.debug("status :" + estado)

                                    if estado == "waitingnombre" :
                                        registranombre(fromId,text)
                                        sendWhastAppMessage(fromId, f"\u2705 Gracias {text}")
                                        showlistaedad(fromId)

                                    elif estado == "waitingubicacion":
                                        registraubicacion(fromId, text)
                                        sendWhastAppMessage(fromId, f"\u2705 Gracias")
                                        sendWhastAppMessage(fromId, f"Ahora permiteme sugerirte algunos de nuestros productos, para ello favor envianos una foto o selfie")

                                    elif estado == "0":
                                        sendWhastAppMessage(fromId, f" Estimado(a) {nombre}, ya hemos registrado sus datos")

                                else:

                                    time.sleep(1)
                                    sendWhastAppMessage(fromId, f"Bienvenido a BELCORP  !!!!")
                                    #logoimg(fromId)
                                    time.sleep(2)
                                    sendWhastAppMessage(fromId, f"Soy sonIA tu asesora virtual  \ud83e\udd16 que te ayudará a verte más bella hoy")
                                    sendWhastAppMessage(fromId, f"Para una mejor experiencia favor indicanos los siguientes datos : ")
                                    sendWhastAppMessage(fromId, f"Tu nombre y apellido: ")
                                    registraWhatsappnum(fromId)

                        elif msgType == "image":
                            code = entry['changes'][0]['value']['messages'][0]['image']['id']
                            nombrearchivo = imagecontrol.getimagen(code)

                            sendWhastAppMessage(fromId, f"\u2705 Su fotografia ha sido recibida")
                            showlistadetalles(fromId)
                            setstatus(fromId, "waitingdetalles")

                        elif msgType == "location":
                            lat = entry['changes'][0]['value']['messages'][0]['location']['latitude']
                            lon = entry['changes'][0]['value']['messages'][0]['location']['longitude']
                            sendWhastAppMessage(fromId, f"\u2705 Su localitzaion ha sido recibida : " + str(lat) + "," + str(lon) )
                            setstatus(fromId, "waitfinal")
                            sendWhastAppMessage(fromId, f"Te presento a tu consultora :")
                            sendcontact(fromId)



                        else:
                            resp = buscawhatsappnum(fromId)

                            if resp != None:

                                estado = resp["status"]
                                nombre = resp["nombre"]

                                if estado == "waitingedad":

                                    accionid = entry['changes'][0]['value']['messages'][0]['interactive']['list_reply']['id']
                                    registraedad(fromId, accionid)
                                    sendWhastAppMessage(fromId, f"\u2705 Muchas gracias por indicar su rango de edad")
                                    sendWhastAppMessage(fromId, f"Indícanos de que ciudad nos escribes")

                                elif estado == "waitingdetalles" :

                                    accionid = entry['changes'][0]['value']['messages'][0]['interactive']['list_reply']['id']
                                    registradetalle(fromId, accionid)
                                    sendWhastAppMessage(fromId, f"\u2705 Muchas gracias por los detalles adicionales")
                                    sendWhastAppMessage(fromId, f"En base a tus detalles tenemos una recomendacionde maquillaje para ti y un producto que te va a gustar")
                                    time.sleep(0.5)
                                    retornaimagen(fromId)
                                    time.sleep(0.5)
                                    retornaproducto(fromId)
                                    time.sleep(0.5)
                                    sendWhastAppMessage(fromId, f"Se ha identificado que por el contorno de tu rostro los colores de labios y cejas transmiten una estetica de armonia evocando calma y conexion con tu entorno")
                                    time.sleep(2)
                                    sendWhastAppMessage(fromId, f"Para poder asignarte a la consultora mas cercana favor enviarnos tu ubicacion")
                                    setstatus(fromId, "waitinglocation")


        return 'success', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555)





