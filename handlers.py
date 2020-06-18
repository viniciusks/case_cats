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
                'id_name': r['id'].lower(),
                'name': r['name'].lower(),
                'origin': r['origin'].lower(),
                'temperament': temperament_list,
                'description': r['description'].lower()
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
        breeds_list = []

        # Se não existir um id_name ele traz todas as informações do banco
        if id_name_low == "":
            # Procura todas as raças
            datas = breeds_col.find({}, {'_id': False})
            for data in datas:
                breeds_list.append(data)
            
            # Caso não exista gatos no banco de dados
            if breeds_list == []:
                info = {
                    "msg": "Não existem gatos."
                }
                breeds_list.append(info)
        else:
            # Procura apenas 1 raça
            datas = breeds_col.find({'id_name': id_name_low}, {'_id': False})
            for data in datas:
                breeds_list.append(data)

            # Caso não ache gatos da raça passada
            if breeds_list == []:
                info = {
                    "msg": "Não existe essa raça de gato."
                }
                breeds_list.append(info)
        
        self.ResponseWithJson(1, breeds_list)
        return

class BreedsOriginHandler(DefaultHandler):
    def get(self, origin_name):
        origem_name_low = origin_name.lower()
        breeds_list = []

        # Verifica se tem um valor dentro de origem_name_low
        if origem_name_low == "":
            print("[ERROR] - Argumento de origem faltando.")
            error = {
                "error_msg": "Coloque uma origem!"
            }
            breeds_list.append(error)
            self.ResponseWithJson(0, breeds_list)
            return
        else:
            # Traz apenas os gatos da origem passada
            datas = breeds_col.find({'origin': origem_name_low}, {'_id': False})
            for data in datas:
                breeds_list.append(data)

            # Caso não encontre gatos com a origem passada
            if breeds_list == []:
                info = {
                    "msg": "Não foi encontrado gatos com essa origem."
                }
                breeds_list.append(info)

            self.ResponseWithJson(1, breeds_list)
            return

class BreedsTemperamentHandler(DefaultHandler):
    def get(self, temperament):
        temperament_low = temperament.lower()
        breeds_list = []

        # Verifica se tem valor dentro de temperament_low
        if temperament_low == "":
            print("[ERROR] - Argumento de temperamento faltando.")
            error = {
                "error_msg": "Coloque um temperamento!"
            }
            breeds_list.append(error)
            self.ResponseWithJson(0, breeds_list)
            return
        else:
            # Traz todos os dados e procura dentro do array os temperamentos equivalentes
            datas = breeds_col.find({}, {'_id': False})
            for data in datas:
                for t in data['temperament']:
                    if temperament_low == t:
                        breeds_list.append(data)
            
            # Caso não encontre o temperamento passado
            if breeds_list == []:
                info = {
                    "msg": "Não foi encontrado gatos com esse temperamento."
                }
                breeds_list.append(info)

            self.ResponseWithJson(1, breeds_list)
            return