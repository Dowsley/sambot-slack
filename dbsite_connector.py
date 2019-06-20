import MySQLdb
import time

con = MySQLdb.connect( # O nome da tabela é 'mensagens_contatos'
	host="sql223.main-hosting.eu",
	user="u980762916_form",
	password="Recife02",
	port = 3306,
	db="u980762916_form" 
	)
print(con)


# Parametros do cursor estão definidos para retornar um dict
c = con.cursor(MySQLdb.cursors.DictCursor) 


# Função que devolve dados determinados de uma tabela
def select(fields, tables, where=None):
	global c
	query = "SELECT " + fields + " FROM " + tables + ' ORDER BY id_usuarios_report ASC' # Detalhe importante: devolve em ordem ascendente.

	if (where):
		query += " WHERE " + where

	c.execute(query)
	return c.fetchall()


# Determina quantidade inicial de reports, irá servir de comparador para saber se existe report um novo
aux = len(select("id_usuarios_report","mensagens_contatos"))


# Realiza a escuta por uma entrada de report nova e, caso detecte uma, quebra o loop para entrar no BOT.
print("Escutando...")
while True:
	cont = 0
	db_info=select("id_usuarios_report, email_usuario, problema_reportado, status, mensagem","mensagens_contatos")
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