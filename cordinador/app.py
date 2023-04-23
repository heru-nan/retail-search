import json
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

def get_node_endpoints():
    with open("nodes.txt", "r") as f:
        return [line.strip() for line in f]

@app.route("/search", methods=["GET"])
def search_product():
    # Get the product name from the query string or category name from the query
    
    
    product_name = request.args.get("productos")
    category_name = request.args.get("categorias")

    if not product_name and not category_name:
        return jsonify({"error": "Missing 'categorias or productos' parameter"}), 400

    products = []
    nodes = get_node_endpoints()

    categorias_by_node = { "lista1": [
        "fruta",
        "grano",
        "lacteo",
        "pan",
        "bebida"
    ],
    "lista2": [
        "ropa",
        "calzado",
        "electronica",
        "accesorio",
        "bebida"
    ],
    "lista3": [
        "alimento",
        "accesorio",
        "cuidado",
        "hogar",
        "bebida"
    ]
    }

    if(product_name):
        for node in nodes:
            try:
                response = requests.get(f"{node}/inventory/products?name={product_name.lower()}")
                if response.status_code == 200:
                    inventory_arr = response.json()
                    for product in inventory_arr:
                        products.append(product)

            except requests.exceptions.RequestException:
                pass

    if(category_name):
        for node, cat_bynode in zip(nodes, categorias_by_node.values()):
            category_name_arr = category_name.split(" ")
            # check if some elements of category_name_arr are in cat_bynode
            if not any(elem in cat_bynode for elem in category_name_arr):
                continue

            try:
                response = requests.get(f"{node}/inventory/category?category={category_name.lower()}")
                if response.status_code == 200:
                    inventory_arr = response.json()
                    for product in inventory_arr:
                        products.append(product)

            except requests.exceptions.RequestException:
                pass

    return jsonify({"products": products})

if __name__ == "__main__":
    app.run(debug=True)
