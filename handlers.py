import requests
import config
import logging_cats
from pymongo import MongoClient
from main import DefaultHandler

# Conexão Mongo
client = MongoClient(config.APP_SETTINGS['mongodb']['host'], config.APP_SETTINGS['mongodb']['port'])

# Database
db = client[config.APP_SETTINGS['database']]

# Collection
breeds_col = db.breeds
categories_image_col = db.categories_image

# Função para fazer a carga inicial no banco
def verify_data():
    data = breeds_col.find({}, {'_id': False})

    # List das breeds para inserir no banco
    # Model: Id_name, Origem, Temperamento, Descrição, 3 imagens
    breeds_list = []

    if data.count() == 0:
        logging_cats.logging_cats(1, "Collection vazia.")
        logging_cats.logging_cats(1, "Requisitando dados.")
        req = requests.get(config.API + "breeds")

        temperament_list = []

        for r in req.json():

            # Pega 3 imagens para cada raça
            # Por conta desta parte pode levar cerca de 3 minutos a primeira execução
            cont = 0
            images = []
            logging_cats.logging_cats(1, "Pegando imagens.")
            while cont < 3:
                img = requests.get(config.API + "images/search?breed_id=" + r['id'].lower())
                img_json = img.json()
                images.append(img_json[0]['url'])
                cont += 1

            logging_cats.logging_cats(1, "Carregamento de imagens concluída.")

            temperament_list = r['temperament'].lower().split(", ")
            breed = {
                'id_name': r['id'].lower(),
                'name': r['name'].lower(),
                'origin': r['origin'].lower(),
                'temperament': temperament_list,
                'description': r['description'].lower(),
                'images': images
            }
            breeds_list.append(breed)
        logging_cats.logging_cats(1, "Dados solicitados com sucesso!")
        logging_cats.logging_cats(1, "Inserindo no banco.")
        breeds_col.insert_many(breeds_list)
        logging_cats.logging_cats(1, "Inserido com sucesso!")
        return
    logging_cats.logging_cats(1, "Database já existe.")
    logging_cats.logging_cats(1, "Collection já existe.")
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
            logging_cats.logging_cats(1, "Sem nome de raça.")
            logging_cats.logging_cats(1, "Procurando todas as raças.")
            # Procura todas as raças
            datas = breeds_col.find({}, {'_id': False})
            for data in datas:
                breeds_list.append(data)
            
            # Caso não exista gatos no banco de dados
            if breeds_list == []:
                logging_cats.logging_cats(2, "Não existem gatos.")
                info = {
                    "msg": "Não existem gatos."
                }
                breeds_list.append(info)
        else:
            logging_cats.logging_cats(1, "Nome de raça encontrado.")
            logging_cats.logging_cats(1, "Procurando apenas a raça.")
            # Procura apenas 1 raça
            datas = breeds_col.find({'id_name': id_name_low}, {'_id': False})
            for data in datas:
                breeds_list.append(data)

            # Caso não ache gatos da raça passada
            if breeds_list == []:
                logging_cats.logging_cats(2, "Não existe essa raça de gato.")
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
            logging_cats.logging_cats(2, "Coloque uma origem.")
            error = {
                "error_msg": "Coloque uma origem."
            }
            breeds_list.append(error)
            self.ResponseWithJson(0, breeds_list)
            return
        
        logging_cats.logging_cats(1, "Origem encontrada.")
        logging_cats.logging_cats(1, "Procurando gatos desta origem.")
        # Traz apenas os gatos da origem passada
        datas = breeds_col.find({'origin': origem_name_low}, {'_id': False})
        for data in datas:
            breeds_list.append(data)

        # Caso não encontre gatos com a origem passada
        if breeds_list == []:
            logging_cats.logging_cats(2, "Não foi encontrado gatos com essa origem.")
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
            logging_cats.logging_cats(2, "Coloque um temperamento.")
            error = {
                "error_msg": "Coloque um temperamento."
            }
            breeds_list.append(error)
            self.ResponseWithJson(0, breeds_list)
            return
        
        logging_cats.logging_cats(1, "Temperamento encontrado.")
        logging_cats.logging_cats(1, "Procurando gatos deste temperamento.")
        # Traz todos os dados e procura dentro do array os temperamentos equivalentes
        datas = breeds_col.find({}, {'_id': False})
        for data in datas:
            for t in data['temperament']:
                if temperament_low == t:
                    breeds_list.append(data)
        
        # Caso não encontre o temperamento passado
        if breeds_list == []:
            logging_cats.logging_cats(2, "Não foi encontrado gatos com esse temperamento.")
            info = {
                "msg": "Não foi encontrado gatos com esse temperamento."
            }
            breeds_list.append(info)

        self.ResponseWithJson(1, breeds_list)
        return

class CatsImagesHandler(DefaultHandler):
    def post(self, category_id):
        # Certifica que tudo estará minúsculo para a pesquisa
        category_id_low = category_id.lower()

        if category_id_low == "":
            logging_cats.logging_cats(2, "Coloque uma categoria.")
            error = {
                "error_msg": "Coloque uma categoria."
            }

            self.ResponseWithJson(0, error)
            return

        logging_cats.logging_cats(1, "Requisitando imagem da api.")
        # Requisição feita na api cat
        img = requests.get(config.API + "images/search?&category_ids=" + category_id_low)
        img_json = img.json()

        # Objeto para inserir dentro do MongoDB
        categories_image = {
            "name": img_json[0]['categories'][0]['name'],
            "url": img_json[0]['url']
        }

        logging_cats.logging_cats(1, "Inserindo no banco.")
        # Momento da inserção
        categories_image_col.insert_one(categories_image)

        # Response em formato JSON
        self.ResponseWithJson(1,categories_image)
        return