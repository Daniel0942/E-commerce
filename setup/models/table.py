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
        id_username VARCHAR(50),
        produto VARCHAR(50) NOT NULL,
        quantidade INT NOT NULL,
        preço DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (id_username) REFERENCES users(username)
        )""")
        self.conectar.commit()

    def fecharconexões(self):
        self.cursor.close()
        self.conectar.close()
    
    def reverterCommit(self):
        self.conectar.rollback()