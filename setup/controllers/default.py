from setup import app
from flask import render_template, flash, redirect, url_for, request, session
from setup.models.table import Conexao
from mysql.connector import connect, errors

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/registrar")
def registrar():
    session.pop("username_foreign", None)  # Remove a chave 'user_id' da sessão
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

@app.route("/carrinho")
def carrinho():
    username = session.get("username_foreign")
    conectar = Conexao()
    conectar.cursor.execute("SELECT produtos.produto, carrinho.quantidade, produtos.preço, carrinho.produto_id FROM carrinho JOIN produtos ON carrinho.produto_id = produtos.id WHERE carrinho.username = %s", (username,))
    carrinho = conectar.cursor.fetchall()
    conectar.fecharconexões()
    return render_template("carrinho.html", carrinho = carrinho, username = username)
    
# Receber dados do novo registro do front end
@app.route("/registrar", methods = ["POST"])
def CADASTRO():
    username = request.form["username"]
    password = request.form["password"]
    # enviando pro banco
    if username:
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
    else:
        flash("Campo obrigatório em branco, Digite novamente")
        return redirect(url_for("registrar"))

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
        flash(f"{username[0]} logado com sucesso")
        return redirect(url_for("loja"))
    else:
        flash("Usuário ou senha incorretos !")
        return redirect(url_for("login"))

# fazer logout
@app.route("/logout")
def LOGOUT():
    username = session.get("username_foreign")
    session.pop("username_foreign", None)  # Remove a chave 'user_id' da sessão
    session.pop('_flashes', None)
    flash(f"O {username} foi desconectado com sucesso !")
    return redirect(url_for("login"))

@app.route("/AdicionarCarrinho", methods = ["POST"])
def adicionar_carrinho():
    produto_id = request.form.get("produto_id")
    if produto_id:
        try:
            conectar = Conexao()
            # inserir produto na tabela carrinho
            conectar.cursor.execute("INSERT INTO carrinho (username, produto_id) VALUES (%s, %s)", (session["username_foreign"], produto_id))
            conectar.conectar.commit()
            flash("Produto adicionado com sucesso")
            return redirect(url_for("carrinho"))
        except errors.IntegrityError as e:
            # Verifica se o erro é de duplicidade de chave única (Código 1062)
            if e.errno == 1062:
                flash(f"[ERRO], Produto já adicionado no carrinho! ")
                return redirect(url_for("loja"))
        finally:
            conectar.fecharconexões()
    else:
        flash("Erro ao adicionar produto !")
        return redirect(url_for("loja"))

# Excluir do carrinho
@app.route("/excluir", methods = ["POST"])
def excluir():
    produto_id = request.form.get("produto_id")
    try:
        conectar = Conexao()
        conectar.cursor.execute("DELETE FROM carrinho WHERE produto_id = %s", (produto_id,))
        conectar.conectar.commit()
        flash(f"Produto removido do carrinho !")
        return redirect(url_for("carrinho"))
    except:
            flash(f"Ocorreu erro ao remover produto, tente novamente")
            return redirect(url_for("carrinho"))
    finally:
        conectar.fecharconexões()

# Editar quantidade do carrinho (ta sem funcionar, falta completar o front)
@app.route("/editar", methods= ["POST"])
def editar():
    produto_id = request.form.get("produto_id")
    try:
        conectar = Conexao()
        conectar.cursor.execute("UPDATE carrinho SET quantidade = %s WHERE produtos_id = %s", (quantidade, produto_id))
        conectar.conectar.commit()
        flash("Quantidade atualizada com sucesso")
        return redirect(url_for("carrinho"))
    except:
        flash("Erro ao atualizar quantidade, tente novamente !")
        conectar.reverterCommit()
        return redirect(url_for("carrinho"))
    finally:
        conectar.fecharconexões()