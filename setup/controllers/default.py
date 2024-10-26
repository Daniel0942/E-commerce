from setup import app
from flask import render_template, flash, redirect, url_for, request, session
from setup.models.table import Conexao

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/registrar")
def registrar():
    return render_template("registrar.html")

@app.route("/loja")
def loja():
    return render_template("loja.html")

# Receber dados do novo registro do front end
@app.route("/registrar", methods = ["POST"])
def CADASTRO():
    username = request.form["username"]
    password = request.form["password"]
    # enviando pro banco
    try:
        conectar = Conexao()
        conectar.cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)",(username, password))
        conectar.conectar.commit()
        flash(f"{username} cadastrado com sucesso")
        return redirect(url_for("login"))
    except Exception as e:
        print(f"[ERRO] ao registrar usuário: {str(e)}")
        flash(f"Erro ao cadastrar {username}")
        return redirect(url_for("registrar"))
    finally:
        conectar.fecharconexões()