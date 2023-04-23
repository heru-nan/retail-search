import json
from flask import Flask, jsonify, request

app = Flask(__name__)

def get_inventory():
    with open("inventory.json", "r") as f:
        return json.load(f)

@app.route("/inventory", methods=["GET"])
def inventory():
    return jsonify(get_inventory())


@app.route("/inventory/products", methods=["GET"])
def inventoryP():
    name = request.args.get("name")
    names = name.split(" ")
    # find products with that names
    products = []
    for name in names:
        products += [product for product in get_inventory()["productos"] if product["nombre"] == name]

    return jsonify(products)


@app.route("/inventory/category", methods=["GET"])
def inventoryC():
    category = request.args.get("category")

    categorys = category.split(" ")
    # find products with that categorys
    products = []
    for category in categorys:
        products += [product for product in get_inventory()["productos"] if product["categoria"] == category]
    return jsonify(products)

if __name__ == "__main__":
    app.run(port=5001, debug=True)