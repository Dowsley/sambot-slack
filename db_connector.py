import MySQLdb # Lib para banco de dados MySQL
import time # Funções de delay


# Declara acesso ao banco de dados
con = MySQLdb.connect(
	host="localhost",
	user="root",
	password="s4mb0t_cesarschool",
	port = 3306,
	db="database_report"
	)
print(con)


# Parametros do cursor estão definidos para retornar um dict
c = con.cursor(MySQLdb.cursors.DictCursor) 


# Função que devolve dados determinados de uma tabela
def select(fields, tables, where=None):
	global c
	query = "SELECT " + fields + " FROM " + tables

	if (where):
		query += " WHERE " + where

	c.execute(query)
	return c.fetchall()


# Determina quantidade inicial de reports, irá servir de comparador para saber se existe report um novo
aux = len(select("id_usuarios_report","usuarios_report"))


# Loop que realiza a detecção de um report novo e, caso aconteça, quebra o loop e entra no BOT.
print("Detecção iniciada...")
while True:
	cont = 0
	db_info=select("id_usuarios_report, email_usuario, problema_reportado, status","usuarios_report")
	time.sleep(1)

	for i in db_info:
		cont += 1

	if cont > aux:
		print("Nova entrada detectada... Iniciando Bot")
		db_userinfo = db_info[cont-1]
		aux = cont
		con.commit()
		break

	con.commit()