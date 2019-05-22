import MySQLdb
import time

con = MySQLdb.connect(
	host="localhost",
	user="root",
	password="s4mb0t_cesarschool",
	port = 3306,
	db="database_report"
	)
print(con)

c = con.cursor(MySQLdb.cursors.DictCursor) #Parametros do cursor estão definidos para retornar um dict

def select(fields, tables, where=None): #Seletor
	global c
	query = "SELECT " + fields + " FROM " + tables

	if (where):
		query += " WHERE " + where

	c.execute(query)
	return c.fetchall()


aux = len(select("id_usuarios_report","usuarios_report"))
print("Aux =",aux)

while True:
	cont = 0
	db_info=select("id_usuarios_report, email_usuario, problema_reportado, status","usuarios_report")
	time.sleep(1)

	for i in db_info:
		cont+=1
		print("Cont: {}".format(cont))

	if cont > aux:
		print("Detectada nova entrada!")
		db_userinfo = db_info[cont-1]
		aux = cont
		con.commit()
		break

	con.commit()




