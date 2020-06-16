import asyncio
import requests
import json
from bson.json_util import dumps
from bson.json_util import loads
from bson import json_util
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

# Constantes
API = "https://api.thecatapi.com/v1/"

# Classe que é a base das chamadas
class DefaultHandler(RequestHandler):
    def initialize(self):
        self.set_header("x-api-key", "4b85ecd6-652a-48d2-9c53-6546526507b1")
        self.set_header("Content-Type", "application/json")
        self.content_type = 'application/json'

    def ResponseWithJson(self,return_code,est_json):
        self.write(json.dumps({"return_code": return_code, "data": est_json}, default=json_util.default))

class MainHandler(DefaultHandler):
    def get(self):
        self.write("Oi, main handler aqui")

class BreedsHandler(DefaultHandler):
    def get(self, id_name):
        id_name_low = id_name.lower()
        # Lista todas as raças, mas não insere no banco ainda
        breeds = {}
        items = []

        if id_name_low == "":
            print("Não deu " + id_name_low)
            req = requests.get(API + "breeds")
            for r in req.json():
                items.append(r)
            breeds = items
        else:
            print(id_name_low)
            req = requests.get(API + "breeds/search?q=" + id_name_low)
            for r in req.json():
                items.append(r)
            breeds = items
        
        if breeds is not {}:
            self.ResponseWithJson(1,breeds)
            breeds = {}
        else:
            self.ResponseWithJson(0,breeds)

class BreedsOriginHandler(DefaultHandler):
    def get(self, origin_name):
        origem_name_low = origin_name.lower()
        # Lista todas as raças de uma certa ORIGEM, mas não insere no banco ainda
        breeds = {}
        items = []

        if origem_name_low == "":
            # PRINT MENSAGEM ERRO
            print("[ERROR] - Coloque uma origem")
            self.ResponseWithJson(0, breeds)
            return
        else:
            print(origem_name_low)
            req = requests.get(API + "breeds")
            for r in req.json():
                if r['origin'].lower() == origem_name_low:
                    items.append(r)
            breeds = items
            self.ResponseWithJson(1, breeds)
            return

class BreedsTemperamentHandler(DefaultHandler):
    def get(self, temperament):
        temperament_low = temperament.lower()
        # Lista todas as raças de uma certa ORIGEM, mas não insere no banco ainda
        breeds = {}
        items = []

        if temperament_low == "":
            # PRINT MENSAGEM ERRO
            print("[ERROR] - Coloque uma origem")
            self.ResponseWithJson(0, breeds)
            return
        else:
            print(temperament_low)
            req = requests.get(API + "breeds")
            for r in req.json():
                list_temperament = r['temperament'].lower().split(", ")
                for l in list_temperament:
                    if l == temperament_low:
                        items.append(r)

            breeds = items
            self.ResponseWithJson(1, breeds)
            return

# Função que define urls
def make_app():
    paths = [
        (r"/", MainHandler),
        (r"/breeds/(.*)", BreedsHandler),
        (r"/breeds-origin/(.*)", BreedsOriginHandler),
        (r"/breeds-temperament/(.*)", BreedsTemperamentHandler),
    ]
    return Application(paths, debug=True)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app = make_app()
    app.listen(8888)
    IOLoop.current().start()

# def teste():
#     print("hi")
# teste()