import requests, json
import random

def getimagen (code) :

    endpoint = "https://graph.facebook.com/v21.0/" + code + "/"
    headers = {"Authorization": "XXXXXX"}

    r = requests.get(endpoint,  headers=headers)
    json_data = json.loads(r.text)
    endpoint2 = json_data['url']

    r2 = requests.get(endpoint2,  headers=headers)
    resheaders = dict(r2.headers)
    contenttype = resheaders['Content-Type']
    rbinary=r2.content
    print (rbinary)

    img_name = "imagen" + str(random.randint(1000000, 9999999))
    rutaimagen = "/home/whatsappbot/development/whatsappchat/static/fotos/" + img_name

    if (contenttype=="image/png"):
        rutaimagen = rutaimagen + ".png"
    elif (contenttype=="image/jpeg"):
        rutaimagen = rutaimagen + ".jpg"

    with open(rutaimagen, 'wb') as handler:
        handler.write(rbinary)

    return img_name

def main():
    getmagen("1761872591214516")

if __name__=="__main__":
    main()

