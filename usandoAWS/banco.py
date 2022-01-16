import pymysql
""" 
db = pymysql.connect(host = 'teste-gestor.c4rucplnsq72.sa-east-1.rds.amazonaws.com',
                user = 'admin',
                passwd = 'admin123',
                database = 'gestor_teste')

cursor = db.cursor()


sql = '''CREATE DATABASE gestor_teste'''
cursor.execute(sql)

sql = "CREATE TABLE merceariaResende (id INT AUTO_INCREMENT PRIMARY KEY, produto TEXT, codigo TEXT, quantidade TEXT, observacao TEXT)"
cursor.execute(sql)
cursor.connection.commit()



sql = "SHOW TABLES"
cursor.execute(sql)
print(cursor.fetchall())
"""

def ConexaoBanco():
    con = None
    try:
        con = pymysql.connect(
            host = 'teste-gestor.c4rucplnsq72.sa-east-1.rds.amazonaws.com',
            user = 'admin',
            passwd = 'admin123',
            database = 'gestor_teste')
    except:
        print("Erro na conexão!")
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


dml('INSERT INTO merceariaResende (produto, codigo, quantidade, observacao) VALUES ("coca", "123", "5", "teste4")')

print(dql("SELECT * FROM merceariaResende"))


# Nome DB: gestor_teste
# Nome table: merceariaResende