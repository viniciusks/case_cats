import requests
import config
from pymongo import MongoClient
from main import DefaultHandler

# Conexão Mongo
client = MongoClient(config.APP_SETTINGS['mongodb']['host'], config.APP_SETTINGS['mongodb']['port'])

# Database
db = client[config.APP_SETTINGS['database']]

# Collection
breeds_col = db.breeds

# Função para fazer a carga inicial no banco
def verify_data():
    data = breeds_col.find({}, {'_id': False})

    # List das breeds para inserir no banco
    # Model: Id_name, Origem, Temperamento, Descrição, 3 imagens
    breeds_list = []

    if data.count() == 0:
        print("Collection vazia")
        print("Requisitando dados de CATSAPI...")
        req = requests.get(config.API + "breeds")

        temperament_list = []

        for r in req.json():
            temperament_list = r['temperament'].lower().split(", ")
            breed = {
                'id_name': r['id'],
                'name': r['name'],
                'origin': r['origin'],
                'temperament': temperament_list,
                'description': r['description']
            }
            breeds_list.append(breed)
        print("Dados solicitados com sucesso...")
        print("Inserido no banco...")
        breeds_col.insert_many(breeds_list)
        print("Inserido com sucesso!")
        return
    print("Database existe, collection contém dados...")
    return

class HelloHandler(DefaultHandler):
    def get(self):
        self.write("Oi, main handler aqui")

class BreedsHandler(DefaultHandler):
    def get(self, id_name):
        id_name_low = id_name.lower()
        # Lista todas as raças, mas não insere no banco ainda
        breeds_list = []

        # Se não existir um id_name ele traz todas as informações do banco
        if id_name_low == "":
            # Procura todas as raças
            datas = breeds_col.find({}, {'_id': False})
            for data in datas:
                breeds_list.append(data)
            self.ResponseWithJson(1, breeds_list)
            return
        else:
            # Procura apenas 1 raça
            datas = breeds_col.find({'id_name': id_name_low}, {'_id': False})
            for data in datas:
                breeds_list.append(data)
            self.ResponseWithJson(1, breeds_list)
            return

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
            req = requests.get(config.API + "breeds")
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
            req = requests.get(config.API + "breeds")
            for r in req.json():
                list_temperament = r['temperament'].lower().split(", ")
                for l in list_temperament:
                    if l == temperament_low:
                        items.append(r)

            breeds = items
            self.ResponseWithJson(1, breeds)
            return