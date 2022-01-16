import sqlite3
from sqlite3 import Error
import os

pastaApp = os.path.dirname(__file__)    # Pega o endereço q está este arquivo atual
nomeBanco = pastaApp+"\\gestor.db"

def ConexaoBanco():
    con = None
    try:
        con = sqlite3.connect(nomeBanco)
    except Error as ex:
        print(ex)
    finally:
        return con

def dql(query): # SELECT # Data Query Language → São os comandos de consulta
    vcon = ConexaoBanco()
    c = vcon.cursor()
    c.execute(query)
    res = c.fetchall()
    vcon.close()
    return res

def dml(query): # INSERT, UPDATE e DELETE # Data Manipulation Language → Permite acesso e manipulação aos dados
    try:
        vcon = ConexaoBanco()
        c = vcon.cursor()
        c.execute(query)
        vcon.commit()
        vcon.close()
    except Error as ex:
        print(ex)

# nome tabela → merceariaResende
# cursor.execute("CREATE TABLE merceariaResende (id INT AUTO_INCREMENT PRIMARY KEY, produto VARCHAR(255), codigo VARCHAR(255), quantidade VARCHAR(255), observacao VARCHAR(255))")
