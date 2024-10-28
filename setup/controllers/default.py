from setup import app
from flask import render_template, flash, redirect, url_for, request, session
from setup.models.table import Conexao
from mysql.connector import connect, errors

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/registrar")
def registrar():
    return render_template("registrar.html")

@app.route("/loja")
def loja():
    username = session.get("username_foreign")  # Recupera o username da sessão
    # extraindo produtos do banco de dados
    conectar = Conexao()
    conectar.cursor.execute("SELECT * FROM produtos")
    produtos = conectar.cursor.fetchall()
    conectar.fecharconexões()
    return render_template("loja.html", username = username, produtos = produtos)

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
    except errors.IntegrityError as e:
        # Verifica se o erro é de duplicidade de chave única (Código 1062)
        if e.errno == 1062:
            flash("Usuário já existe, escolha outro")
            conectar.reverterCommit()
            return redirect(url_for("registrar"))
        else:
            return print("Erro no banco de dados !")
            conectar.reverterCommit()
            return redirect(url_for("registrar"))
    finally:
        conectar.fecharconexões()

# (Logar) verificar se o username e password estão iguais ao do banco de dados e redicionar o usuário a loja
@app.route("/", methods = ["POST"])
def LOGAR():
    username = request.form["username"]
    password = request.form["password"]
    
    conectar = Conexao()
    conectar.cursor.execute("SELECT username FROM users WHERE username = %s AND password = %s", (username, password))
    username = conectar.cursor.fetchone()
    
    if username:
        session["username_foreign"] = username[0]  #armazenar username na sessão, pra usar na outra tabela
        flash(f"{username} logado com sucesso")
        return redirect(url_for("loja"))
    else:
        flash("Usuário ou senha incorretos !")
        return redirect(url_for("login"))