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

print(select("status", "usuarios_report", "id_usuarios_report=8")[0]['status'])
