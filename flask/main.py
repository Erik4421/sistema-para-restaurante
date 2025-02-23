from flask import *

app = Flask(__name__, template_folder="../templates", static_folder="../static")

menu_items = [
    {"id": 1, "name": "Bebida", "price": 5},
    {"id": 2, "name": "Entrada", "price": 10},
    {"id": 3, "name": "Prato Principal", "price": 20},
    {"id": 4, "name": "Sobremesa", "price": 7},
]

order = []


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/menu")
def menu():
    return render_template("menu.html", menu_items=menu_items)


@app.route("/add_to_order/<int:item_id>")
def add_to_order(item_id):
    # Encontrar o item do menu com o id correspondente
    item = next((i for i in menu_items if i["id"] == item_id), None)
    if item:
        # Adicionar o item ao pedido
        order.append(item)
    return redirect("/order")


@app.route("/order")
def view_order():
    total = sum(item["price"] for item in order)
    return render_template("order.html", order=order, total=total)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")