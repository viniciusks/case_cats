import asyncio
import requests
import json
import config
import handlers
from bson.json_util import dumps
from bson.json_util import loads
from bson import json_util
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

# Classe que é a base das chamadas
class DefaultHandler(RequestHandler):
    def initialize(self):
        self.set_header("x-api-key", "4b85ecd6-652a-48d2-9c53-6546526507b1")
        self.set_header("Content-Type", "application/json")
        self.content_type = 'application/json'

    def ResponseWithJson(self,return_code,est_json):
        self.write(json.dumps({"return_code": return_code, "data": est_json}, default=json_util.default))

# Função que define urls
def make_app():
    handlers.verify_data()
    paths = [
        (r"/", handlers.HelloHandler),
        (r"/breeds/(.*)", handlers.BreedsHandler),
        (r"/breeds-origin/(.*)", handlers.BreedsOriginHandler),
        (r"/breeds-temperament/(.*)", handlers.BreedsTemperamentHandler),
        (r"/cats-category-images/(.*)", handlers.CatsImagesHandler),
    ]
    return Application(paths)

if __name__ == "__main__":
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app = make_app()
    app.listen(8888)
    IOLoop.current().start()

# def teste():
#     print("hi")
# teste()