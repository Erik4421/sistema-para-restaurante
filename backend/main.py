from flask import *
app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = "secret_key"

# <Parte aberta para usuários em geral> 


@app.route("/", methods = ["POST", "GET"])
def home():
    # button = request.form.get('button')
    # if not session.get('open_access'):
    #    return redirect(url_for("entry"))
    return render_template("home.html")

@app.route("/menu")
def menu():
    # if not session.get('open_access'):
    #    return redirect(url_for("entry"))
    return render_template("products_show/menu.html")


# @app.route("/set_access", methods = ["POST"])
# def set_access():
#     if request.form.get('acess_value') == '1':
#         session['open_access'] = True
#     return redirect(url_for("home"))


# <Parte de Gerenciamento>


@app.route("/gerente")
def manager():
    return render_template("manager_screen/manager_login.html")

@app.route("/gerente/gerenciamento")
def manager_utilities():
    return render_template("manager_screen/manager.html")

@app.route("/gerente/gerenciamento/adicionar")
def manager_utilities_add():
    return render_template("products_manager/add.html")

@app.route("/gerente/gerenciamento/modificar")
def manager_utilities_modificar():
    return render_template("products_manager/modify.html")

@app.route("/gerente/gerenciamento/remover")
def manager_utilities_remove():
    return render_template("products_manager/remove.html")


app.run(debug=True, host="0.0.0.0")