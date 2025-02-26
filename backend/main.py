from flask import *
import productSQL, userManagerSQL
import sqlite3
from functools import wraps

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = "secret_key"

# Função para todos os produtos de determinada categoria
def get_products_by_category(category_name):
    conn = sqlite3.connect('productSQL.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT products.* FROM products
        JOIN category ON products.categoriaId = category.id
        WHERE category.nome = ?
    ''', (category_name,))
    data = cursor.fetchall()
    conn.close()
    return data

# Função para verificar se o usuário está logado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect("/gerente")
        return f(*args, **kwargs)
    return decorated_function


def alter_verify(column, id):
    # Lista de colunas válidas para garantir que o nome da coluna seja válido
    valid_columns = ['nome', 'descricao', 'preco']  # Exemplo, ajuste conforme necessário

    if column not in valid_columns:
        raise ValueError("Coluna inválida")

    conn = sqlite3.connect('productSQL.sqlite')
    cursor = conn.cursor()
    
    # Construção da consulta SQL dinamicamente com o nome da coluna
    query = f"SELECT {column} FROM products WHERE id = ?"
    
    cursor.execute(query, (id,))
    data = cursor.fetchone()
    
    conn.close()
    return data[0]




# <Parte aberta para usuários em geral> 

@app.route("/", methods = ["POST", "GET"])
def home():
    return render_template("home.html")

@app.route("/menu")
def menu():
    categoria = request.args.get('categoria', '')  # Captura a categoria da URL
    produtos = get_products_by_category(categoria) if categoria else []
    return render_template("products_show/menu.html", list=produtos, categoria=categoria)

@app.route("/gerente")
def manager():
    return render_template("manager_screen/manager_login.html")

@app.route("/gerente/gerenciamento")
@login_required
def manager_utilities():
    return render_template("manager_screen/manager.html")

@app.route("/gerente/gerenciamento/adicionar")
@login_required
def manager_utilities_add():
    product_list = productSQL.list()
    return render_template("products_manager/add.html", list = product_list)

@app.route("/gerente/gerenciamento/modificar")
@login_required
def manager_utilities_modify():
    product_list = productSQL.list()
    return render_template("products_manager/modify.html", list = product_list)

@app.route("/gerente/gerenciamento/remover")
@login_required
def manager_utilities_remove():
    product_list = productSQL.list()
    return render_template("products_manager/remove.html", list = product_list)




# <Gerenciando produtos>
@app.route("/gerente/gerenciamento/add", methods=["POST", "GET"])
@login_required
def manager_sql_add():
    if request.method == 'POST':
        name = request.form.get('name-products')
        description = request.form.get('description-products')
        price = float(request.form.get('price-products'))
        category = int(request.form.get("category-products"))
        if(name and description and price):
            productSQL.insert(name, description, price, category)
            print("Produto cadastrado!!")
        return redirect("adicionar")
    product_list = productSQL.list()
    userManagerSQL.list()
    return render_template("products_manager/add.html", list = product_list)

@app.route("/gerente/gerenciamento/modify", methods=["POST", "GET"])
@login_required
def manager_sql_modify():
    if request.method == 'POST':
        id = int(request.form.get('id-products'))
        name = request.form.get('name-products')
        description = request.form.get('description-products')
        price = float(request.form.get('price-products'))

        if name == "":
            name = alter_verify("nome", id)
        if description == "":
            description = alter_verify("descricao", id)
        if price == "":
            price = alter_verify("preco", id)
  
        productSQL.alter(name, description, price, id)
        
        return redirect("modificar")
    product_list = productSQL.list()
    return render_template("products_manager/modify.html", list = product_list)

@app.route("/gerente/gerenciamento/remove", methods=["POST", "GET"])
@login_required
def manager_sql_remove():
    if request.method == 'POST':
        id = int(request.form.get('id-products'))
        productSQL.delete(id)
        return redirect("remover")
    product_list = productSQL.list()
    return render_template("products_manager/remove.html", list = product_list)





# <Login gerente>
@app.route("/gerente/login", methods=["POST", "GET"])
def manager_login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        if(userManagerSQL.login(login, password)):
            session['user'] = login
            return redirect("gerenciamento")
        else:
            print("Deu errado")
    return render_template("manager_screen/manager_login.html")

@app.route("/gerente/logout")
@login_required  # Garante que o usuário esteja logado
def logout():
    session.pop('user', None)  # Remove o login do gerente da sessão
    return redirect(url_for('manager_login'))

app.run(debug=True, host="0.0.0.0")