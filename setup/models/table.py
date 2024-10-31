import mysql.connector

class Conexao():
    def __init__(self):
        self.conectar = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "0942",
            database = "e_commerce"
        )
        self.cursor = self.conectar.cursor()

        # Criando a tabela users
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(50) NOT NULL 
        )""")

        # Criar tabela produtos 
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos(
        id INT PRIMARY KEY AUTO_INCREMENT,
        produto VARCHAR(50) NOT NULL,
        estoque INT NOT NULL,
        preço DECIMAL(10, 2) NOT NULL,
        imagem VARCHAR(100)
        )""")
        self.conectar.commit()

        # Criar tabela carrinho de compras
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS carrinho(
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(50) NOT NULL,
        produto VARCHAR(50) NOT NULL UNIQUE,
        quantidade INT NOT NULL,
        preço DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (username) REFERENCES users(username)
        )""")
        self.conectar.commit()

    def fecharconexões(self):
        self.cursor.close()
        self.conectar.close()
    
    def reverterCommit(self):
        self.conectar.rollback()
    
    def adicionarProdutos(self, produtos):
        try:
            for produto in produtos:
                self.cursor.execute("INSERT INTO produtos (produto, estoque, preço, imagem) VALUES (%s, %s, %s, %s)", (produto["produto"], produto["estoque"], produto["preço"], produto["imagem"]))
                self.conectar.commit()
                print(f"Produto {produto["produto"]} inserido na tabela produtos com sucesso")
        except Exception as e:
            print(f"Ocorreu ao ao inserir produtos ao carrinho: {str(e)}")
            self.conectar.rollback()
        finally:
            self.cursor.close()
            self.conectar.close()

produtos = [
    {"produto": "Fone 520bt",
    "estoque": 20,
    "preço": 250,
    "imagem": "img/fone520bt.png"},

    {"produto": "Fone QCY",
    "estoque": 50,
    "preço": 150,
    "imagem": "img/foneQCY.webp"},

    {"produto": "Echo Dot",
    "estoque": 80,
    "preço": 300,
    "imagem": "img/caixa_de_som(echo).webp"},
]
"""conexao = Conexao()
conexao.adicionarProdutos(produtos)"""