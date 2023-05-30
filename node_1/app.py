import json
from flask import Flask, jsonify, request
import logging
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, help='Puerto para iniciar la aplicación')
args = parser.parse_args()

port = 5000

if args.port is None:
    print("No se proporcionó el puerto. Por favor, proporciona un puerto usando --port.")
else:
    port = args.port

# set variable log_name with the name "logfile" + port variable
log_name = "logfile" + str(port) + ".log"

inventory_name = "inventory" + str(port) + ".json"

class CustomFormatter(logging.Formatter):
    def __init__(self):
        super().__init__(fmt="%(asctime)s - %(funcName)s - %(message)s")
        
    def formatTime(self, record, datefmt=None):
        timestamp = time.time()
        return str(int(timestamp))


# remove werkzeug logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Crear un logger
logger = logging.getLogger('MiAplicacion')
handler = logging.FileHandler(log_name)
handler.setFormatter(CustomFormatter())
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
# Loggear un mensaje

app = Flask(__name__)

def get_inventory():
    logger.info("ini")
    with open(inventory_name, "r") as f:
        logger.info("fin")
        return json.load(f)

@app.route("/inventory", methods=["GET"])
def get_inventory_by_all():
    logger.info("ini")
    res = get_inventory()
    logger.info("fin")
    return jsonify(res)


@app.route("/inventory/products", methods=["GET"])
def get_inventory_by_products():
    logger.info("ini")
    name = request.args.get("name")
    names = name.split(" ")
    # find products with that names
    products = []
    for name in names:
        products += [product for product in get_inventory()["productos"] if product["nombre"] == name]

    logger.info("fin")

    return jsonify(products)


@app.route("/inventory/category", methods=["GET"])
def get_inventory_by_category():
    logger.info("ini")
    category = request.args.get("category")

    categorys = category.split(" ")
    # find products with that categorys
    products = []
    for category in categorys:
        products += [product for product in get_inventory()["productos"] if product["categoria"] == category]
    logger.info("fin")

    return jsonify(products)

if __name__ == "__main__":
    app.run(port=port, debug=True)